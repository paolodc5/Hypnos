# gui/login.py
import customtkinter as ctk
from gui.doctor.doctor_app import DoctorApp
from services.auth_service import authenticate_doctor

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hypnos - Login")
        self.geometry("400x300")

        ctk.CTkLabel(self, text="Doctor Login", font=("Arial", 18)).pack(pady=20)
        self.doc_id_entry = ctk.CTkEntry(self, placeholder_text="Enter Doctor Name")
        self.doc_id_entry.pack(pady=10)

        # Add password entry
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter Password", show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_callback)
        self.login_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(self, text="", text_color="red")
        self.message_label.pack(pady=10)
    
    def login_callback(self):
        name = self.doc_id_entry.get().strip()
        password = self.password_entry.get().strip()

        print(f"Attempting to login with name: {name} and password: {password}")
        print(type(name), type(password))

        doctor = authenticate_doctor(name, password)

        if doctor:
            self.destroy()
            app = DoctorApp(doctor)  # pass full Doctor object
            app.mainloop()
        else:
            self.message_label.configure(text="Invalid credentials", text_color="red")