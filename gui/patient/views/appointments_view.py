from .base_view import BaseView
import customtkinter as ctk
from services.patient_services import get_appointmentslot_by_patient, load_appointment_slots_by_doctor, book_appointment, get_doctor_name
from tkinter import messagebox
from models.appointment import Appointment
from models.appointment_slot import AppointmentSlot
from datetime import datetime, timedelta
from tkcalendar import Calendar

class AppointmentView(BaseView):
    def show(self):
        self.app.clear_content()

        # Create a scrollable frame to hold all content
        scrollable = ctk.CTkScrollableFrame(self.app.content_frame, corner_radius=25, fg_color="#1B263B")
        scrollable.pack(pady=40, padx=60, fill="both", expand=True)

        # Title for the page
        title = ctk.CTkLabel(
            scrollable,
            text="My Appointments",
            font=("Helvetica", 28, "bold"),
            text_color="#63B3ED"
        )
        title.pack(pady=(30, 10))

        # Show the appointments the patient has booked
        self.show_patient_appointments(scrollable)

        # Calendar for selecting a new appointment slot
        self.show_calendar(scrollable)

    def show_patient_appointments(self, parent_frame):
        """
        Displays a list of appointments the patient has already booked.
        """
        appointments_frame = ctk.CTkFrame(parent_frame, fg_color="#0D1B2A", corner_radius=18)
        appointments_frame.pack(pady=18, padx=40, fill="x")

        ctk.CTkLabel(appointments_frame, text="Your Booked Appointments", font=("Helvetica", 20, "bold"), text_color="#63B3ED").pack(anchor="w", padx=20, pady=(10, 5))

        appointments = get_appointmentslot_by_patient(self.app.patient.patient_id)
        doctor_name = get_doctor_name(self.app.patient.doctor_id)
        
        if not appointments:
            ctk.CTkLabel(appointments_frame, text="No booked appointments.", font=("Helvetica", 14), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=10)
        else:
            for appointment in appointments:
                status_color = "#66d9cc" if appointment.is_booked else "#f97316"  # Assuming is_booked is the flag
                status = f"Status: {'Confirmed' if appointment.is_booked else 'Pending'}"
                
                # Create the label displaying the appointment details
                ctk.CTkLabel(
                appointments_frame, 
                text=f"Doctor {doctor_name} | Date: {appointment.start_time.strftime('%Y-%m-%d %H:%M')} | {status}",
                font=("Helvetica", 15), 
                text_color=status_color,
                justify="left"
            ).pack(anchor="w", padx=30, pady=4)


    def show_calendar(self, parent_frame):
        """
        Displays a calendar where the patient can choose a date to see available appointment slots.
        """
        calendar_frame = ctk.CTkFrame(parent_frame, fg_color="#0D1B2A", corner_radius=18)
        calendar_frame.pack(pady=18, padx=40, fill="x")

        ctk.CTkLabel(calendar_frame, text="Select a Date to Book an Appointment", font=("Helvetica", 20, "bold"), text_color="#63B3ED").pack(anchor="w", padx=20, pady=(10, 5))

        # Calendar Widget
        self.calendar = Calendar(
    calendar_frame,
    selectmode='day',
    date_pattern="yyyy-mm-dd",
    background="#1B263B",          # calendar body bg
    foreground="#63B3ED",          # text color
    weekendforeground="#63B3ED",   # weekend text
    headersforeground="#63B3ED",   # header text
    bordercolor="#63B3ED",         # border of the calendar
    font=("Helvetica", 13),        # font inside cells
    firstweekday="monday"
)


        self.calendar.pack(pady=20, padx=30, anchor="n")

        # Slots list container
        self.slots_frame = ctk.CTkFrame(calendar_frame, fg_color="#0D1B2A", corner_radius=18)
        self.slots_frame.pack(fill="x", padx=40, pady=20)

        self.show_slots_for_selected_date()

        self.calendar.bind("<<CalendarSelected>>", lambda e: self.show_slots_for_selected_date())

    def show_slots_for_selected_date(self):
        for widget in self.slots_frame.winfo_children():
            widget.destroy()
        
        selected_date = self.calendar.get_date()
        slots = [s for s in load_appointment_slots_by_doctor(self.app.patient.doctor_id, selected_date) if s.start_time.startswith(selected_date)]

        # Header row
        header = ctk.CTkFrame(self.slots_frame, fg_color="#23304a")
        header.pack(fill="x", padx=0, pady=(0, 8))
        ctk.CTkLabel(header, text="Start", font=("Helvetica", 14, "bold"), width=120, text_color="#63B3ED").pack(side="left", padx=8)
        ctk.CTkLabel(header, text="End", font=("Helvetica", 14, "bold"), width=120, text_color="#63B3ED").pack(side="left", padx=8)
        ctk.CTkLabel(header, text="Available", font=("Helvetica", 14, "bold"), width=80, text_color="#63B3ED").pack(side="left", padx=8)
        ctk.CTkButton(header, text="ℹ️",font=("Helvetica", 14),width=50, fg_color="#23304a", text_color="#63B3ED", command=self.show_room_legend).pack(side="left", padx=8)

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

                booked = "✖" if slot.is_booked else "✔"
                booked_color = "#be123c" if slot.is_booked else "#22c55e"

                row = ctk.CTkFrame(self.slots_frame, fg_color="#0D1B2A")
                row.pack(fill="x", padx=0, pady=2)
                ctk.CTkLabel(row, text=start_str, font=("Helvetica", 13), width=120, text_color="#F0EDEE").pack(side="left", padx=8)
                ctk.CTkLabel(row, text=end_str, font=("Helvetica", 13), width=120, text_color="#F0EDEE").pack(side="left", padx=8)
                ctk.CTkLabel(row, text=booked, font=("Helvetica", 13, "bold"), width=80, text_color=booked_color).pack(side="left", padx=8)

                if not slot.is_booked:
                    book_button = ctk.CTkButton(
                        row,
                        text="Book Appointment",
                        font=("Helvetica", 12, "bold"),
                        fg_color="#2563eb",
                        hover_color="#1e40af",
                        width=150,
                        command=lambda slot_id=slot.slot_id: self.book_appointment(slot_id)
                    )
                    book_button.pack(side="left", padx=8, pady=8)
                else:
                    # If the slot is booked, display a non-clickable button
                    ctk.CTkButton(
                        row,
                        text="Booked",
                        font=("Helvetica", 12, "bold"),
                        fg_color="#d1d5db",  # Gray color for booked slots
                        width=150,
                        state="disabled"  # Disable the button
                    ).pack(side="left", padx=8, pady=8)
    
    def book_appointment(self, slot_id):
        """
        Handle the booking of an available appointment slot.
        """
        try:
            # Call the booking service to finalize the appointment
            status = book_appointment(slot_id, self.app.patient.patient_id)
            if status:
                messagebox.showinfo("Success", "Your appointment has been booked!")
                self.show_slots_for_selected_date()  # Refresh the view after booking
            else:
                messagebox.showwarning("Warning", "Unable to book this appointment, please try again.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_room_legend(self):
        popup = ctk.CTkToplevel()
        popup.title("Room Number Info")
        popup.geometry("360x160")
        popup.configure(fg_color="#1B263B")

        ctk.CTkLabel(
            popup,
            text="✖ - Appointment is booked\n✔ - Appointment is available",
            font=("Helvetica", 14),
            text_color="#F0EDEE",
            justify="left",
            wraplength=320
        ).pack(padx=20, pady=30)

        ctk.CTkButton(
            popup,
            text="Close",
            command=popup.destroy,
            fg_color="#63B3ED",
            hover_color="#7A8FF7",
            text_color="#121927"
        ).pack(pady=10)
