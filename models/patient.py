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
                 birth_date: str, 
                 age: int,
                 gender: str,
                 phone_number: str,
                 fiscal_code: str,
                 doctor_id: Optional[int] = None,
                 email: Optional[str] = None

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
        self.email = email  

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

    def load_prescriptions(self):
        from services.patient_services import get_prescriptions
        self.prescriptions = get_prescriptions(self.patient_id)

    def load_notes(self):
        from services.patient_services import get_patient_notes
        from services.patient_services import get_doctor_notes
        self.patient_notes = get_patient_notes(self.patient_id)
        self.doctor_notes = get_doctor_notes(self.patient_id, self.doctor_id)

    def get_doctor_notes(self):
        from services.patient_services import get_doctor_notes
        return get_doctor_notes(self.patient_id, self.doctor_id)

    def get_patient_notes(self):
        from services.patient_services import get_patient_notes
        return get_patient_notes(self.patient_id)

    def add_note(self, content):
        from services.patient_services import add_patient_note
        add_patient_note(self.patient_id, content)

    def update_note(self, note_id, new_content=None, delete=False):
        from services.patient_services import update_patient_note
        from services.patient_services import delete_patient_note
        if delete:
            delete_patient_note(note_id)
        else:
            update_patient_note(note_id, new_content)

    def load_sleep_records(self):
        from services.patient_services import get_sleep_records
        self.sleep_records = get_sleep_records(self.patient_id)

    def __str__(self):
        return f"Patient({self.patient_id}, {self.name}, {self.email})"
    
    def get_doctor(self):
        from services.patient_services import get_doctor_by_id
        """Fetch the assigned doctor from the database."""
        if not self.doctor_id:
            return None
        return get_doctor_by_id(self.doctor_id)
    
    def save(self):
        from services.patient_services import update_patient_profile
        update_patient_profile(
            self.patient_id,
            self.name,
            self.surname,
            self.birth_date,
            self.age,
            self.gender,
            self.fiscal_code,
            self.email,
            self.phone_number
        )

    def reload_from_db(self):
        from services.patient_services import get_patient_by_id
        fresh = get_patient_by_id(self.patient_id)
        if fresh:
            self.__dict__.update(fresh.__dict__)



