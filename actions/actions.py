from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import re
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import BotUttered
import sqlite3
from rasa_sdk.events import  SlotSet, AllSlotsReset 
from rasa_sdk.events import SlotSet

from rasa_sdk import Action, Tracker
# change this to the location of your SQLite file
path_to_db = "actions/example1.db"

class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get slots and save as tuple
        shoe = [(tracker.get_slot("color")), (tracker.get_slot("size"))]

        # place cursor on correct row based on search criteria
        cursor.execute("SELECT * FROM inventory WHERE color=? AND size=?", shoe)
        
        # retrieve sqlite row
        data_row = cursor.fetchone()

        if data_row:
            # provide in stock message
            dispatcher.utter_message(template="utter_in_stock")
            connection.close()
            slots_to_reset = ["size", "color"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            dispatcher.utter_message(template="utter_no_stock")
            connection.close()
            slots_to_reset = ["size", "color"]
            return [SlotSet(slot, None) for slot in slots_to_reset]

class SurveySubmit(Action):
    def name(self) -> Text:
        return "action_survey_submit"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_open_feedback")
        dispatcher.utter_message(template="utter_survey_end")
        return [SlotSet("survey_complete", True)]


class OrderStatus(Action):
    def name(self) -> Text:
        return "action_order_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # convert tuple to list
            data_list = list(data_row)

            # respond with order status
            dispatcher.utter_message(template="utter_order_status", status=data_list[5])
            connection.close()
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            connection.close()
            return []


class CancelOrder(Action):
    def name(self) -> Text:
        return "action_cancel_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # change status of entry
            status = [("cancelled"), (tracker.get_slot("email"))]
            cursor.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            connection.commit()
            connection.close()

            # confirm cancellation
            dispatcher.utter_message(template="utter_order_cancel_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            connection.close()
            return []


class ReturnOrder(Action):
    def name(self) -> Text:
        return "action_return"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # change status of entry
            status = [("returning"), (tracker.get_slot("email"))]
            cursor.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            connection.commit()
            connection.close()

            # confirm return
            dispatcher.utter_message(template="utter_return_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            connection.close()
            return []

class GiveName(Action):
    def name(self) -> Text:
        return "action_give_name"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        evt = BotUttered(
            text = "my name is bot? idk", 
            metadata = {
                "nameGiven": "bot"
            }
        )

        return [evt]
    
# Take order 
class TakeOrder(Action):
    def name(self) -> Text:
        return "action_take_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        try:
            # connect to DB
            connection = sqlite3.connect(path_to_db)
            cursor = connection.cursor()

            # get order details
            order_email = tracker.get_slot("email")
            order_address = tracker.get_slot("address")
            order_phone = tracker.get_slot("phone")
            order_quantity = tracker.get_slot("quantity")
            order_product = tracker.get_slot("product")
            order_name= tracker.get_slot("name")
            
            # insert new order into the database
            cursor.execute("INSERT INTO dummy(order_name, order_email, order_address, order_phone, order_quantity, order_product) VALUES (?, ?, ?, ?, ?, ?)", (order_name,order_email, order_address, order_phone, order_quantity, order_product))
            connection.commit()

            # confirm order
            dispatcher.utter_message(template="utter_order_confirm")

            connection.close()
            return []
        except Exception as e:
            print (e.message, e.args)
            connection.close()
            return []

class UtterDefaultFallback(Action):

    def name(self) -> Text:
        return "utter_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Sorry, I didn't understand. Could you please rephrase that?")

        return []
    
class ActionDeactivateLoop(Action):
    def name(self) -> Text:
        return "action_deactivate_loop"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("active_loop", None)]
    
class ValidateOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_order_form"

    async def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if re.match(email_regex, slot_value):
            return {"email": slot_value}
        else:
            dispatcher.utter_message(text="The email address is not valid. Please enter a valid email address.")
            return {"email": None}

    async def validate_quantity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if slot_value > 0:
            return {"quantity": slot_value}
        else:
            dispatcher.utter_message(text="Please enter a positive quantity.")
            return {"quantity": None}