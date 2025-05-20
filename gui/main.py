# gui/main.py
import customtkinter as ctk
from gui.login import LoginWindow
from gui.doctor.doctor_app import DoctorApp
from models.doctor import Doctor
from services.doctor_services import get_doctor_by_id

def start_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    # start_gui()
    # Create a dummy or real Doctor object as needed
    #doctor = Doctor(doctor_id=3, name="Alice", surname="Carrol", specialty="Neurologist", email="alice@hypnos.com", password="pass123")
    doctor = get_doctor_by_id(3)  # Dr. Vanessa Bautista (3) connected to patient id=5 (Darius Barker)

    if doctor is None:
        print("No doctor found with that ID.")
    else:
        app = DoctorApp(doctor)
        app.mainloop()