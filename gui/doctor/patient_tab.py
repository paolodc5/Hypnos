# gui/doctor/patient_tab.py
import customtkinter as ctk
from models.doctor import Doctor
from gui.doctor.scrollable_list_frame import ScrollableListFrame
from gui.doctor.patient_selection_frame import PatientSelectionFrame
from gui.doctor.administration_frame import AdministrationFrame

class PatientTab(ctk.CTkFrame):
    def __init__(self, master, doctor: Doctor):
        super().__init__(master, fg_color=("#f8fafc", "#222c3c"), corner_radius=16)
        self.doctor = doctor
        self.selected_patient = ctk.StringVar()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=8)
        self.grid_columnconfigure(0, weight=1)

        self.dropdown_frame = PatientSelectionFrame(self, doctor=self.doctor, patients=self.doctor.patients, command_callback=self.show_info)
        self.dropdown_frame.configure(fg_color='transparent')
        self.dropdown_frame.grid(row=0, column=0, padx=(30, 30), pady=(15, 0), sticky="nsew")

        self.info_frame = InfoFrame(self)
        self.info_frame.grid(row=1, column=0, padx=(30, 30), pady=(15, 0), sticky="nsew")

        self.segmented_bar = AdministrationFrame(self)
        self.segmented_bar.grid(row=2, column=0, padx=(30, 30), pady=(15, 30), sticky="nsew")

    def show_info(self, patient):
        self.info_frame.show_info(patient)
        self.segmented_bar.set_patient(patient)


class InfoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=("#eaf0fb", "#1a2233"), corner_radius=12)
        self.configure(fg_color="#f5f7fa", corner_radius=12)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)

    def show_info(self, patient):
        for widget in self.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            self, 
            text="👤 Patient Information", 
            font=("Arial", 18, "bold"), 
            text_color="#1e3a8a"
            ).grid(row=0, column=0, padx=20, pady=(20, 8), sticky="w")
        
        for i, text in enumerate([
            f"Name: {patient.name} {patient.surname}",
            f"Age: {patient.age}",
            f"Phone: {patient.phone_number}",
            f"Fiscal Code: {patient.fiscal_code}"
            ]):
            ctk.CTkLabel(
                self, 
                text=text, 
                font=("Arial", 14), 
                text_color="#1e293b"
            ).grid(row=i+1, column=0, padx=20, pady=2, sticky="w")



