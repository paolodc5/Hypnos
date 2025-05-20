import customtkinter as ctk
from services.patient_services import add_patient_to_db, get_all_doctors
import re

class AddPatientDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add New Patient")
        self.geometry("400x480")
        self.resizable(False, False)
        self.new_patient = None

        ctk.CTkLabel(self, text="Add New Patient", font=("Arial", 18, "bold")).pack(pady=(18, 10))

        form = ctk.CTkFrame(self, fg_color="#1B263B", corner_radius=12)
        form.pack(fill="both", expand=True, padx=16, pady=8)

        # Name
        ctk.CTkLabel(form, text="Name:", anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 2))
        self.name_entry = ctk.CTkEntry(form)
        self.name_entry.grid(row=0, column=1, padx=10, pady=(10, 2))

        # Surname
        ctk.CTkLabel(form, text="Surname:", anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.surname_entry = ctk.CTkEntry(form)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=2)

        # Age
        ctk.CTkLabel(form, text="Age:", anchor="w").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.age_entry = ctk.CTkEntry(form)
        self.age_entry.grid(row=2, column=1, padx=10, pady=2)

        # Date of Birth
        ctk.CTkLabel(form, text="Date of Birth (YYYY-MM-DD):", anchor="w").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.dob_entry = ctk.CTkEntry(form)
        self.dob_entry.grid(row=3, column=1, padx=10, pady=2)

        # Gender
        ctk.CTkLabel(form, text="Gender:", anchor="w").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.gender_combo = ctk.CTkComboBox(form, values=["M", "F"])
        self.gender_combo.grid(row=4, column=1, padx=10, pady=2)

        # Fiscal Code
        ctk.CTkLabel(form, text="Fiscal Code:", anchor="w").grid(row=5, column=0, sticky="w", padx=10, pady=2)
        self.fiscal_entry = ctk.CTkEntry(form)
        self.fiscal_entry.grid(row=5, column=1, padx=10, pady=2)

        # Phone Number
        ctk.CTkLabel(form, text="Phone Number:", anchor="w").grid(row=6, column=0, sticky="w", padx=10, pady=2)
        self.phone_entry = ctk.CTkEntry(form)
        self.phone_entry.grid(row=6, column=1, padx=10, pady=2)

        # Doctor (ComboBox)
        ctk.CTkLabel(form, text="Doctor:", anchor="w").grid(row=7, column=0, sticky="w", padx=10, pady=2)
        doctors = get_all_doctors()
        self.doctor_map = {doc['Surname']: doc['DocID'] for doc in doctors}
        self.doctor_combo = ctk.CTkComboBox(form, values=list(self.doctor_map.keys()))
        self.doctor_combo.grid(row=7, column=1, padx=10, pady=2)

        # Error label (persistent)
        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 12, "bold"))
        self.error_label.pack(pady=(0, 0))

        # Submit button
        ctk.CTkButton(self, text="Add Patient", fg_color="#2563eb", hover_color="#1e40af", command=self.submit).pack(pady=18)

    def submit(self):
        self.error_label.configure(text="")  # Clear previous error

        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        age = self.age_entry.get().strip()
        dob = self.dob_entry.get().strip()
        gender = self.gender_combo.get().strip()
        fiscal = self.fiscal_entry.get().strip()
        phone = self.phone_entry.get().strip()
        doctor_surname = self.doctor_combo.get().strip()
        doctor_id = self.doctor_map.get(doctor_surname)

        # Validation
        if not all([name, surname, age, dob, gender, fiscal, phone, doctor_id]):
            self.error_label.configure(text="All fields are required.")
            return

        if not age.isdigit() or int(age) <= 0:
            self.error_label.configure(text="Age must be a positive integer.")
            return

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
            self.error_label.configure(text="Date of Birth must be YYYY-MM-DD.")
            return

        # Add to DB
        try:
            add_patient_to_db(
                name=name,
                surname=surname,
                age=int(age),
                birth_date=dob,
                gender=gender,
                fiscal_code=fiscal,
                phone_number=phone,
                doctor_id=doctor_id
            )
        except Exception as e:
            self.error_label.configure(text=f"Database error: {e}")
            return

        self.new_patient = True
        self.destroy()