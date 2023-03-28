import json
import datetime
import time


class InputValidator:
    """
    Provides methods for validating the input 
    from the user for each slot type.
    """

    # Class variables
    validApplianceBrands = ["lg", "samsung", "ge"]
    validApplianceTypes = ["washer", "dryer",
                           "refrigerator", "stove", "dishwasher"]

    def __init__(self, slots):
        # Initialize the slots
        self.slots = slots

    # Getter methods
    def getSlotOriginalValue(self, slotName: str) -> str:
        """
        Gets the original value of the slot.

        Args:
            slotName (str): The name of the slot.

        Returns:
            str: The original value of the slot.
        """

        return self.slots[slotName]['value']["originalValue"]

    def getSlotInterpretedValue(self, slotName: str) -> str:
        """
        Gets the interpreted value of the slot.

        Args:
            slotName (str): The name of the slot.

        Returns:
            str: The interpreted value of the slot.
        """
        return self.slots[slotName]['value']['interpretedValue']

    def getSlotResolvedValue(self, slotName: str) -> list:
        """
        Gets the resolved value of the slot.

        Args:
            slotName (str): The name of the slot.

        Returns:
            list: The list of resolved values.
        """
        return self.slots[slotName]['value']['resolvedValues']

    def getSlotValue(self, slotName: str) -> str:
        """
        Gets the value of the slot.

        Args:
            slotName (str): The name of the slot.

        Returns:
            str: The value of the slot.
        """
        return self.slots[slotName]['value']

    # Setter methods
    def setInvalidResponseForSlot(self, slotName: str) -> dict:
        """
        Sets the invalid response for the slot.

        Args:
            slotName (str): The name of the slot.

        Returns:
            dict: A dictionary containing the validation result.
        """
        return {
            'isValid': False,
            'violatedSlot': slotName,
            'message': f'The value for the {slotName} is not covered and therefore invalid.'
        }

    # Validation methods
    def checkDNE(self, slotName: str) -> dict:
        """
        Checks if the slot is not provided.

        Args:
            slotName (str): The name of the slot to check.

        Returns:
            dict: A dictionary containing the validation result.
        """
        if not self.slots[slotName]:
            return {
                'isValid': False,
                'violatedSlot': slotName,
                'message': 'The value for the slot is not provided.'
            }

    def checkAllSlotsForDNE(self) -> dict:
        """
        Checks if all slots are not provided.

        Returns:
            dict: A dictionary containing the validation result.
        """
        for slotName in self.slots:
            return self.checkDNE(slotName)
        return {'isValid': True}

    def validateApplianceBrand(self) -> dict:
        """
        Validates the appliance brand.

        Returns:
            dict: A dictionary containing the validation result.
        """
        applianceBrand = self.getSlotOriginalValue('applianceBrand')

        if applianceBrand.lower() not in self.validApplianceBrands:
            self.setInvalidResponseForSlot('applianceBrand')

    def validateApplianceType(self) -> dict:
        """
        Validates the appliance type.

        Returns:
            dict: A dictionary containing the validation result.
        """

        applianceType = self.getSlotOriginalValue('applianceType')

        if applianceType.lower() not in self.validApplianceTypes:
            self.setInvalidResponseForSlot('applianceType')

    def isValid_date(self, date: str) -> bool:
        """
        Checks if the date is valid.

        Args:
            date (str): The date to check.

        Returns:
            bool: True if the date is valid, False otherwise.
        """
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validateAllSlots(self) -> dict:
        """
        Validates all the slots.

        Returns:
            dict: A dictionary containing the validation result.
        """
        if self.checkAllSlotsForDNE():
            return self.checkAllSlotsForDNE()

        if self.validateApplianceBrand():
            return self.validateApplianceBrand()

        if self.validateApplianceType():
            return self.validateApplianceType()

        return {'isValid': True}

    def validateOneSlot(self, slotName: str) -> dict:
        """
        Validates one slot.

        Args:
            slotName (str): The name of the slot to validate.

        Returns:
            dict: A dictionary containing the validation result.
        """
        if self.checkDNE(slotName):
            return self.checkDNE(slotName)

        if slotName == 'applianceBrand':
            return self.validateApplianceBrand()

        if slotName == 'applianceType':
            return self.validateApplianceType()

        return {'isValid': True}


class LambdaHandler:
    """
    Handles the Lambda function invocation.
    """

    def __init__(self, event, context):
        self.event = event  # Lambda runetime converts the JSON input to a Python dictionary
        self.context = context  # Lambda runetime provides the context object

        # Initialize the input validator
        self.inputValidator = InputValidator(self.getSlots())

    # Getter methods

    def getSlots(self) -> dict:
        """
        Gets the slots.

        Returns:
            dict: The slots.
        """
        print(self.event['sessionState']['intent']['slots'])

        return self.event['sessionState']['intent']['slots']

    def getIntent(self) -> dict:
        """
        Gets the intent.

        Returns:
            dict: The intent.
        """

        return self.event['sessionState']['intent']['name']

    def getContext(self):
        """
        Gets the context object.

        Returns:
            context: The context object.
        """

        return self.context

    # Handler methods

    def validateEvent(self, slotName: str) -> dict:
        """
        Validates the event.

        Returns:
            dict: A dictionary containing the validation result.
        """

        return self.inputValidator.validateOneSlot(slotName=slotName)

    def processDialogCodeHook(self) -> dict:
        """
        Processes the dialog code hook.

        Returns:
            dict: A dictionary containing the response.
        """
        slots = self.getSlots()

        # TODO: Validate the slots in real time.
        validation = self.validateEvent(slotName=slotName)

        # If the validation is not valid, return the validation result.
        # TODO: Add runetimehints
        if not validation['isValid']:
            # Define the slot to elicit from the user and send the message.
            return self.elicitSlot(validation['violatedSlot'], validation['message'])

        # If the validation is valid, delegate Lex to decide the next action.
        return self.delegate()

    def processFulfillmentCodeHook(self) -> dict:
        """
        Processes the fulfillment code hook.
        Adds the booking request to the database.

        Returns:
            dict: A dictionary containing the response.
        """
        intent = self.getIntent()
        slots = self.getSlots()
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }
            },
            "messages": [{
                "contentType": "PlainText",
                "content": "Thank you I have placed your appointment."
            }]
        }

    # TODO: Make dispatch method to be able to handle multiple intents
    def dispatch(self) -> dict:
        """
        Processes the invocation source.

        Returns:
            dict: A dictionary containing the response.
        """

        invocationSource = self.event["invocationSource"]

        if invocationSource == "DialogCodeHook":
            return self.processDialogCodeHook()
        elif invocationSource == "FulfillmentCodeHook":
            return self.processFulfillmentCodeHook()

    def delegate(self) -> dict:
        """
        Delegates the intent to Lex.

        Returns:
            dict: A dictionary containing the response.
        """

        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'Delegate'
                }
            },
            "messages": [{
                "contentType": "PlainText",
                "content": "Thank you I have placed your appointment."
            }]
        }

    def elicitSlot(self, slotName: str, message: str) -> dict:
        """
        Elicits a slot from the user.

        Args:
            slotName (str): The name of the slot.
            message (str): The message to send to the user.

        Returns:
            dict: A dictionary containing the response.
        """

        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'slotToElicit': slotName
                }
            },
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': message
                }
            ]
        }


def handler(event, context):
    """
    Handles the Lambda function invocation.

    Args:
        event (dict): The event.
        context (context): The context object.

    Returns:
        dict: A dictionary containing the response.
    """
    print(event)
    print(context)
    lambdaHandler = LambdaHandler(event, context)

    return lambdaHandler.dispatch()
