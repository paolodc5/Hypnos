import customtkinter as ctk
from services.auth_service import add_doctor_to_db

class AddDoctorDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add New Doctor")
        self.geometry("600x700")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Add New Doctor", font=("Arial", 20, "bold"), text_color="#63B3ED").pack(pady=(16, 12))

        form = ctk.CTkFrame(self, fg_color="#1B263B", corner_radius=12)
        form.pack(fill="both", padx=20, pady=10)

        self.entries = {}

        # Fields for doctor registration
        fields = [
            ("Name", True),
            ("Surname", True),
            ("Specialty", True),
            ("Email", True),
            ("Password", True),
        ]

        # Create input fields dynamically
        for i, (label_text, required) in enumerate(fields):
            ctk.CTkLabel(form, text=f"{label_text}:", anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=8)

            placeholder = "Required" if required else "Optional"

            # Create the entry fields based on the type (Password or Text)
            if label_text == "Password":
                entry = ctk.CTkEntry(form, show="*", placeholder_text=placeholder)
                entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
                self.entries["password"] = entry
            else:
                entry = ctk.CTkEntry(form, placeholder_text=placeholder)
                entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
                key = label_text.split()[0].lower()
                self.entries[key] = entry

        form.grid_columnconfigure(1, weight=1)

        self.error_label = ctk.CTkLabel(form, text="", text_color="red", font=("Arial", 12, "bold"))
        self.error_label.grid(row=len(fields), column=0, columnspan=2, pady=(4, 0))

        # Submit Button
        ctk.CTkButton(form, text="Add Doctor", fg_color="#63B3ED", hover_color="#2563eb", command=self.submit).grid(
            row=len(fields)+1, column=0, columnspan=2, pady=20, ipadx=10, ipady=5
        )

    def submit(self):
        self.error_label.configure(text="")

        # Get the input data
        data = {key: widget.get().strip() for key, widget in self.entries.items()}

        # Validate required fields
        required_fields = ["name", "surname", "specialty", "email", "password"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            self.error_label.configure(text=f"Missing required fields: {', '.join(missing)}")
            return

        # Insert the new doctor into the database
        try:
            add_doctor_to_db(
                name=data["name"],
                surname=data["surname"],
                specialty=data["specialty"],
                email=data["email"],
                password=data["password"]
            )
        except Exception as e:
            self.error_label.configure(text=f"Error adding doctor: {e}")
            return

        self.error_label.configure(text="Doctor added successfully!", text_color="green")
        self.destroy()
