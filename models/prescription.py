from typing import List, Optional


class Prescription:    
    def __init__(self, prescription_id: str, 
                 patient_id: str, 
                 doctor_id: str, 
                 treatm_type: str, 
                 prescr_date: str,
                 content: str):
        self.prescription_id = prescription_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.treatm_type = treatm_type
        self.precr_date = prescr_date
        self.content = content


    def edit_prescription(self, content: str):
        self.content = content
    



