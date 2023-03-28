import json
import logging

from bookAppointment import BookAppointment


class LambdaHandler:
    def __init__(self, event, context):
        self.event = event
        self.context = context

    # Getter Methods
    def getIntentName(self) -> str:
        """
        Gets the intent name from the request.

        Returns:
            str: The intent name.

        """
        return self.event['sessionState']['intent']['name']

    def getSlotValue(self, slotName) -> str:
        """
        Gets the value of a slot from the request.

        Args:
            slotName (str): The name of the slot.

        Returns:
            str: The value of the slot.

        """
        return self.event['sessionState']['intent']['slots'][slotName]['value']

    # Dispatches the request to the appropriate handler for the intent.

    def dispatch():
        """
        Calls the appropriate intent handler based on the incoming request.
        """


def handler(event, context):
    lambdaHandler = LambdaHandler(event, context)
    return lambdaHandler.dispatch()
