# this file implements the Patient class like in the class diagram we have defined
# and the methods to interact with the database and the application.
from typing import List, Optional
from models.questionnaire import Questionnaire
from models.prescription import Prescription
from models.sleep_record import SleepRecord
from models.note import Note
from models.appointment import Appointment

class Patient:
    def __init__(self, patient_id: int, name: str, email: str, birth_date: str, doctor_id: Optional[int] = None):
        self.patient_id = patient_id
        self.name = name
        self.email = email
        self.birth_date = birth_date
        self.doctor_id = doctor_id  # Assigned doctor
        self.questionnaires: List[Questionnaire] = []
        self.sleep_records: List[SleepRecord] = []
        self.prescriptions: List[Prescription] = []
        self.notes: List[Note] = []
        self.appointments: List[Appointment] = []

    def fill_questionnaire(self, questionnaire: Questionnaire):
            self.questionnaires.append(questionnaire)
            questionnaire.submit()

    def add_sleep_record(self, sleep_record: SleepRecord):
        self.sleep_records.append(sleep_record)

    def view_prescriptions(self) -> List[Prescription]:
        return self.prescriptions

    def view_notes(self) -> List[Note]:
        return self.notes

    def book_appointment(self, appointment: Appointment):
        self.appointments.append(appointment)

    def view_appointments(self) -> List[Appointment]:
        return self.appointments

    def __str__(self):
        return f"Patient({self.patient_id}, {self.name}, {self.email})"




