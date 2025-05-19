# gui/login.py
import customtkinter as ctk
from gui.patient.patient_app import PatientApp
from services.auth_patient_service import authenticate_patient

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hypnos - Login")
        self.geometry("400x300")

        ctk.CTkLabel(self, text="Patient Login", font=("Arial", 18)).pack(pady=20)
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Enter your username (email)")
        self.username_entry.pack(pady=10)

        # Add password entry
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter Password", show="*")
        self.password_entry.pack(pady=10)


        self.message_label = ctk.CTkLabel(self, text="", text_color="red")
        self.message_label.pack(pady=10)
    
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_callback)
        self.login_button.pack(pady=20)

 
    
    def login_callback(self):
        name = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        print(f"Attempting to login with username: {name} and password: {password}")
        print(type(name), type(password))

        patient = authenticate_patient(name, password)

        if patient:
            self.destroy()
            app = PatientApp(patient)  # pass full Doctor object
            app.mainloop()
        else:
            self.message_label.configure(text="Invalid credentials", text_color="red")