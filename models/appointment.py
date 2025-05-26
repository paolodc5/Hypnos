# appointment.py

from typing import TYPE_CHECKING
from models.appointment_slot import AppointmentSlot

if TYPE_CHECKING:
    from models.doctor import Doctor
    from models.patient import Patient

class Appointment:
    def __init__(self, 
                 appointment_id: int = None, 
                 slot: "AppointmentSlot" = None, 
                 patient_id: str = None, 
                 doctor_id: str = None,
                 status: str = "pending", 
                 notes: str = None):
        
        if slot:
            # Check if the slot is valid and assigned to the patient
            if not slot.is_booked or slot.selected_by != patient_id:
                raise ValueError("Slot must be selected and booked by this patient to confirm the appointment")

            self.slot_id = slot.slot_id
            self.slot = slot  # Store the AppointmentSlot instance
        else:
            self.slot_id = None  # Can be set later after selecting a slot
        
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.status = status  # Default is "pending"
        self.notes = notes  # Optional notes

    def book_appointment(self):
        if self.status == "confirmed":
            raise Exception("Appointment already confirmed")
        
        if not self.slot_id:
            raise ValueError("No slot selected for the appointment")

        # Call the service function to insert the appointment into the database
        from services.patient_services import add_appointment
        appointment_id = add_appointment(self.slot_id, self.patient_id, self.doctor_id, self.status, self.notes)
        
        self.appointment_id = appointment_id
        self.status = "confirmed"  # Update the status
        self.slot.mark_as_booked()  # Mark the slot as booked

    def cancel_appointment(self):
        if self.status != "confirmed":
            raise Exception("Appointment is not confirmed yet")
        
        # Call the service function to update the appointment status in the database
        from services.patient_services import cancel_appointment
        cancel_appointment(self.appointment_id)

        self.slot.cancel_booking()  # Free the slot
        self.status = "cancelled"
