from .base_view import BaseView
import customtkinter as ctk

class NotesView(BaseView):
    def show(self):
        self.app.clear_content()

        notes = self.app.patient.get_notes()  # List of note objects with .date and .content

        # Header
        header = ctk.CTkLabel(
            self.app.content_frame,
            text="Your Notes",
            font=("Helvetica", 26, "bold"),
            text_color="#63B3ED",
            anchor="w"
        )
        header.pack(padx=30, pady=(20, 10), fill="x")

        # Scrollable container for notes
        notes_scroll = ctk.CTkScrollableFrame(
            self.app.content_frame,
            fg_color="#121927",
            corner_radius=20,
            width=750,
            height=380,
            border_width=1,
            border_color="#2A3A60"
        )
        notes_scroll.pack(padx=30, pady=(0, 20), fill="both", expand=True)

        # Sort notes newest first if date is sortable
        try:
            notes = sorted(notes, key=lambda n: n.date, reverse=True)
        except Exception:
            pass

        for note in notes:
            # Format date nicely
            date_str = note.date.strftime("%d %B %Y") if hasattr(note.date, "strftime") else str(note.date)

            card = ctk.CTkFrame(
                notes_scroll,
                fg_color="#1B263B",
                corner_radius=15,
                border_width=1,
                border_color="#3A4A78",
                height=90
            )
            card.pack(fill="x", pady=8, padx=10)

            # Date title
            ctk.CTkLabel(
                card,
                text=f"{date_str} Notes",
                font=("Helvetica", 14, "bold"),
                text_color="#89A9E1",
                anchor="w"
            ).pack(padx=15, pady=(12, 4), fill="x")

            # Note content
            ctk.CTkLabel(
                card,
                text=note.content,
                font=("Helvetica", 13),
                text_color="#D1D9F1",
                wraplength=700,
                justify="left",
                anchor="w"
            ).pack(padx=15, pady=(0, 12), fill="x")

        # Input section below notes
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