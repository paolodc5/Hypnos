import customtkinter as ctk
from models.patient import Patient
import os
from PIL import Image
from gui.patient.views.home_view import HomeView
from gui.patient.views.profile_view import ProfileView
from gui.patient.views.prescriptions_view import PrescriptionsView
from gui.patient.views.doctor_view import DoctorView
from gui.patient.views.sleep_records_view import SleepRecordsView
from gui.patient.views.questionnaires_view import QuestionnairesView
from gui.patient.views.notes_view import NotesView
from gui.patient.views.faq_view import FAQView

class PatientApp(ctk.CTk):
    def __init__(self, patient: Patient):
        super().__init__()
        self.title("Hypnos - Patient Dashboard")
        self.geometry("1100x900")
        self.patient = patient

        self.setup_gui()

        # Instantiate views
        self.home_view = HomeView(self)
        self.profile_view = ProfileView(self)
        self.prescriptions_view = PrescriptionsView(self)
        self.doctor_view = DoctorView(self)
        self.sleep_records_view = SleepRecordsView(self)
        self.questionnaires_view = QuestionnairesView(self)
        self.notes_view = NotesView(self)
        self.faq_view = FAQView(self)

        self.show_home()

    def setup_gui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.sidebar = ctk.CTkFrame(self, width=240, fg_color="#0D1B2A", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self, fg_color="#1B263B")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), "../images/Hypnos_Logo.png")
        logo_image = ctk.CTkImage(Image.open(logo_path), size=(100, 100))
        ctk.CTkLabel(self.sidebar, image=logo_image, text="", bg_color="transparent").pack(pady=(30, 10))

        ctk.CTkLabel(
            self.sidebar,
            text="HYPNOS",
            font=("Helvetica", 22, "bold"),
            text_color="#F0EDEE"
        ).pack(pady=(0, 20))

        button_style = {
            "width": 180,
            "corner_radius": 20,
            "font": ("Helvetica", 16, "bold"),
            "fg_color": "#3366cc",
            "hover_color": "#66d9cc",
        }

        ctk.CTkButton(self.sidebar, text="Home", command=self.show_home, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="My Profile", command=self.show_profile, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Prescriptions", command=self.show_prescriptions, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Doctor", command=self.show_doctor_profile, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Sleep Records", command=self.show_sleep_records, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Questionnaires", command=self.show_questionnaires, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Notes", command=self.show_notes, **button_style).pack(pady=8)
        
        ctk.CTkFrame(self.sidebar, fg_color="transparent", height=1).pack(expand=True, fill="both")
        ctk.CTkButton(self.sidebar, text="FAQ", command=self.show_faq, **button_style).pack(pady=(0, 8))

        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar, values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
            width=180, fg_color="#3366cc", corner_radius=20,
            font=("Helvetica", 14, "bold")
        )
        self.appearance_mode_menu.pack(pady=(0, 30))

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # Navigation methods
    def show_home(self):
        self.home_view.show()
    def show_profile(self):
        self.profile_view.show()
    def show_prescriptions(self):
        self.prescriptions_view.show()
    def show_doctor_profile(self):
        self.doctor_view.show()
    def show_sleep_records(self):
        self.sleep_records_view.show()
    def show_questionnaires(self):
        self.questionnaires_view.show()
    def show_notes(self):
        self.notes_view.show()
    def show_faq(self):
        self.faq_view.show()