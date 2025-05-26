# gui/main.py
import customtkinter as ctk
from gui.patient.patient_app import PatientApp
from gui.loginall import LoginWindow
from models.patient import Patient
from services.patient_services import get_patient_by_id

def start_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    # start_gui()
    # Create a dummy or real Patient object as needed
    
    #patient = Patient(patient_id=102, name="Maria", surname="Rossi", birth_date="1995-07-05", age=29,
    #    gender="F", phone_number="0987654321", fiscal_code="MRARSS95", doctor_id=1)

    # Use a real patient from the database
    patient = get_patient_by_id(5) # Darius Barker (5) connected to doctor 3 (Vanessa Bautista)

    if patient is None:
        print("No patient found with that ID.")
    else:
        app = PatientApp(patient)
        app.geometry("1200x800")
        app.mainloop()