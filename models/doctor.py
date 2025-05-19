from typing import List, TYPE_CHECKING
from datetime import datetime
from services.patient_services import get_patients_by_doctor
from services.doctor_services import load_appointment_slots_by_doctor, load_appointments_by_doctor


if TYPE_CHECKING:
    from models.patient import Patient
    from models.prescription import Prescription
    from models.note import Note
    from models.sleep_record import SleepRecord
    from models.questionnaire import Questionnaire
    from models.appointment import Appointment
    from models.appointment_slot import AppointmentSlot



class Doctor:
    def __init__(self, doctor_id: int, name: str, surname:str, specialty: str, email: str, password: str):
        self.doctor_id = doctor_id
        self.name = name
        self.surname = surname
        self.specialty = specialty
        self.email = email
        self.password = password
        self.patients: List["Patient"] = []
        self.appointment_slots: List["AppointmentSlot"] = []
        self.appointments: List["Appointment"] = []

    # PATIENT MANAGEMENT
    def assign_patient(self, patient: "Patient"):
        """Assign a patient to the doctor."""
        self.patients.append(patient)

    def view_patient_sleep_data(self, patient: "Patient") -> List["SleepRecord"]:
        """View sleep data for a specific patient."""
        return patient.get_sleep_records()

    def view_patient_questionnaires(self, patient: "Patient") -> List["Questionnaire"]:
        """View questionnaires filled by a specific patient."""
        return patient.get_questionnaires()

    def write_note(self, patient_id, content):
        """Write a note for a specific patient."""
        from services.doctor_services import write_note
        write_note(patient_id, self.doctor_id, content)

    def edit_note(self, note_id, new_content):
        """Edit an existing note."""
        from services.doctor_services import update_note
        update_note(note_id, new_content, self.doctor_id)

    def delete_note(self, note_id):
        """Delete a note."""
        from services.doctor_services import delete_note
        delete_note(note_id, self.doctor_id)

    def get_notes_for_patient(self, patient_id):
        """Get notes for a specific patient."""
        from services.doctor_services import get_notes_for_patient
        return get_notes_for_patient(patient_id, self.doctor_id)

    def write_prescription(self, patient: "Patient", prescription: "Prescription"):
        """Write a prescription for a specific patient."""
        patient.prescriptions.append(prescription)

    def edit_prescription(self, prescription: "Prescription", new_instructions: str):
        """Edit an existing prescription."""
        prescription.instructions = new_instructions
        prescription.last_modified = datetime.now()

    # APPOINTMENT MANAGEMENT
    def propose_appointment_slot(self, start_time: datetime, end_time: datetime) -> "AppointmentSlot":
        """Propose a new appointment slot."""
        slot = AppointmentSlot(slot_id=None, doctor=self, start_time=start_time, end_time=end_time)
        self.appointment_slots.append(slot)
        return slot

    def confirm_appointment(self, appointment: "Appointment"):
        """Confirm an appointment."""

        if appointment.status != "pending": # Check if the appointment is in 'pending' status
            raise Exception("Appointment must be in 'pending' status to confirm")
        
        appointment.status = "confirmed"
        appointment.slot.is_booked = True
    
    def load_patients(self):
        self.patients = get_patients_by_doctor(self.doctor_id)

    def load_appointment_slots(self):
        self.appointment_slots = load_appointment_slots_by_doctor(self.doctor_id)

    def load_appointments(self):
        self.appointments = load_appointments_by_doctor(self.doctor_id)

    def __str__(self):
        return f"Doctor({self.doctor_id}, {self.name}, {self.specialty})"
