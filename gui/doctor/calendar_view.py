import customtkinter as ctk
from services.doctor_services import load_appointment_slots_by_doctor
from models.appointmnet_slot import AppointmentSlot
from tkcalendar import Calendar
from services.patient_services import get_patient_by_id
from datetime import datetime, timedelta

class CalendarView(ctk.CTkFrame):
    def __init__(self, master, doctor):
        super().__init__(master, fg_color="#121927")
        self.doctor = doctor

        # Title
        ctk.CTkLabel(
            self,
            text="📅 Appointment Calendar",
            font=("Helvetica", 28, "bold"),
            text_color="#63B3ED"
        ).pack(pady=(30, 10))

        # Card-like container for calendar and slots
        card = ctk.CTkFrame(self, corner_radius=25, fg_color="#1B263B")
        card.pack(pady=24, padx=40, fill="both", expand=True)

        # Calendar widget
        self.calendar = Calendar(card, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(pady=20, padx=30, anchor="n")

        # Add Slot button
        ctk.CTkButton(
            card,
            text="Add Slot",
            font=("Helvetica", 14, "bold"),
            fg_color="#2563eb",
            hover_color="#1e40af",
            command=self.open_add_slot_dialog
        ).pack(pady=(0, 10))

        # Slots list
        self.slots_frame = ctk.CTkFrame(card, fg_color="#0D1B2A", corner_radius=18)
        self.slots_frame.pack(fill="x", padx=40, pady=20)
        self.show_slots_for_selected_date()

        self.calendar.bind("<<CalendarSelected>>", lambda e: self.show_slots_for_selected_date())

    def show_slots_for_selected_date(self):
        for widget in self.slots_frame.winfo_children():
            widget.destroy()
        selected_date = self.calendar.get_date()
        slots = [s for s in load_appointment_slots_by_doctor(self.doctor.doctor_id) if s.start_time.startswith(selected_date)]

        # Header row
        header = ctk.CTkFrame(self.slots_frame, fg_color="#23304a")
        header.pack(fill="x", padx=0, pady=(0, 8))
        ctk.CTkLabel(header, text="Start", font=("Helvetica", 14, "bold"), width=120, text_color="#63B3ED").pack(side="left", padx=8)
        ctk.CTkLabel(header, text="End", font=("Helvetica", 14, "bold"), width=120, text_color="#63B3ED").pack(side="left", padx=8)
        ctk.CTkLabel(header, text="Booked", font=("Helvetica", 14, "bold"), width=80, text_color="#63B3ED").pack(side="left", padx=8)
        ctk.CTkLabel(header, text="Patient", font=("Helvetica", 14, "bold"), width=180, text_color="#63B3ED").pack(side="left", padx=8)

        if not slots:
            ctk.CTkLabel(
                self.slots_frame,
                text="No slots for this day.",
                font=("Helvetica", 15),
                text_color="#F0EDEE"
            ).pack(pady=16)
        else:
            for slot in slots:
                # Format times
                try:
                    start_time = datetime.strptime(slot.start_time, "%Y-%m-%d %H:%M")
                    end_time = start_time + timedelta(hours=1)
                    start_str = start_time.strftime("%H:%M")
                    end_str = end_time.strftime("%H:%M")
                except Exception:
                    start_str = slot.start_time
                    end_str = ""

                booked = "✓" if slot.is_booked else "⏳"
                booked_color = "#be123c" if slot.is_booked else "#22c55e"
                patient_name = ""
                if slot.is_booked and slot.selected_by:
                    patient = get_patient_by_id(slot.selected_by)
                    if patient:
                        patient_name = f"{patient.name} {patient.surname}"

                row = ctk.CTkFrame(self.slots_frame, fg_color="#0D1B2A")
                row.pack(fill="x", padx=0, pady=2)
                ctk.CTkLabel(row, text=start_str, font=("Helvetica", 13), width=120, text_color="#F0EDEE").pack(side="left", padx=8)
                ctk.CTkLabel(row, text=end_str, font=("Helvetica", 13), width=120, text_color="#F0EDEE").pack(side="left", padx=8)
                ctk.CTkLabel(row, text=booked, font=("Helvetica", 13, "bold"), width=80, text_color=booked_color).pack(side="left", padx=8)
                ctk.CTkLabel(row, text=patient_name, font=("Helvetica", 13), width=180, text_color="#F0EDEE").pack(side="left", padx=8)
    
    def open_add_slot_dialog(self):
        import tkinter.simpledialog as sd
        from services.doctor_services import add_appointment_slot

        selected_date = self.calendar.get_date()
        start_time = sd.askstring("Start Time", f"Enter start time (HH:MM) for {selected_date}:")

        if start_time:
            start_dt = f"{selected_date} {start_time}"
            add_appointment_slot(self.doctor.doctor_id, start_dt)
            self.show_slots_for_selected_date()
