# appointment.py
from models.doctor import Doctor
from models.patient import Patient
from models.appointment_slot import AppointmentSlot

class Appointment:
    def __init__(self, 
                 appointment_id: int, 
                 slot: AppointmentSlot, 
                 patient_id: str, 
                 doctor_id: str,
                 confirmed: bool = False):
        # logical check to ensure the appointment is linked to a valid slot and patient
        if not slot.is_booked or slot.selected_by != patient_id:
            raise ValueError("Slot must be selected and booked by this patient to confirm the appointment")

        self.appointment_id = appointment_id
        self.slot = slot
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.confirmed = confirmed

    def confirm(self):
        if self.confirmed:
            raise Exception("Appointment already confirmed")
        self.confirmed = True

    def cancel(self):
        if not self.confirmed:
            raise Exception("Appointment is not confirmed yet")
        self.slot.cancel_booking()
        self.confirmed = False
