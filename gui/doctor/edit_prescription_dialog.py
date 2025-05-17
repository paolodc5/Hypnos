import customtkinter as ctk
from services.doctor_services import update_prescription

class EditPrescriptionDialog(ctk.CTkToplevel):
    def __init__(self, master, patient, prescription):
        super().__init__(master)
        self.title("✏️ Edit Prescription")
        self.geometry("480x400")
        self.resizable(False, False)
        self.prescription = prescription

        ctk.CTkLabel(self, text="Edit Prescription", font=("Arial", 20, "bold"), text_color="#1e3a8a").pack(pady=(24, 12))
        form = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=12)
        form.pack(fill="both", expand=True, padx=24, pady=8)
        form.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form, text="Treatment Type:", font=("Arial", 14), anchor="w", text_color="#334155").grid(row=0, column=0, sticky="w", padx=12, pady=(18, 6))
        self.type_entry = ctk.CTkEntry(form, height=36, font=("Arial", 13))
        self.type_entry.grid(row=0, column=1, sticky="ew", padx=12, pady=(18, 6))
        self.type_entry.insert(0, prescription.treatm_type)

        ctk.CTkLabel(form, text="Content:", font=("Arial", 14), anchor="w", text_color="#334155").grid(row=1, column=0, sticky="nw", padx=12, pady=(6, 12))
        self.content_entry = ctk.CTkTextbox(form, height=100, font=("Arial", 13), corner_radius=8)
        self.content_entry.grid(row=1, column=1, sticky="ew", padx=12, pady=(6, 12))
        self.content_entry.insert("1.0", prescription.content)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 12, "bold"))
        self.error_label.pack(pady=(0, 4))

        ctk.CTkButton(
            self,
            text="💾 Save Changes",
            fg_color="#2563eb",
            hover_color="#1e40af",
            font=("Arial", 14, "bold"),
            height=42,
            width=180,
            corner_radius=8,
            command=self.submit
        ).pack(pady=(8, 20))

    def submit(self):
        treatm_type = self.type_entry.get().strip()
        content = self.content_entry.get("1.0", "end").strip()
        if not treatm_type or not content:
            self.error_label.configure(text="All fields are required.")
            return
        try:
            update_prescription(self.prescription.prescription_id, treatm_type, content)
            self.destroy()
        except Exception as e:
            self.error_label.configure(text=f"Error: {e}")