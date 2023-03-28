import datetime
import logging


class BookAppointment:

    def __init__(self, event):
        self.event = event
        self.slots = self.event['sessionState']['intent']['slots']
