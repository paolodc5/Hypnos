# gui/doctor/prescription_tab.py
import customtkinter as ctk

def show_prescriptions(parent, doctor_id):
    ctk.CTkLabel(parent, text="Create Prescription", font=("Arial", 16)).pack(pady=10)
    
    # Simulated patient selector
    ctk.CTkLabel(parent, text="Patient ID").pack()
    patient_entry = ctk.CTkEntry(parent)
    patient_entry.pack()

    # Prescription content
    ctk.CTkLabel(parent, text="Prescription Content").pack()
    content_text = ctk.CTkTextbox(parent, height=100, width=400)
    content_text.pack(pady=10)

    def submit():
        patient = patient_entry.get()
        content = content_text.get("1.0", "end").strip()
        print(f"Saving prescription for Doctor {doctor_id}, Patient {patient}:\n{content}")

    ctk.CTkButton(parent, text="Submit", command=submit).pack(pady=10)
