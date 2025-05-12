from datetime import datetime
from typing import Optional

class AppointmentSlot:
    def __init__(self, 
                 slot_id: int, 
                 doctor_id: str, 
                 start_time: datetime, 
                 end_time: datetime):
        self.slot_id = slot_id
        self.doctor_id = doctor_id  # It's clearer to use "_id" for foreign keys
        self.start_time = start_time
        self.end_time = end_time
        self.selected_by: Optional[str] = None  # Patient ID, if selected
        self.is_booked: bool = False

    def select_slot(self, patient_id: str):
        """Patient selects this slot, but appointment not confirmed yet."""
        if self.is_booked:
            raise Exception("Slot already booked")
        self.selected_by = patient_id

    def mark_as_booked(self):
        """Finalize booking (after confirmation)."""
        if not self.selected_by:
            raise Exception("Slot must be selected before booking")
        self.is_booked = True

    def cancel_booking(self):
        """Cancel the selection and mark it as free again."""
        self.selected_by = None
        self.is_booked = False

