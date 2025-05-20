# gui/doctor/doctor_app.py
import customtkinter as ctk
from models.doctor import Doctor
from gui.doctor.sidebar import Sidebar
from gui.doctor.home_tab import HomeTab
from gui.doctor.patient_tab import PatientTab
from gui.doctor.doctors_list_view import DoctorsListView

class DoctorApp(ctk.CTk):
    def __init__(self, doctor: Doctor):
        super().__init__()
        self.title("Hypnos - Doctor Dashboard")
        self.geometry("1100x650")
        self.doctor = doctor
        self.doctor.load_patients()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, command_callback=self.handle_sidebar_command)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.content_frame = ctk.CTkFrame(
            self, 
            fg_color="#ffffff", 
            corner_radius=10, 
            border_width=1,
            border_color="#d1d5db"
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        self.show_home()

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
            case "doctors":
                self.show_doctors_list()

    def show_home(self):
        HomeTab(self.content_frame, self.doctor).pack(fill="both", expand=True)

    def show_patients(self):
        PatientTab(self.content_frame, self.doctor).pack(fill="both", expand=True)

    def show_doctors_list(self):
        DoctorsListView(self.content_frame).pack(fill="both", expand=True)
