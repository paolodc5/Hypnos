import customtkinter as ctk
from models.patient import Patient


class PatientApp(ctk.CTk):
    def __init__(self, patient: Patient):
        super().__init__()
        self.title(f"Hypnos - Patient Dashboard")
        self.geometry("1000x600")
        self.patient = patient
        # self.patient.load_patients()

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
        ctk.CTkLabel(self.sidebar, text="E-Health System", font=("Arial", 16, "bold"), text_color="white", width=200, 
                     height=30, anchor="center").place(x=0, y=30)

        # Navigation buttons
        self.home_button = ctk.CTkButton(self.sidebar, text="Home", command=self.load_home, width=160, fg_color="#3366cc", 
                                         hover_color="#66d9cc").place(x=20, y=80)
        
        self.myprofile_button = ctk.CTkButton(self.sidebar, text="My Profile", command=self.load_my_profile, width=160, 
                                              fg_color="#3366cc", hover_color="#66d9cc")
        self.myprofile_button.place(x=20, y=130)

        self.prescriptions_button = ctk.CTkButton(self.sidebar, text="My Prescriptions", width=160, fg_color="#3366cc", 
                                                  hover_color="#66d9cc")
        self.prescriptions_button.place(x=20, y=180) 

        self.mydoctor_button = ctk.CTkButton(self.sidebar, text="Sleep Specialist's Profile", command=self.load_doctor_profile, 
                                             width=160, fg_color="#3366cc", hover_color="#66d9cc")
        self.mydoctor_button.place(x=20, y=230)

        self.myreports_button = ctk.CTkButton(self.sidebar, text="My Sleep Records", width=160, fg_color="#3366cc", 
                                                  hover_color="#66d9cc")
        self.myreports_button.place(x=20, y=280)
        
        self.notes_button = ctk.CTkButton(self.sidebar, text="Personal Notes", command=self.load_notes, width=160, fg_color="#3366cc", 
                                                  hover_color="#66d9cc")
        self.notes_button.place(x=20, y=330)


    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            if widget not in [self.sidebar]:
                widget.destroy()


    def load_home(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text=f"Welcome back, {(self.patient.surname), (self.patient.name)}", 
                     font=("Arial", 18), text_color="#204080", width=600, height=50 ).place(x=0, y=225)


    """def load_profile(self):
        self.clear_main_content()
        label = ctk.CTkLabel(self.content_frame, text=f
            Name: {self.patient.name}
            Surname: {self.patient.surname}
            Fiscal code: {self.patient.fiscal_code}
            Gender: {self.patient.gender}
            Age: {self.patient.age}
            Email: {self.patient.email}
        , font=("Arial", 18), justify="left")
        label.pack(pady=40)"""

    def load_my_profile(self):
        self.clear_content()

        # Card centrale
        card = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#f0f4f7")
        card.pack(pady=50, padx=50, fill="both", expand=True)

        title = ctk.CTkLabel(card, text="My Profile", font=("Arial", 22, "bold"), text_color="#204080")
        title.pack(pady=(20, 10))

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(pady=20)

        ctk.CTkLabel(info_frame, text=f"👤 Name: {self.patient.name} {self.patient.surname}", font=("Arial", 16)).pack(pady=5, anchor="w")
        ctk.CTkLabel(info_frame, text=f"🎂 Birthdate: {self.patient.birth_date}", font=("Arial", 16)).pack(pady=5, anchor="w")
        ctk.CTkLabel(info_frame, text=f"📧 Email: {self.patient.email}", font=("Arial", 16)).pack(pady=5, anchor="w")
        """self.email_entry = ctk.CTkEntry(self.content_frame)
        self.email_entry.insert(0, self.patient.email)
        self.email_entry.pack()"""
        ctk.CTkLabel(info_frame, text=f"📞 Phone: {self.patient.phone_number}", font=("Arial", 16)).pack(pady=5, anchor="w")
        """self.phone_entry = ctk.CTkEntry(self.content_frame)
        self.phone_entry.insert(0, getattr(self.patient, "phone_number", ""))  # se ce l’hai
        self.phone_entry.pack()"""
        update_button = ctk.CTkButton(card, text="Update Info", fg_color="#33aa66", hover_color="#55cc88",
                                      command=self.show_update_form, width=120)
        update_button.pack(pady=20)

    def show_update_form(self):
        self.clear_content()

        form_frame = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#f0f4f7")
        form_frame.pack(pady=50, padx=50, fill="both", expand=True)

        title = ctk.CTkLabel(form_frame, text="Update Profile Information", font=("Arial", 20, "bold"), text_color="#204080")
        title.pack(pady=(20, 10))

        # Email field
        email_label = ctk.CTkLabel(form_frame, text="Email:", font=("Arial", 14))
        email_label.pack(pady=(20, 5))
        self.email_entry = ctk.CTkEntry(form_frame, width=300)
        self.email_entry.insert(0, self.patient.email)
        self.email_entry.pack()

        # Phone field
        phone_label = ctk.CTkLabel(form_frame, text="Phone Number:", font=("Arial", 14))
        phone_label.pack(pady=(20, 5))
        self.phone_entry = ctk.CTkEntry(form_frame, width=300)
        self.phone_entry.insert(0, self.patient.phone_number)
        self.phone_entry.pack()

        # Save button
        save_button = ctk.CTkButton(
            form_frame, text="Save Changes", fg_color="#3366cc", hover_color="#5588dd",
            command=self.save_profile_changes
        )
        save_button.pack(pady=30)

    def save_profile_changes(self):
        new_email = self.email_entry.get()
        new_phone = self.phone_entry.get()

        # Aggiorna l'oggetto e salva (supponiamo ci sia un metodo .save())
        self.patient.email = new_email
        self.patient.phone_number = new_phone
        self.patient.save()  # implementa se non esiste

        # Torna al profilo aggiornato
        self.load_my_profile()


    """def load_doctor_profile(self):
        self.clear_content()
        doctor = self.patient.get_doctor()
        if not doctor:
                error_label = ctk.CTkLabel(self.content_frame, text="No doctor assigned.", font=("Arial", 16), text_color="red")
                error_label.pack(pady=40)
                return
        
        label = ctk.CTkLabel(self.content_frame, text=f
            Name: {doctor.name}
            Surname: {doctor.surname}
            Specialization: {doctor.specialty}
            Email: {doctor.email}
        , font=("Arial", 18), justify="left")
        label.pack(pady=40)"""

    def load_doctor_profile(self):
        self.clear_content()
        doctor = self.patient.get_doctor()

        # Cornice centrale tipo "card"
        card = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#f0f4f7")
        card.pack(pady=50, padx=50, fill="both", expand=True)

        title = ctk.CTkLabel(card, text="Your Sleep Specialist", font=("Arial", 22, "bold"), text_color="#204080")
        title.pack(pady=(20, 10))

        # Dati visualizzati in colonne/righe
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(pady=20)

        ctk.CTkLabel(info_frame, text=f"👤 Name: {doctor.name} {doctor.surname}", font=("Arial", 16)).pack(pady=5, anchor="w")
        ctk.CTkLabel(info_frame, text=f"🩺 Specialty: {doctor.specialty}", font=("Arial", 16)).pack(pady=5, anchor="w")
        ctk.CTkLabel(info_frame, text=f"📧 Email: {doctor.email}", font=("Arial", 16)).pack(pady=5, anchor="w")

        # Opzionale: bottone per contattare il dottore
        contact_button = ctk.CTkButton(card, text="Contact Doctor", fg_color="#3366cc", hover_color="#66d9cc")
        contact_button.pack(pady=(10, 20))


    def load_notes(self):
        self.clear_content()

        # Simuliamo il caricamento di note dal database
        notes = self.patient.get_notes()  # Supponiamo che restituisca una lista di Note

        notes_label = ctk.CTkLabel(self.content_frame, text="Your Notes:", font=("Arial", 16))
        notes_label.pack(pady=10)

        for note in notes:
            ctk.CTkLabel(self.content_frame, text=f"{note.date}: {note.content}", font=("Arial", 14)).pack(anchor="w", padx=20)

        # Area per inserire una nuova nota
        self.note_entry = ctk.CTkTextbox(self.content_frame, height=100, width=500)
        self.note_entry.pack(pady=10)

        save_button = ctk.CTkButton(self.content_frame, text="Add Note", command=self.save_note)
        save_button.pack()

def save_note(self):
    content = self.note_entry.get("1.0", "end").strip()
    if content:
        self.patient.add_note(content)  # Salva nel DB o lista
        self.load_notes()  # Ricarica la sezione




    # def load_prescriptions(self):
    #     self.clear_content()
    #     show_prescriptions(self.content_frame, self.doctor_id)

    # def load_notes(self):
    #     self.clear_content()
    #     show_notes(self.content_frame, self.doctor_id)

    # def load_sleep_data(self):
    #     self.clear_content()
    #     show_sleep_data(self.content_frame, self.doctor_id)