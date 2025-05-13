from datetime import datetime

class Note:
    def __init__(self, 
                 note_id: str, 
                 patient_id: str, 
                 doctor_id: str, 
                 content: str, 
                 date: datetime):
        self.note_id = note_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.content = content
        self.date = date

    def edit_note(self, new_content: str):
        self.content = new_content
        self.date = datetime.now()  # Updates timestamp upon editing
