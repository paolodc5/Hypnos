# gui/doctor/note_tab.py

import customtkinter as ctk
from services.doctor_services import write_note, get_patient_notes


def show_notes(parent, doctor_id: int):
    # Title
    ctk.CTkLabel(parent, text="Patient Notes", font=("Arial", 16)).pack(pady=10)

    # Patient ID input
    patient_id_var = ctk.StringVar()
    ctk.CTkLabel(parent, text="Enter Patient ID").pack()
    patient_entry = ctk.CTkEntry(parent, textvariable=patient_id_var)
    patient_entry.pack(pady=5)

    # Frame to show notes
    notes_display = ctk.CTkTextbox(parent, height=200, width=600)
    notes_display.pack(pady=10)
    notes_display.configure(state="disabled")

    def load_notes():
        patient_id = patient_id_var.get()
        if not patient_id.isdigit():
            return

        notes = get_patient_notes(int(patient_id))  # list of rows
        notes_display.configure(state="normal")
        notes_display.delete("1.0", "end")

        for note in notes:
            date = note["Date"]
            content = note["Content"]
            notes_display.insert("end", f"[{date}] {content}\n\n")

        notes_display.configure(state="disabled")

    ctk.CTkButton(parent, text="Load Notes", command=load_notes).pack()

    # --- Section: Add New Note ---
    ctk.CTkLabel(parent, text="Write New Note").pack(pady=10)
    new_note_text = ctk.CTkTextbox(parent, height=100, width=600)
    new_note_text.pack()

    def submit_note():
        patient_id = patient_id_var.get()
        content = new_note_text.get("1.0", "end").strip()
        if patient_id.isdigit() and content:
            write_note(int(patient_id), doctor_id, content)
            new_note_text.delete("1.0", "end")
            load_notes()  # reload notes to show the new one

    ctk.CTkButton(parent, text="Submit Note", command=submit_note).pack(pady=10)
