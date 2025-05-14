import customtkinter as ctk
from models.doctor import Doctor
# from gui.doctor.prescription_tab import show_prescriptions
# from gui.doctor.note_tab import show_notes
# from gui.doctor.sleep_tab import show_sleep_data

class DoctorApp(ctk.CTk):
    def __init__(self, doctor: Doctor):
        super().__init__()
        self.title(f"Hypnos - Doctor Dashboard")
        self.geometry("1000x600")
        self.doctor = doctor
        self.doctor_id = doctor.doctor_id
  

        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self, width=800)
        self.content_frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(self.sidebar, text="Doctor Dashboard", font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Prescriptions").pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Notes").pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Sleep Records").pack(pady=10)

        self.load_home()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def load_home(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text=f"Welcome Doctor {self.doctor.name}", font=("Arial", 20)).pack(pady=20)

    # def load_prescriptions(self):
    #     self.clear_content()
    #     show_prescriptions(self.content_frame, self.doctor_id)

    # def load_notes(self):
    #     self.clear_content()
    #     show_notes(self.content_frame, self.doctor_id)

    # def load_sleep_data(self):
    #     self.clear_content()
    #     show_sleep_data(self.content_frame, self.doctor_id)