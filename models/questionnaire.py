from typing import Optional, List

class Questionnaire:
    def __init__(self, questionnaire_id: int, patient_id: int, doctor_id: int, date: str, score: int, notes: Optional[str] = None):
        self.questionnaire_id = questionnaire_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.questionnaire_score = score
        self.answers = List[int]  # List of answers to the questionnaire
        self.notes = notes  # Additional notes about the questionnaire

    def submit(self):
        # Logic to submit the questionnaire (e.g., save to database)
        pass

    def compute_score(self):
        # Logic to compute the score based on answers
        # The questionnaire considered is the ISI (Insomnia Severity Index)
        summary_score = sum(self.answers)
        if summary_score <= 7:
            self.questionnaire_score = 0
        elif summary_score <= 14:
            self.questionnaire_score = 1
        elif summary_score <= 21:
            self.questionnaire_score = 2
        elif summary_score <= 28:
            self.questionnaire_score = 3
        else:
            self.questionnaire_score = 4
        
        return self.questionnaire_score

    def __str__(self):
        return f"Questionnaire({self.questionnaire_id}, {self.patient_id}, {self.date})"