# this file implements the Patient class like in the class diagram we have defined
# and the methods to interact with the database and the application.
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.questionnaire import Questionnaire
    from models.prescription import Prescription
    from models.sleep_record import SleepRecord
    from models.note import Note
    from models.appointment import Appointment
    from models.appointment_slot import AppointmentSlot

class Patient:
    def __init__(self, 
                 patient_id: str, 
                 name: str,
                 surname: str, 
                 email: None, 
                 birth_date: str, 
                 age: int,
                 gender: str,
                 phone_number: str,
                 fiscal_code: str,
                 doctor_id: Optional[int] = None,

                 ):
        self.patient_id = patient_id
        self.name = name
        self.surname = surname
        self.birth_date = birth_date
        self.doctor_id = doctor_id  # Assigned doctor
        self.age = age
        self.gender = gender
        self.phone_number = phone_number
        self.fiscal_code = fiscal_code

        # Lists to hold the patient's data
        self.questionnaires: List["Questionnaire"] = []
        self.sleep_records: List["SleepRecord"] = []
        self.prescriptions: List["Prescription"] = []
        self.notes: List["Note"] = []
        self.appointments: List["Appointment"] = []


    # Functions to handle patient data entry 
    def fill_questionnaire(self, questionnaire: "Questionnaire"):
            """Fill out a questionnaire."""
            self.questionnaires.append(questionnaire)
            questionnaire.submit()

    def add_sleep_record(self, sleep_record: "SleepRecord"):
        """Add a sleep record."""
        self.sleep_records.append(sleep_record)

    # Functions to retrieve patient prescription and note data
    def view_prescriptions(self) -> List["Prescription"]:
        """View prescriptions."""
        return self.prescriptions

    def view_notes(self) -> List["Note"]:
        """View notes."""
        return self.notes

    # Functions to manage appointments
    def book_appointment_slot(self, slot: "AppointmentSlot"):
        """Book an appointment slot."""
        slot.select_slot(self.id)

    def view_appointments(self) -> List["Appointment"]:
        """View all appointments."""
        return self.appointments
    
    # Functions to retrieve data for the doctor
    def get_questionnaires(self) -> List["Questionnaire"]:
        """Get all questionnaires filled by the patient."""
        return self.questionnaires

    def get_sleep_records(self) -> List["SleepRecord"]:
        """Get all sleep records of the patient."""
        return self.sleep_records

    def get_notes(self) -> List["Note"]:
        """Get all notes for the patient."""
        return self.notes
    
    def get_prescriptions(self) -> List["Prescription"]:
        """Get all prescriptions for the patient."""
        return self.prescriptions

    def __str__(self):
        return f"Patient({self.patient_id}, {self.name}, {self.email})"




