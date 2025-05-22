from typing import List, Optional
from models.forum_question import ForumQuestion
import services.ITtechnician_services as IT_services  # Your new service module
import datetime

class ITTechnician:
    def __init__(self, technician_id: int, name: str, email: str, phone_number: str, password: str):
        self.technician_id = technician_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.password = password  # Remember to hash passwords in production!

    # Fetch all forum questions (both taken and pending)
    def fetch_all_forum_questions(self) -> List[ForumQuestion]:
        return IT_services.get_all_forum_questions()

    # Fetch only pending forum questions (not taken yet)
    def fetch_pending_forum_questions(self) -> List[ForumQuestion]:
        return IT_services.get_pending_forum_questions()

    # Mark a forum question as taken (handled)
    def mark_question_taken(self, request_id: int) -> bool:
        return IT_services.mark_forum_question_as_taken(request_id)

    # Fetch a specific forum question by its request ID
    def get_forum_question(self, request_id: int) -> Optional[ForumQuestion]:
        return IT_services.get_forum_question_by_id(request_id)

    # Example method to simulate contacting the software developer
    def contact_software_developer(self, message: str):
        timestamp = datetime.datetime.now().isoformat()
        print(f"[{timestamp}] IT Technician {self.name} contacts Software Developer: {message}")

    # You can add system monitoring methods, e.g.:
    def check_system_status(self) -> str:
        # Placeholder for real system check logic
        return "System is operational."
    
    def __str__(self):
        return f"IT Technician(ID={self.technician_id}, Name={self.name}, Email={self.email})"
