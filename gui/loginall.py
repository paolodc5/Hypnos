# gui/loginall.py
import customtkinter as ctk
from PIL import Image
import os
from gui.doctor.doctor_app import DoctorApp
from gui.patient.patient_app import PatientApp
from services.auth_service import authenticate_doctor, authenticate_patient
from gui.registrationpat import AddPatientDialog
from gui.registrationdoc import AddDoctorDialog

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hypnos - Login")
        self.geometry("900x700")
        self.configure(bg_color="#121927")  # Main background

        # --- Background image ---
        bg_path = os.path.join(os.path.dirname(__file__), "images", "dark_sky_background.png")
        bg_image = ctk.CTkImage(Image.open(bg_path), size=(900, 700))
        self.bg_label = ctk.CTkLabel(self, image=bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # --- Scrollable card ---
        card = ctk.CTkScrollableFrame(self, corner_radius=30, fg_color="#1B263B", width=300, height=500)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), "images", "logo_hypnos.png")
        logo_image = ctk.CTkImage(Image.open(logo_path), size=(200, 200))
        ctk.CTkLabel(card, image=logo_image, text="", bg_color="transparent").pack(pady=(24, 8))

        ctk.CTkLabel(card, text="Login", font=("Arial", 22, "bold"), text_color="#63B3ED").pack(pady=(0, 10))

        # Switch for Doctor/Patient (vertical layout)
        self.user_type = ctk.StringVar(value="Doctor")
        switch_frame = ctk.CTkFrame(card, fg_color="transparent")
        switch_frame.pack(pady=10)
        ctk.CTkRadioButton(
            switch_frame, text="Doctor", font=("Helvetica", 18, "bold"), text_color="#63B3ED", variable=self.user_type, value="Doctor",
            fg_color="#2563eb", hover_color="#1e40af", border_color="#63B3ED"
        ).pack(fill="x", pady=2)
        ctk.CTkRadioButton(
            switch_frame, text="Patient", font=("Helvetica", 18, "bold"), text_color="#63B3ED", variable=self.user_type, value="Patient",
            fg_color="#2563eb", hover_color="#1e40af", border_color="#63B3ED"
        ).pack(fill="x", pady=2)

        # Name entry
        self.name_entry = ctk.CTkEntry(card, placeholder_text="Enter Name", width=200, fg_color="#0D1B2A", text_color="#F0EDEE")
        self.name_entry.pack(pady=8)

        # Surname entry
        self.surname_entry = ctk.CTkEntry(card, placeholder_text="Enter Surname", width=200, fg_color="#0D1B2A", text_color="#F0EDEE")
        self.surname_entry.pack(pady=8)

        # Password entry
        self.password_entry = ctk.CTkEntry(card, placeholder_text="Enter Password", show="*", width=200, fg_color="#0D1B2A", text_color="#F0EDEE")
        self.password_entry.pack(pady=8)

        self.message_label = ctk.CTkLabel(card, text="", text_color="#ef4444")
        self.message_label.pack(pady=8)

        # Register New Patient button
#        self.register_patient_button = ctk.CTkButton(
#            card, text="New Patient?", fg_color="#3366cc", hover_color="#5588dd",
#            text_color="#F0EDEE", width=200, height=30, font=("Arial", 15, "bold"), corner_radius=10,
#            command=self.open_registrationpat
#        )
#        self.register_patient_button.pack(pady=(8, 16))

        # Register New Doctor button
        self.register_doctor_button = ctk.CTkButton(
            card, text="New Doctor?", fg_color="#3366cc", hover_color="#5588dd",
            text_color="#F0EDEE", width=200, height=30, font=("Arial", 15, "bold"), corner_radius=10,
            command=self.open_registrationdoc
        )
        self.register_doctor_button.pack(pady=(8, 16))

        self.login_button = ctk.CTkButton(
            card, text="Login", command=self.login_callback,
            fg_color="#63B3ED", hover_color="#2563eb", text_color="#1B263B",
            width=200, height=40, font=("Arial", 15, "bold"), corner_radius=18
        )
        self.login_button.pack(pady=8)

    def login_callback(self):
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        password = self.password_entry.get().strip()
        user_type = self.user_type.get()

        print(f"Attempting login as {user_type} with name: {name}, surname: {surname}, password: {password}")

        if user_type == "Doctor":
            user = authenticate_doctor(surname, password)
            if user and user.name.lower() == name.lower():
                self.destroy()
                app = DoctorApp(user)
                app.mainloop()
            else:
                self.message_label.configure(text="Invalid doctor credentials", text_color="#ef4444")
        else:
            user = authenticate_patient(surname, password)
            if user and user.name.lower() == name.lower():
                self.destroy()
                app = PatientApp(user)
                app.mainloop()
            else:
                self.message_label.configure(text="Invalid patient credentials", text_color="#ef4444")

    def open_registrationpat(self):
        AddPatientDialog(self)

    def open_registrationdoc(self):
        AddDoctorDialog(self)

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()

    # patient credentials = {Name: "Darius", Surname: "Barker", Password: "12345" }
    # doctor credentials = {Name: "Vanessa", Surname: "Bautista", Password: "12345" }