# gui/doctor/patient_tab.py
import customtkinter as ctk
from models.doctor import Doctor
from gui.doctor.scrollable_list_frame import ScrollableListFrame

class PatientTab(ctk.CTkFrame):
    def __init__(self, master, doctor: Doctor):
        super().__init__(master)
        self.doctor = doctor
        self.selected_patient = ctk.StringVar()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=8)
        self.grid_columnconfigure(0, weight=1)

        self.dropdown_frame = PatientSelectionFrame(self, patients=self.doctor.patients, command_callback=self.show_info)
        self.dropdown_frame.configure(fg_color='transparent')
        self.dropdown_frame.grid(row=0, column=0, padx=(20, 20), pady=(5, 0), sticky="nsew")

        self.info_frame = InfoFrame(self)
        self.info_frame.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.segmented_bar = AdministrationFrame(self)
        self.segmented_bar.grid(row=2, column=0, padx=(20, 20), pady=(10, 20), sticky="nsew")

    def show_info(self, patient):
        self.info_frame.show_info(patient)
        self.segmented_bar.set_patient(patient)

class InfoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)

    def show_info(self, patient):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        # Display patient info
        ctk.CTkLabel(self, text="Patient Information", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=15, pady=(20, 5), sticky="w")
        ctk.CTkLabel(self, text=f"Name: {patient.name} {patient.surname}").grid(row=1, column=0, padx=15, sticky="w")
        ctk.CTkLabel(self, text=f"Age: {patient.age}").grid(row=2, column=0, padx=15, sticky="w")
        ctk.CTkLabel(self, text=f"Phone Number: {patient.phone_number}").grid(row=3, column=0, padx=15, sticky="w")
        ctk.CTkLabel(self, text=f"Fiscal Code: {patient.fiscal_code}").grid(row=4, column=0, padx=15, sticky="w")

class AdministrationFrame(ctk.CTkFrame):
    def __init__(self, master, patient=None):
        super().__init__(master)
        self.patient = patient

        # Segmented button at the top center
        self.seg_button = ctk.CTkSegmentedButton(self, values=["Sleep", "Notes", "Prescriptions"], command=self.show_section)
        self.seg_button.grid(row=0, column=0, pady=(10, 10), padx=0, sticky="n")

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.current_section = None
        self.show_section("Sleep")  # Default

    def set_patient(self, patient):
        self.patient = patient
        self.show_section(self.current_section or "Sleep")

    def show_section(self, section):
        self.current_section = section
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.patient:
            ctk.CTkLabel(self.content_frame, text="No patient selected").pack()
            return

        if section == "Sleep":
            self.patient.load_sleep_records()
            items = self.patient.sleep_records
            formatter = lambda r: f"{r.date} | HR: {r.hr} | SpO2: {r.spo2} | MovIdx: {r.movement_idx} | Cycles: {r.sleep_cycles}"
        elif section == "Notes":
            self.patient.load_notes()
            items = self.patient.notes
            formatter = lambda n: f"{n.date}: {n.content}"
        elif section == "Prescriptions":
            self.patient.load_prescriptions()
            items = self.patient.prescriptions
            formatter = lambda p: f"{p.precr_date}: {p.treatm_type} - {p.content}"
        else:
            items = []
            formatter = str

        ScrollableListFrame(self.content_frame, items, item_formatter=formatter).pack(fill="both", expand=True)

class PatientSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, patients, command_callback):
        super().__init__(master)
        self.command_callback = command_callback
        self.selected_patient = ctk.StringVar()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Map full name to patient object
        self.patient_map = {f"{p.surname} {p.name}": p for p in patients}

        # Set up dropdown
        self.dropdown = ctk.CTkComboBox(
            self,
            values=list(self.patient_map.keys()),
            variable=self.selected_patient,
            width=300,
            command=self._on_selection
        )
        self.dropdown.grid(row=0, column=0)

    def _on_selection(self, selected_name):
        # Get Patient object from name
        patient = self.patient_map.get(selected_name)
        if patient:
            self.command_callback(patient)
