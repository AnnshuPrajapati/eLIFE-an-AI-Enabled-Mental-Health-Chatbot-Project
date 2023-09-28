# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List, Optional, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
from datetime import timedelta
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.types import DomainDict
import requests
import json
from json import dump
import random
import nrclex
from nrclex import NRCLex

#.................joke.....................................................    
class ActionTellJoke(Action):
    def name(self):
        return "action_tell_joke"
    def run(self, dispatcher, tracker, domain):
        url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        response = requests.get(url)
        joke = response.json()

        if joke["type"] == "single":
            joke_text = joke["joke"]
        else:
            joke_text = joke["setup"] + " " + joke["delivery"]

        dispatcher.utter_message(joke_text)
        return []




#.................LogGratitude.....................................................    
class ActionLogGratitude(Action):

    def name(self) -> Text:
        return "action_log_gratitude"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the moment of gratitude from the user
        moment = tracker.latest_message['text']

       # Log the gratitude message in a file with timestamp
        with open('gratitude_log.txt', 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {moment}\n")

        # Log the moment of gratitude in a file or database
        # ...

        # Send a response to the user to confirm that their gratitude has been logged
        dispatcher.utter_message(text="Thanks for sharing your moment of gratitude!")

        return []



#.................disclaimer.....................................................    
class ActionDisclaimer(Action):
    def name(self) -> Text:
        return "action_disclaimer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # message = "[Hello, I am a chatbot designed to provide assistance and answer your questions to the best of my abilities.However, please note that my responses are based on the information provided and may not always be accurate. If you require specific or professional advice, please consult an expert in the relevant field. Additionally, I may collect and store information for the purpose of improving my services. Do you agree to continue with this conversation?]"
        message = "------------------------------------⚠️ Disclaimer ⚠️-----------------------------------\nHello, I am a eLIFE bot chatbot designed to provide assistance and\nanswer your questions to the best of my abilities. However, please\nnote that my responses are based on the information provided &\nmay not always be accurate.\nIf you are experiencing a mental health emergency, please contact\na qualified mental health professional or call your local emergency\nservices immediately."

        dispatcher.utter_message(message)

        return []


#.................ConversationHistory.....................................................    
class ActionSaveConversationHistory(Action):
    def name(self) -> Text:
        return "action_save_conversation_history"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conversation_history = []
        for event in tracker.events:
            if event.get("event") == "user":
                conversation_history.append({"user": event.get("text")})
            elif event.get("event") == "bot":
                conversation_history.append({"bot": event.get("text")})

        with open("conversation_history.txt", "a") as f:
            f.write(json.dumps(conversation_history))
            f.write("\n")

        return []
    
#............................Sentimental analysis...................................................

class ActionEmotion(Action): #finalllll

  def name(self) -> Text:
    return "action_emotion"

  def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        text = str(tracker.latest_message["text"])

        emotion = NRCLex(text)

        dispatcher.utter_message(text=" The affect dictionary of the emotions detected are {} ".format(emotion.affect_dict))
        dispatcher.utter_message(text=" The raw emotion scores detected are {} ".format(emotion.raw_emotion_scores))
        dispatcher.utter_message(text=" The top emotions detected are  {} ".format(emotion.top_emotions))
        dispatcher.utter_message(text=" The affect frequencies detected are {} ".format(emotion.affect_frequencies))

        return []

#.......................................Snack,water & Gun (games)..............................................
class ActionPlaySWG(Action):
   
    def name(self) -> Text:
        return "action_play_swg"
 
    def computer_choice(self):
        generatednum = random.randint(1,3)
        if generatednum == 1:
            computerchoice = "snake"
        elif generatednum == 2:
            computerchoice = "water"
        elif generatednum == 3:
            computerchoice = "gun"
       
        return(computerchoice)
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # play snake, water & gun
        user_choice = tracker.get_slot("choice")
        dispatcher.utter_message(text=f"You chose {user_choice}")
        comp_choice = self.computer_choice()
        dispatcher.utter_message(text=f"The computer chose {comp_choice}")
 
        if user_choice == "snake" and comp_choice == "water":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "snake" and comp_choice == "gun":
            dispatcher.utter_message(text="The computer won this round.")
        elif user_choice == "water" and comp_choice == "gun":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "water" and comp_choice == "snake":
            dispatcher.utter_message(text="The computer won this round.")
        elif user_choice == "gun" and comp_choice == "snake":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "gun" and comp_choice == "water":
            dispatcher.utter_message(text="The computer won this round.")
        else:
            dispatcher.utter_message(text="It was a tie!")
        return[]
    
#.......................................Psychatrist Data..............................................
import pandas as pd
import random
class PsychiatristDataAction(Action):

    def name(self) -> str:
        return "action_suggest_psychiatrist"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        # Provide the file path
        file_path = "C:\\Users\\Kalpe\\OneDrive\\Desktop\\last\\actions\\Psychatrist Dataa.xlsx"

        # Read Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # # Load the Excel file into a DataFrame
        # df = pd.read_excel(df = pd.read_excel("C:\\Users\\Kalpe\\Desktop\\jsk\\actions\\Psychatrist Data.xlsx"))

        # Get 3 random rows from the DataFrame
        random_rows = df.sample(n=3)

        # Extract the values from the random rows
        random_data = random_rows.to_dict(orient="records")

        # Format the response for the chatbot
        response = "Here are the Details of the available Psychiatrist in Ahmedabad:\n"
        for data in random_data:
            response += f"\nName: {data['NAME']}\nAddress: {data['ADDRESS']}\nContact: {data['CONTACT']}\nExperience: {data['EXPERIENCE']}\nServices: {data['SERVICES']}\n"

        # Send the response to the user
        dispatcher.utter_message(text=response)

        return []


#.................show image..............
class ShowImage(Action):

    def name(self) -> Text:
        return "action_show_image"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_unique_qualities")

        return []
    
#...............wellness form ............
from rasa_sdk.forms import FormValidationAction

class ValidateHealthForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_health_form"

    async def validate_confirm_exercise(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value:
            return {"confirm_exercise": True}
        else:
            return {"exercise": "None", "confirm_exercise": False}

class ActionSubmitResults(Action):
    def name(self) -> Text:
        return "action_submit_results"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        confirm_exercise = tracker.get_slot("confirm_exercise")
        exercise = tracker.get_slot("exercise")
        sleep = tracker.get_slot("sleep")
        stress = tracker.get_slot("stress")
 # diet = tracker.get_slot("diet")
        goal = tracker.get_slot("goal")

        # Display slot values
        # slot_values = tracker.current_slot_values()
        # dispatcher.utter_message(f"Here are your responses: {slot_values}")

        dispatcher.utter_message("Thanks, your answers have been recorded!")
        return []

