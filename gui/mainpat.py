# gui/main.py
import customtkinter as ctk
from gui.loginpat import LoginWindow
from gui.patient.patient_app import PatientApp
from models.patient import Patient

def start_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    # start_gui()
    # Create a dummy or real Patient object as needed
    patient = Patient(
        patient_id=102,
        name="Maria",
        surname="Rossi",
        birth_date="1995-07-05",
        age=29,
        gender="F",
        phone_number="0987654321",
        fiscal_code="MRARSS95",
        doctor_id=1
    )

    app = PatientApp(patient)
    app.geometry("1200x700")
    app.mainloop()