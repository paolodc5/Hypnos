from typing import List, TYPE_CHECKING
from datetime import date, time

class ForumQuestion:
    def __init__(self, user_type: str, user_id: int, request_id: int, request: str, filling_date: date, filling_time: time, taken=False):
        self.user_type = user_type # Type of user submitting the request, e.g. "Doctor" or "Patient"
        self.user_id = user_id # Identifier of the user (can be different types)
        self.request_id = request_id # Unique request identifier within the forum
        self.request = request # The text of the request/question
        self.filling_date = filling_date # Date when the form was filled, e.g. "2024-05-16"
        self.filling_time = filling_time # Time when the form was filled, e.g. "10:00"
        self.taken = taken # Has the request been taken/handled - default is False

    def mark_as_taken(self):
        """Mark this request as handled."""
        self.taken = True
               