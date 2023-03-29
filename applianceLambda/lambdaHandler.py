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
        return self.event['currentIntent']['name']

    # Dispatches the request to the appropriate handler for the intent.

    def dispatch(self):
        """
        Calls the appropriate intent handler based on the incoming request.
        """
        intent_name = self.getIntentName()

        if intent_name == 'BookAppointment':
            bookAppointment = BookAppointment(self.event)
            return bookAppointment.makeAppointment()
        # elif (Add more intents here):
        raise Exception('Intent with name ' + intent_name + ' not supported')


def handler(event, context):
    lambdaHandler = LambdaHandler(event, context)
    return lambdaHandler.dispatch()
