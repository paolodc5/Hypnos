import customtkinter as ctk
import re

class ProfileUpdateDialog(ctk.CTkToplevel):
    def __init__(self, master, patient, on_success=None):
        super().__init__(master)
        self.title("Update Profile")
        self.geometry("420x480")
        self.resizable(False, False)
        self.patient = patient
        self.on_success = on_success

        ctk.CTkLabel(self, text="Update Profile", font=("Arial", 20, "bold")).pack(pady=(18, 10))

        form = ctk.CTkFrame(self, fg_color="#f8fafc", corner_radius=12)
        form.pack(fill="both", expand=True, padx=16, pady=8)

        # Name
        ctk.CTkLabel(form, text="Name:", anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 2))
        self.name_entry = ctk.CTkEntry(form)
        self.name_entry.insert(0, patient.name)
        self.name_entry.grid(row=0, column=1, padx=10, pady=(10, 2))

        # Surname
        ctk.CTkLabel(form, text="Surname:", anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.surname_entry = ctk.CTkEntry(form)
        self.surname_entry.insert(0, patient.surname)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=2)

        # Birthdate
        ctk.CTkLabel(form, text="Birthdate (YYYY-MM-DD):", anchor="w").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.birth_entry = ctk.CTkEntry(form)
        self.birth_entry.insert(0, patient.birth_date)
        self.birth_entry.grid(row=2, column=1, padx=10, pady=2)

        # Age
        ctk.CTkLabel(form, text="Age:", anchor="w").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.age_entry = ctk.CTkEntry(form)
        self.age_entry.insert(0, str(patient.age))
        self.age_entry.grid(row=3, column=1, padx=10, pady=2)

        # Gender
        ctk.CTkLabel(form, text="Gender (M/F):", anchor="w").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.gender_entry = ctk.CTkEntry(form)
        self.gender_entry.insert(0, patient.gender)
        self.gender_entry.grid(row=4, column=1, padx=10, pady=2)

        # Fiscal Code
        ctk.CTkLabel(form, text="Fiscal Code:", anchor="w").grid(row=5, column=0, sticky="w", padx=10, pady=2)
        self.fiscal_entry = ctk.CTkEntry(form)
        self.fiscal_entry.insert(0, patient.fiscal_code)
        self.fiscal_entry.grid(row=5, column=1, padx=10, pady=2)

        # Email
        ctk.CTkLabel(form, text="Email:", anchor="w").grid(row=6, column=0, sticky="w", padx=10, pady=2)
        self.email_entry = ctk.CTkEntry(form)
        self.email_entry.insert(0, patient.email or "")
        self.email_entry.grid(row=6, column=1, padx=10, pady=2)

        # Phone
        ctk.CTkLabel(form, text="Phone Number:", anchor="w").grid(row=7, column=0, sticky="w", padx=10, pady=2)
        self.phone_entry = ctk.CTkEntry(form)
        self.phone_entry.insert(0, patient.phone_number)
        self.phone_entry.grid(row=7, column=1, padx=10, pady=2)

        # Error label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 12, "bold"))
        self.error_label.pack(pady=(0, 0))

        # Submit button
        ctk.CTkButton(self, text="Submit", fg_color="#3366cc", hover_color="#5588dd", command=self.submit).pack(pady=18)

    def submit(self):
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        birth = self.birth_entry.get().strip()
        age = self.age_entry.get().strip()
        gender = self.gender_entry.get().strip().upper()
        fiscal = self.fiscal_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        # Validation
        if not all([name, surname, birth, age, gender, fiscal, phone]):
            self.error_label.configure(text="All fields except email are required.")
            return
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", birth):
            self.error_label.configure(text="Birthdate must be YYYY-MM-DD.")
            return
        if not age.isdigit() or int(age) <= 0:
            self.error_label.configure(text="Age must be a positive integer.")
            return
        if gender not in ("M", "F"):
            self.error_label.configure(text="Gender must be 'M' or 'F'.")
            return
        if not re.match(r"^[A-Z0-9]{8}$", fiscal, re.IGNORECASE):
            self.error_label.configure(text="Fiscal code must be 8 alphanumeric characters.")
            return
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.error_label.configure(text="Invalid email format.")
            return
        if not re.match(r"^\d{8,15}$", phone):
            self.error_label.configure(text="Phone must be 8-15 digits.")
            return

        # Save to patient object
        self.patient.name = name
        self.patient.surname = surname
        self.patient.birth_date = birth
        self.patient.age = int(age)
        self.patient.gender = gender
        self.patient.fiscal_code = fiscal
        self.patient.email = email
        self.patient.phone_number = phone
        self.patient.save()  # This should update the DB

        if self.on_success:
            self.on_success()
        self.destroy()