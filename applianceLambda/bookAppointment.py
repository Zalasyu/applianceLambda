import datetime
import logging


class BookAppointment:

    def __init__(self, event):
        self.event = event
        # A map of slot names to slot values
        self.slots = self.event['currentIntent']['slots']

    # Getter Methods

    # Setter Methods

    # Helper Methods

    # Handler Methods

    def makeAppointment(self):
        """
        Handles the BookAppointment intent.
        """
