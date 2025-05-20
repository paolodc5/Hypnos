import customtkinter as ctk
from services.patient_services import add_patient_to_db, get_all_doctors
import re

class AddPatientDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add New Patient")
        self.geometry("600x700")

        ctk.CTkLabel(self, text="Add New Patient", font=("Arial", 20, "bold"), text_color="#63B3ED").pack(pady=(16, 12))

        form = ctk.CTkFrame(self, fg_color="#1B263B", corner_radius=12)
        form.pack(fill="both", padx=20, pady=10)

        # Load doctors for combobox
        self.doctor_map = {doc['Surname']: doc['DocID'] for doc in get_all_doctors()}

        self.entries = {}

        # Fields for patients only
        fields = [
            ("Name", True),
            ("Surname", True),
            ("Password", True),
            ("Phone Number", True),
            ("Birth Date (YYYY-MM-DD)", True),
            ("Age", True),
            ("Gender (M/F)", True),
            ("Fiscal Code (8 simbols)", True),
            ("Doctor", False),
        ]

        for i, (label_text, required) in enumerate(fields):
            ctk.CTkLabel(form, text=f"{label_text}:", anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=8)

            placeholder = "Required" if required else "Optional"

            if label_text == "Gender (M/F)":
                combo = ctk.CTkComboBox(form, values=["M", "F"])
                combo.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
                self.entries["gender"] = combo

            elif label_text == "Doctor":
                combo = ctk.CTkComboBox(form, values=list(self.doctor_map.keys()))
                combo.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
                self.entries["doctor"] = combo

            elif label_text == "Password":
                entry = ctk.CTkEntry(form, show="*", placeholder_text=placeholder)
                entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
                self.entries["password"] = entry

            else:
                entry = ctk.CTkEntry(form, placeholder_text=placeholder)
                entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
                key = label_text.split()[0].lower()
                if label_text == "Birth Date (YYYY-MM-DD)":
                    key = "birth_date"
                if label_text == "Phone Number":
                    key = "phone"
                if label_text == "Fiscal Code (8 simbols)":
                    key = "fiscal_code"
                if label_text == "Age":
                    key = "age"
                self.entries[key] = entry

        form.grid_columnconfigure(1, weight=1)

        self.error_label = ctk.CTkLabel(form, text="", text_color="red", font=("Arial", 12, "bold"))
        self.error_label.grid(row=len(fields), column=0, columnspan=2, pady=(4, 0))

        ctk.CTkButton(form, text="Add Patient", fg_color="#63B3ED", hover_color="#2563eb", command=self.submit).grid(
            row=len(fields)+1, column=0, columnspan=2, pady=20, ipadx=10, ipady=5
        )

    def submit(self):
        self.error_label.configure(text="")

        data = {key: widget.get().strip() for key, widget in self.entries.items()}

        # Required fields except doctor which is optional here
        required_fields = ["name", "surname", "password", "phone", "birth_date", "age", "gender", "fiscal_code"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            self.error_label.configure(text=f"Missing required fields: {', '.join(missing)}")
            return

        if not data["age"].isdigit() or int(data["age"]) <= 0:
            self.error_label.configure(text="Age must be a positive integer.")
            return

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", data["birth_date"]):
            self.error_label.configure(text="Birth Date must be in YYYY-MM-DD format.")
            return

        if data["gender"] not in ("M", "F"):
            self.error_label.configure(text="Gender must be M or F.")
            return

        # Doctor ID optional
        doctor_id = None
        if data.get("doctor"):
            doctor_id = self.doctor_map.get(data["doctor"])
            if doctor_id is None:
                self.error_label.configure(text="Selected doctor is invalid.")
                return

        # Call DB save function
        try:
            add_patient_to_db(
                name=data["name"],
                surname=data["surname"],
                password=data["password"],
                phone_number=data["phone"],
                birth_date=data["birth_date"],
                age=int(data["age"]),
                gender=data["gender"],
                fiscal_code=data["fiscal_code"],
                doctor_id=doctor_id,
            )
        except Exception as e:
            self.error_label.configure(text=f"Database error: {e}")
            return

        self.error_label.configure(text="Patient added successfully!", text_color="green")
        self.destroy()
