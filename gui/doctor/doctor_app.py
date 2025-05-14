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
        self.doctor.load_patients()
        
        self.setup_gui()
        self.load_home()


    def setup_gui(self):

        # Set up the sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, height=500, fg_color="#204080")
        self.sidebar.pack(side="left", fill="y")
        self.title("Workspace")
        self.geometry("800x500")


        # Set up the main window
        self.content_frame = ctk.CTkFrame(self, width=800)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Set appearance and theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")  # Predefined blue theme

        # Sidebar title
        ctk.CTkLabel(self.sidebar, text="E-Health System", font=("Arial", 16, "bold"), text_color="white", width=200, height=30, anchor="center"
                     ).place(x=0, y=30)

        # Navigation buttons
        self.home_button = ctk.CTkButton(self.sidebar, text="Home", command=self.load_home, width=160, fg_color="#3366cc", hover_color="#66d9cc"
                                        ).place(x=20, y=80)
        self.prescriptions_button = ctk.CTkButton(self.sidebar, text="Patients", width=160, fg_color="#3366cc", hover_color="#66d9cc"
                                        ).place(x=20, y=130)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()


    def load_home(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text=f"Welcome back, Dr. {self.doctor.surname}", font=("Arial", 18), text_color="#204080", width=600, height=50
                     ).place(x=0, y=225)

    # def load_prescriptions(self):
    #     self.clear_content()
    #     show_prescriptions(self.content_frame, self.doctor_id)

    # def load_notes(self):
    #     self.clear_content()
    #     show_notes(self.content_frame, self.doctor_id)

    # def load_sleep_data(self):
    #     self.clear_content()
    #     show_sleep_data(self.content_frame, self.doctor_id)