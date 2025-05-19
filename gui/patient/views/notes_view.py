from .base_view import BaseView
import customtkinter as ctk
import tkinter.simpledialog

class NotesView(BaseView):
    def show(self):
        self.app.clear_content()

        self.app.patient.load_notes()  # Load notes from the database
        doctor_notes = self.app.patient.doctor_notes
        patient_notes = self.app.patient.patient_notes

        # Doctor's notes section
        ctk.CTkLabel(
            self.app.content_frame,
            text="Doctor's Notes",
            font=("Helvetica", 22, "bold"),
            text_color="#63B3ED"
        ).pack(padx=30, pady=(20, 10), anchor="w")

        notes_scroll = ctk.CTkScrollableFrame(
            self.app.content_frame,
            fg_color="#121927",
            corner_radius=20,
            width=750,
            height=180,
            border_width=1,
            border_color="#2A3A60"
        )
        notes_scroll.pack(padx=30, pady=(0, 20), fill="both", expand=True)

        for note in doctor_notes:
            date_str = note.date.strftime("%d %B %Y") if hasattr(note.date, "strftime") else str(note.date)
            card = ctk.CTkFrame(notes_scroll, fg_color="#1B263B", corner_radius=15, border_width=1, border_color="#3A4A78", height=90)
            card.pack(fill="x", pady=8, padx=10)
            ctk.CTkLabel(card, text=f"{date_str} (Doctor)", font=("Helvetica", 14, "bold"), text_color="#89A9E1", anchor="w").pack(padx=15, pady=(12, 4), fill="x")
            ctk.CTkLabel(card, text=note.content, font=("Helvetica", 13), text_color="#D1D9F1", wraplength=700, justify="left", anchor="w").pack(padx=15, pady=(0, 12), fill="x")

        # Patient's notes section
        ctk.CTkLabel(
            self.app.content_frame,
            text="Your Notes",
            font=("Helvetica", 22, "bold"),
            text_color="#63B3ED"
        ).pack(padx=30, pady=(10, 10), anchor="w")

        patient_notes_scroll = ctk.CTkScrollableFrame(
            self.app.content_frame,
            fg_color="#121927",
            corner_radius=20,
            width=750,
            height=180,
            border_width=1,
            border_color="#2A3A60"
        )
        patient_notes_scroll.pack(padx=30, pady=(0, 20), fill="both", expand=True)

        for note in patient_notes:
            date_str = note.date.strftime("%d %B %Y") if hasattr(note.date, "strftime") else str(note.date)
            card = ctk.CTkFrame(patient_notes_scroll, fg_color="#1B263B", corner_radius=15, border_width=1, border_color="#3A4A78", height=90)
            card.pack(fill="x", pady=8, padx=10)
            ctk.CTkLabel(card, text=f"{date_str} (You)", font=("Helvetica", 14, "bold"), text_color="#89A9E1", anchor="w").pack(padx=15, pady=(12, 4), fill="x")
            ctk.CTkLabel(card, text=note.content, font=("Helvetica", 13), text_color="#D1D9F1", wraplength=700, justify="left", anchor="w").pack(padx=15, pady=(0, 12), fill="x")

            edit_btn = ctk.CTkButton(
                card,
                text="Edit",
                width=60,
                fg_color="#63B3ED",
                hover_color="#7A8FF7",
                font=("Helvetica", 12, "bold"),
                command=lambda n=note: self.edit_note_dialog(n)
            )
            edit_btn.pack(side="right", padx=15, pady=10)

            delete_btn = ctk.CTkButton(
                card,
                text="Delete",
                width=60,
                fg_color="#E57373",
                hover_color="#FF8A80",
                font=("Helvetica", 12, "bold"),
                command=lambda n=note: self.delete_note_confirm(n)
            )
            delete_btn.pack(side="right", padx=5, pady=10)

        # Input section for adding a new note
        input_frame = ctk.CTkFrame(
            self.app.content_frame,
            fg_color="#121927",
            corner_radius=20,
            border_width=1,
            border_color="#2A3A60",
            height=140
        )
        input_frame.pack(fill="x", padx=30, pady=(0, 30))

        input_inner_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        input_inner_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.note_entry = ctk.CTkTextbox(
            input_inner_frame,
            fg_color="#1B263B",
            text_color="#F0F4FF",
            corner_radius=12,
            font=("Helvetica", 14)
        )
        self.note_entry.pack(side="left", fill="both", expand=True, padx=(0,15))

        save_btn = ctk.CTkButton(
            input_inner_frame,
            text="Add Note",
            width=140,
            height=50,
            fg_color="#637DEE",
            hover_color="#7A8FF7",
            font=("Helvetica", 16, "bold"),
            command=self.save_note
        )
        save_btn.pack(side="left", pady=(10,10))

    def save_note(self):
        content = self.note_entry.get("1.0", "end").strip()
        if content:
            self.app.patient.add_note(content)
            self.show()  # Refresh the notes view

    def edit_note_dialog(self, note):
        import tkinter.simpledialog
        new_content = tkinter.simpledialog.askstring("Edit Note", "Modify your note:", initialvalue=note.content, parent=self.app)
        if new_content is not None and new_content.strip():
            self.app.patient.update_note(note.note_id, new_content.strip())
            self.show()  # Refresh notes

    def delete_note_confirm(self, note):
        import tkinter.messagebox
        if tkinter.messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?", parent=self.app):
            self.app.patient.update_note(note.note_id, delete=True)
            self.show()  # Refresh notes