# gui/login.py
import customtkinter as ctk
from gui.doctor.doctor_app import DoctorApp
from services.auth_service import authenticate_doctor

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hypnos - Login")
        self.geometry("600x500")

        ctk.CTkLabel(self, text="Doctor Login", font=("Arial", 18)).pack(pady=20)
        
        self.doc_id_entry = ctk.CTkEntry(self, placeholder_text="Enter Doctor Surname", width=200)
        self.doc_id_entry.pack(pady=10)

        # Add password entry
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter Password", show="*", width=200)
        self.password_entry.pack(pady=10)


        self.message_label = ctk.CTkLabel(self, text="", text_color="red")
        self.message_label.pack(pady=10)
    
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_callback, 
                                           fg_color="#2563eb", hover_color="#1e40af", width=200)
        self.login_button.pack(pady=20)

 
    
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

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()

    # credentials = { Surname: "Bautista", Password: "12345" }