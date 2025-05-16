import customtkinter as ctk
from gui.doctor.add_patient_dialog import AddPatientDialog

class PatientSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, doctor, patients, command_callback):
        super().__init__(master)
        self.doctor = doctor
        self.command_callback = command_callback
        self.selected_patient = ctk.StringVar()
        self.patients = patients

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.patient_map = {f"{p.surname} {p.name}": p for p in patients}

        ctk.CTkLabel(self, text="Select Patient", font=("Arial", 14, "bold"), text_color="#204080").grid(row=0, column=0, sticky="w", padx=10, pady=(0, 8), columnspan=2)
        self.dropdown = ctk.CTkComboBox(
            self,
            values=list(self.patient_map.keys()),
            variable=self.selected_patient,
            width=260,
            font=("Arial", 13),
            command=self._on_selection
        )
        self.dropdown.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="w")

        # + Button
        self.add_button = ctk.CTkButton(self, text="+", width=36, height=36, font=("Arial", 18, "bold"),
                                        fg_color="#2563eb", hover_color="#1e40af", command=self.open_add_patient_dialog)
        self.add_button.grid(row=1, column=1, padx=(8, 10), pady=(0, 10), sticky="w")

    def _on_selection(self, selected_name):
        patient = self.patient_map.get(selected_name)
        if patient:
            self.command_callback(patient)

    def open_add_patient_dialog(self):
        dialog = AddPatientDialog(self)
        self.wait_window(dialog)
        if getattr(dialog, "new_patient", None):
            self.doctor.load_patients()
            self.patients = self.doctor.patients
            self.patient_map = {f"{p.surname} {p.name}": p for p in self.patients}
            self.dropdown.configure(values=list(self.patient_map.keys()))