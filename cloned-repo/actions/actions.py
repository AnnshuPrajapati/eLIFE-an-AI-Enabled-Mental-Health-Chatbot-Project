# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from typing import Dict, Text, Any, List, Union, Type, Optional

import typing
import logging
import requests
import json
import re
import csv
import random

# from . import otel
# import tracing

from rasa_sdk.events import SlotSet, AllSlotsReset, EventType
from rasa_sdk.types import DomainDict
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher, Action

# from rasa_core.trackers import (
#    DialogueStateTracker, ActionExecuted,
#    EventVerbosity)
# from rasa_core.policies.fallback import FallbackPolicy
# from rasa_core.domain import Domain
from datetime import datetime, date, time, timedelta

# from rasa_core.utils import AvailableEndpoints
# from rasa_core.tracker_store import TrackerStore

logger = logging.getLogger(__name__)
vers = "vers: 0.1.3, date: Apr 27, 2022"
logger.debug(vers)

# otel.init_tracer("action_server")
# tracer = tracing.init_tracer("action_server")


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


def log_slots(tracker):
    # import copy
    # Log currently set slots
    logger.debug("tracker now has {} events".format(len(tracker.events)))
    prev_user_event = get_last_event_for(tracker, "user", skip=1)
    logger.debug(
        "event.text: {}, intent: {}, confidence: {}".format(
            prev_user_event["text"],
            prev_user_event["parse_data"]["intent"]["name"],
            prev_user_event["parse_data"]["intent"]["confidence"],
        )
    )
    feedback_answer = tracker.get_slot("feedback")
    logger.debug("feedback: {}".format(feedback_answer))


class ActionKanye(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_kanye"

    def run(self, dispatcher, tracker, domain):
        # with tracing.extract_start_span(
        #    tracer, domain.get("headers"), self.name()
        # ):
        # r = requests.get("https://api.kanye.rest")
        request = json.loads(requests.get("https://api.kanye.rest").text)
        joke = request["quote"]  # extract a joke from returned json response
        dispatcher.utter_message(joke)  # send the message back to the user
        return []


class ActionChuck(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_chuck"

    def run(self, dispatcher, tracker, domain):
        request = json.loads(requests.get("https://api.chucknorris.io/jokes/random").text)  # make an apie call
        joke = request["value"]  # extract a joke from returned json response
        dispatcher.utter_message(joke)  # send the message back to the user
        return []


class ActionRon(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_ron"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(
            requests.get("https://ron-swanson-quotes.herokuapp.com/v2/quotes").text
        )  # make an apie call
        logger.debug("request: {}".format(request))
        joke = request[0] + " - Ron Swanson"
        logger.debug("joke: {}".format(joke))
        dispatcher.utter_message(joke)  # send the message back to the user
        return []


class ActionBreakingBad(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_breaking"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(
            requests.get("https://breaking-bad-quotes.herokuapp.com/v1/quotes").text
        )  # make an apie call
        author = request[0]["author"]
        quote = request[0]["quote"]
        message = quote + " - " + author
        # message = quote + ' - [' + author + '](' + permalink + ')'
        dispatcher.utter_message(message)  # send the message back to the user
        return []


class ActionCorny(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_corny"

    def run(self, dispatcher, tracker, domain, **kwargs):
        # what your action should do
        request = "API Failure"
        author = ""
        try:
            author = ""
            quote = "Sorry, API Service down"
            req = requests.get("https://official-joke-api.appspot.com/random_joke")
            if req.status_code == 200:
                request = json.loads(req.text)  # make an api call
                author = request["punchline"]
                quote = request["setup"]
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Error: {e}")
        message = quote + " - " + author
        # message = quote + ' - [' + author + '](' + permalink + ')'
        dispatcher.utter_message(message)  # send the message back to the user
        return []


class ActionInspiring(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_inspiring"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = requests.get("https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json")
        if request.status_code == 200:
            logger.info("request.text: {}".format(request.text))
            fixed = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r"", request.text)
            resp = json.loads(fixed)
            author = resp["quoteAuthor"]
            quote = resp["quoteText"]
            permalink = resp["quoteLink"]
            # message = quote + ' - ' + author + ' ' + permalink
            message = quote + " - [" + author + "](" + permalink + ")"
        else:
            message = "quote service error (exceeded max free quotes?), error: " + str(request.status_code)
        # dispatcher.utter_message(message) #send the message back to the user
        dispatcher.utter_message(message)  # send the message back to the user
        return []


class ActionGeek(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_geek"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(requests.get("http://quotes.stormconsultancy.co.uk/random.json").text)  # make an apie call
        author = request["author"]
        quote = request["quote"]
        permalink = request["permalink"]
        # message = quote + ' - ' + author + ' ' + permalink
        message = quote + " - [" + author + "](" + permalink + ")"
        dispatcher.utter_message(message)  # send the message back to the user
        return []


class ActionTrump(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_trump"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(
            requests.get("https://api.whatdoestrumpthink.com/api/v1/quotes/random").text
        )  # make an apie call
        joke = request["message"] + " - Donald Trump"
        dispatcher.utter_message(joke)  # send the message back to the user
        return []


class ActionCreed(Action):
    def __init__(self):
        self.quotes = [
            "I wanna do a cartwheel. But real casual like. Not enough to make a big deal out of it, but I know everyone saw it. One stunning, gorgeous cartwheel",
            "I've been involved in a number of cults, both a leader and a follower. You have more fun as a follower, but you make more money as a leader.",
            "Just pretend like we're talking until the cops leave.",
            "I already won the lottery. I was born in the US of A baby. And as backup I have a Swiss passport.",
            "The Taliban's the worst. Great heroin though.",
            "I run a small fake-ID company from my car with a laminating machine that I swiped from the Sheriff's station.",
            "Ryan, you told Toby that Creed has a distinct old man smell",
            "I know exactly what he's talking about, I sprout mung beans on a damp paper towel in my desk drawer, very nutritious but they smell like death",
            "Nobody steals from Creed Bratton and gets away with it. The last person to do this disappeared. His name: Creed Bratton.",
            "The only difference between me and a homeless man is this job. I will do whatever it takes to survive… like I did when I was a homeless man.",
            "I am not offended by homosexuality, in the sixties I made love to many, many women, often outdoors in the mud & rain. It's possible a man could've slipped in there. There'd be no way of knowing.",
            "You ever notice you can only ooze two things? Sexuality and pus.",
        ]

    def name(self):
        return "action_creed"

    def run(self, dispatcher, tracker, domain):
        n = random.randint(0, len(self.quotes) - 1)
        dispatcher.utter_message(self.quotes[n])  # send the message back to the user
        return []


class ActionDuckingTimeRange(Action):
    """Calculate time range
    ToDo:
      - Support additional grains (week, month, year)
      - Start date must be before end, when `time_from` is set, could be a later date
      - Fixup future dates
      - Handle null duckling entity, "start last weds"
      - Relative statements - "add a week"
    """

    def name(self) -> Text:
        return "action_time_range"

    def _extractRange(self, duckling_time, grain):
        import re

        range = dict()
        range["from"] = duckling_time
        range["to"] = duckling_time
        if grain == "day":
            # strip timezone because of strptime limitation - https://bugs.python.org/issue22377
            # 2020-02-06T00:00:00.000-08:00
            # duckling_time = re.sub(r'\.000', r' ', duckling_time)
            # duckling_time = duckling_time[:19]
            logger.info(f"time w/o ms: {duckling_time}")
            duckling_dt = datetime.strptime(duckling_time, "%Y-%m-%dT%H:%M:%S")
            # dt = datetime.strptime("2020-03-07T00:00:00 -07:00", "%Y-%m-%dT%H:%M:%S %z")
            logger.info(f"duckling_dt: {duckling_dt}")
            dt_delta = duckling_dt + timedelta(hours=24)
            range["to"] = dt_delta.strftime("%Y-%m-%dT%H:%M:%S%z")

        return range

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        # existing slot values
        from_time = tracker.get_slot("from_time")
        to_time = tracker.get_slot("to_time")

        # duckling value
        duckling_time = tracker.get_slot("time")

        logger.info(
            f"duckling_time: {type(duckling_time)}, value: {duckling_time}, to_time: {to_time}, from_time: {from_time}"
        )
        # do we have a range
        if type(duckling_time) is dict:
            from_time = tracker.get_slot("time")["from"][:19]
            to_time = tracker.get_slot("time")["to"][:19]
        else:
            logger.info(f"latest_message: {tracker.latest_message}")
            entities = tracker.latest_message.get("entities", [])
            logger.info(f"entities 1: {entities}")
            entities = {e["entity"]: e["value"] for e in entities}
            logger.info(f"entities: {entities}")
            additional_info = tracker.latest_message.get("entities", [])[0]["additional_info"]
            logger.info(f"grain: {additional_info['grain']}")
            state = tracker.current_state()
            intent = state["latest_message"]["intent"]["name"]
            logger.info(f"intent: {intent}")
            if intent == "time_from" and to_time:
                logger.info(f"setting from_time: {duckling_time[:19]}")
                from_time = duckling_time[:19]
            else:
                range = self._extractRange(duckling_time[:19], additional_info["grain"])
                from_time = range["from"]
                to_time = range["to"]

        # entities = {e["entity"]: e["value"] for e in entities}
        # logger.info(f"entities 2: {entities}")
        # entities_json = json.dumps(entities)

        # date = datetime.datetime.now().strftime("%d/%m/%Y")
        # dispatcher.utter_message(text=entities_json)
        logger.info(f"from: {from_time} to: {to_time}")
        dispatcher.utter_message(text=f"from: {from_time}\n  to: {to_time}")

        return [SlotSet("from_time", from_time), SlotSet("to_time", to_time)]
