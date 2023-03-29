class InputEvent:
    """
    The structure of the event data that Amazon Lex passes to your Lambda function.
    """

    def __init__(self, event):
        self.event = event
        # A map of slot names to slot values
        self.slots = self.event['currentIntent']['slots']

    # Getter Methods
    def getIntentName(self) -> str:
        """
        Gets the intent name from the request.

        Returns:
            str: The intent name.

        """
        return self.event['currentIntent']['name']

    def getSlotDetails(self, slotName) -> dict:
        """
        Gets the value of a slot from the request.

        Args:
            slotName (str): The name of the slot.

        Returns:
            dict: The dictionary containing the value of the slot: OriginalValue, 
        """
        return self.slots[slotName]
