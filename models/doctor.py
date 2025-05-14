from typing import List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from models.patient import Patient
    from models.prescription import Prescription
    from models.note import Note
    from models.sleep_record import SleepRecord
    from models.questionnaire import Questionnaire
    from models.appointment import Appointment
    from models.appointment_slot import AppointmentSlot


class Doctor:
    def __init__(self, doctor_id: int, name: str, specialty: str, email: str, password: str):
        self.doctor_id = doctor_id
        self.name = name
        self.specialty = specialty
        self.email = email
        self.password = password
        self.patients: List["Patient"] = []
        self.appointment_slots: List["AppointmentSlot"] = []

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

    def write_note(self, patient: "Patient", note: "Note"):
        """Write a note for a specific patient."""
        patient.notes.append(note)

    def edit_note(self, note: "Note", new_content: str):
        """Edit an existing note."""
        note.content = new_content
        note.last_modified = datetime.now()

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

    def __str__(self):
        return f"Doctor({self.doctor_id}, {self.name}, {self.specialty})"
