import customtkinter as ctk
from services.doctor_services import write_note

class AddNoteDialog(ctk.CTkToplevel):
    def __init__(self, master, patient, doctor_id=None):
        super().__init__(master)
        self.title("📝 Add Note")
        self.geometry("480x360")
        self.resizable(False, False)
        self.configure(fg_color="#f8fafc")

        self.patient = patient
        self.doctor_id = doctor_id or getattr(patient, "doctor_id", None)

        # Layout grid config
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            self,
            text="📝 New Note",
            font=("Arial", 20, "bold"),
            text_color="#1e3a8a"
        ).grid(row=0, column=0, pady=(24, 12), padx=20, sticky="ew")

        # Form frame
        form = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=12)
        form.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 8))
        form.grid_columnconfigure(0, weight=1)

        # Label
        ctk.CTkLabel(
            form,
            text="Note Content:",
            font=("Arial", 14),
            anchor="w",
            text_color="#334155"
        ).grid(row=0, column=0, sticky="nw", padx=12, pady=(18, 6))

        # Textbox
        self.content_entry = ctk.CTkTextbox(
            form,
            height=120,
            font=("Arial", 13),
            corner_radius=8
        )
        self.content_entry.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))

        # Error message
        self.error_label = ctk.CTkLabel(
            self,
            text="",
            text_color="red",
            font=("Arial", 12, "bold")
        )
        self.error_label.grid(row=2, column=0, pady=(0, 4), padx=24, sticky="ew")

        # Confirmation button
        self.save_button = ctk.CTkButton(
            self,
            text="💾 Save Note",
            fg_color="#2563eb",
            hover_color="#1e40af",
            font=("Arial", 14, "bold"),
            height=42,
            width=180,
            corner_radius=8,
            command=self.submit
        )
        self.save_button.grid(row=3, column=0, pady=(8, 20), padx=24, sticky="ew")

    def submit(self):
        content = self.content_entry.get("1.0", "end").strip()
        if not content:
            self.error_label.configure(text="Content is required.")
            return
        try:
            write_note(
                pat_id=self.patient.patient_id,
                doctor_id=self.doctor_id,
                content=content
            )
            self.destroy()
        except Exception as e:
            self.error_label.configure(text=f"Error: {e}")
