from typing import Any, Optional, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SessionStarted, ActionExecuted, SlotSet
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher, Action
import logging
from importlib.metadata import version

logger = logging.getLogger(__name__)
vers = "Vers: 1.1.3, Date: Oct 15, 2022"


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        channel = tracker.get_latest_input_channel()
        metadata = tracker.get_slot("session_started_metadata")
        events = [SessionStarted(), ActionExecuted("action_listen")]

        # resp.aud; // aud(ience) stores the actions project id
        # req.headers['x-forwarded-host'] 'x-original-url'
        logger.debug(f"channel:  {channel}")
        logger.debug(f"metadata: {metadata}")

        if channel and channel.startswith("google"):
            events.append(SlotSet("bot_name", "mqtt"))
        elif metadata and metadata["handler"]:
            events.append(SlotSet("bot_name", "mqtt"))
        else:
            events.append(SlotSet("bot_name", "joke"))
        # the session should begin with a `session_started` event and an `action_listen`
        # as a user message follows
        return events


class ActionVersion(Action):
    def name(self):
        logger.info("ActionVersion self called")
        logger.info(f"rasa-sdk: {version('rasa-sdk')}")
        # define the name of the action which can then be included in training stories
        return "action_version"

    def run(self, dispatcher, tracker, domain):
        rasa_sdk_version = version('rasa-sdk')
        logger.info(f">> rasa-sdk version: {rasa_sdk_version}")
        dispatcher.utter_message(f"Rasa SDK:  {rasa_sdk_version}\nActions: {vers}")
        return []


class ActionShowSlots(Action):
    def name(self):
        logger.info("ActionVersion self called")
        # define the name of the action which can then be included in training stories
        return "action_show_slots"

    def run(self, dispatcher, tracker, domain):
        with tracing.extract_start_span(tracer, domain.get("headers"), self.name()):
            msg = "Slots:\n"
            for k, v in tracker.slots.items():
                msg += f" {k} | {v}\n"
            dispatcher.utter_message(msg)
            return []


def get_last_event_for(
    tracker,
    event_type: Text,
    action_names_to_exclude: List[Text] = None,
    skip: int = 0,
) -> Optional[Any]:
    def filter_function(e):
        has_instance = e
        if e["event"] == event_type:
            has_instance = e
        excluded = e["event"] != event_type or (
            (
                e["event"] == event_type
                and (
                    (e["parse_data"]["intent"]["name"] == "domicile")
                    or (e["parse_data"]["intent"]["name"] == "customertype")
                )
            )
        )
        return has_instance and not excluded

    filtered = filter(filter_function, reversed(tracker.events))
    for i in range(skip):
        next(filtered, None)

    return next(filtered, None)


def intentHistoryStr(tracker, skip, past):
    msg = ""
    prev_user_event = get_last_event_for(tracker, "user", skip=skip)
    if not prev_user_event:
        return "No prev msg"
    logger.info(
        "event.text: {}, intent: {}, confidence: {}".format(
            prev_user_event["text"],
            prev_user_event["parse_data"]["intent"]["name"],
            prev_user_event["parse_data"]["intent"]["confidence"],
        )
    )
    msg = "Ranked F1 scores:\n"
    msg += (
        "* "
        + prev_user_event["parse_data"]["intent"]["name"]
        + " ("
        + "{:.4f}".format(prev_user_event["parse_data"]["intent"]["confidence"])
        + ")\n"
    )
    for i in range(past - 1):
        msg += (
            "* "
            + prev_user_event["parse_data"]["intent_ranking"][i + 1]["name"]
            + " ("
            + "{:.4f}".format(prev_user_event["parse_data"]["intent_ranking"][i + 1]["confidence"])
            + ")\n"
        )
    return msg
    # msg += "* " + prev_user_event["parse_data"]["intent_ranking"][2]["name"] + " (" + "{:.4f}".format(prev_user_event["parse_data"]["intent_ranking"][2]["confidence"]) + ")\n"
    # msg += "* " + prev_user_event["parse_data"]["intent_ranking"][3]["name"] + " (" + "{:.4f}".format(prev_user_event["parse_data"]["intent_ranking"][3]["confidence"]) + ")"


class ActionF1Scores(Action):
    def name(self):
        print("ActionLastIntent self called")
        # define the name of the action which can then be included in training stories
        return "action_f1_score"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        msg = intentHistoryStr(tracker, 1, 4)
        dispatcher.utter_message(msg)  # send the message back to the user
        return []
