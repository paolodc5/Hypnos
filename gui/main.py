# gui/main.py
import customtkinter as ctk
from gui.login import LoginWindow
from gui.doctor.doctor_app import DoctorApp
from models.doctor import Doctor

def start_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    # start_gui()
    # Create a dummy or real Doctor object as needed
    doctor = Doctor(doctor_id=3, name="Alice", surname="Carrol", specialty="Neurologist", email="alice@hypnos.com", password="pass123")

    app = DoctorApp(doctor)
    app.mainloop()