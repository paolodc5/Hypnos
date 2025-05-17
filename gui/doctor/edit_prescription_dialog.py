import customtkinter as ctk
from services.doctor_services import update_prescription, get_prescription_types

class EditPrescriptionDialog(ctk.CTkToplevel):
    def __init__(self, master, patient, prescription):
        super().__init__(master)
        self.title("Edit Prescription")
        self.geometry("400x400")
        self.resizable(False, False)
        self.prescription = prescription

        ctk.CTkLabel(self, text="Edit Prescription", font=("Arial", 18, "bold")).pack(pady=(18, 10))
        form = ctk.CTkFrame(self, fg_color="#f8fafc", corner_radius=12)
        form.pack(fill="both", expand=True, padx=16, pady=8)

        # Type ComboBox
        ctk.CTkLabel(form, text="Type:", anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=2)
        types = get_prescription_types()
        self.type_map = {name: tid for tid, name in types}
        self.type_combo = ctk.CTkComboBox(form, values=list(self.type_map.keys()))
        # Set current value
        current_type = next((name for name, tid in self.type_map.items() if tid == prescription.type_id), "")
        self.type_combo.set(current_type)
        self.type_combo.grid(row=0, column=1, padx=10, pady=2)

        # Content
        ctk.CTkLabel(form, text="Content:", anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.content_entry = ctk.CTkTextbox(form, height=80)
        self.content_entry.grid(row=1, column=1, padx=10, pady=2)
        self.content_entry.insert("1.0", prescription.content)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 12, "bold"))
        self.error_label.pack(pady=(0, 0))

        ctk.CTkButton(self, text="Save", fg_color="#2563eb", hover_color="#1e40af", command=self.submit).pack(pady=18)

    def submit(self):
        type_name = self.type_combo.get().strip()
        content = self.content_entry.get("1.0", "end").strip()
        if not type_name or not content:
            self.error_label.configure(text="All fields are required.")
            return
        type_id = self.type_map.get(type_name)
        try:
            update_prescription(
                prescription_id=self.prescription.prescription_id,
                type_id=type_id,
                content=content
            )
            self.destroy()
        except Exception as e:
            self.error_label.configure(text=f"Error: {e}")