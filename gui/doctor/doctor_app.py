# gui/doctor/doctor_app.py
import customtkinter as ctk
from models.doctor import Doctor
from gui.doctor.sidebar import Sidebar
from gui.doctor.home_tab import HomeTab
from gui.doctor.patient_tab import PatientTab
# from gui.doctor.prescription_tab import PrescriptionTab
# etc.

class DoctorApp(ctk.CTk):
    def __init__(self, doctor: Doctor):
        super().__init__()
        self.title("Hypnos - Doctor Dashboard")
        self.geometry("1000x600")
        self.doctor = doctor
        self.doctor.load_patients()

        self.setup_layout()
        self.show_home()

    def setup_layout(self):
        self.sidebar = Sidebar(self, command_callback=self.handle_sidebar_command)
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def handle_sidebar_command(self, page: str):
        self.clear_content()
        match page:
            case "home":
                self.show_home()
            case "patients":
                self.show_patients()
            # case "prescriptions":
            #     self.show_prescriptions()

    def show_home(self):
        HomeTab(self.content_frame, self.doctor).pack(fill="both", expand=True)

    def show_patients(self):
        PatientTab(self.content_frame, self.doctor).pack(fill="both", expand=True)
