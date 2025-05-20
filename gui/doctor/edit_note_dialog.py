import customtkinter as ctk
from services.doctor_services import update_note

# This class represents a dialog for editing a note.

class EditNoteDialog(ctk.CTkToplevel):
    def __init__(self, master, patient, note):
        super().__init__(master)
        self.title("✏️ Edit Note")
        self.geometry("480x360")
        self.resizable(False, False)
        self.note = note

        ctk.CTkLabel(self, text="Edit Note", font=("Arial", 20, "bold"), text_color="#1e3a8a").pack(pady=(24, 12))
        self.content_entry = ctk.CTkTextbox(self, height=120, font=("Arial", 13), corner_radius=8)
        self.content_entry.pack(fill="x", padx=24, pady=(0, 12))
        self.content_entry.insert("1.0", note.content)

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
        content = self.content_entry.get("1.0", "end").strip()
        if not content:
            self.error_label.configure(text="Content is required.")
            return
        try:
            update_note(self.note.note_id, content)
            self.destroy()
        except Exception as e:
            self.error_label.configure(text=f"Error: {e}")