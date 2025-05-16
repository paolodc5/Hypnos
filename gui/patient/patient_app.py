import customtkinter as ctk
from models.patient import Patient
import os
import sqlite3
from PIL import Image, ImageTk
from datetime import datetime

class PatientApp(ctk.CTk):
    def __init__(self, patient: Patient):
        super().__init__()
        self.title(f"Hypnos - Patient Dashboard")
        self.geometry("1100x900")
        self.patient = patient
        # self.patient.load_patients()

        self.setup_gui()
        self.load_home()


    def setup_gui(self):
        # Set appearance to dark, matching your brand
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")  # Optional, as we'll use custom colors

        # Set up the sidebar with deep navy and rounded edges
        self.sidebar = ctk.CTkFrame(self, width=240, fg_color="#0D1B2A", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        # Set up the main window with dark background
        self.content_frame = ctk.CTkFrame(self, fg_color="#1B263B")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # --- Logo ---
        logo_path = os.path.join(os.path.dirname(__file__), "../images/Hypnos_Logo.png")
        logo_image = ctk.CTkImage(Image.open(logo_path), size=(100, 100))
        ctk.CTkLabel(self.sidebar, image=logo_image, text="", bg_color="transparent").pack(pady=(30, 10))

        # --- Sidebar Title ---
        ctk.CTkLabel(
            self.sidebar,
            text="HYPNOS",
            font=("Helvetica", 22, "bold"),
            text_color="#F0EDEE"
        ).pack(pady=(0, 20))

        # --- Buttons style ---
        button_style = {
            "width": 180,
            "corner_radius": 20,
            "font": ("Helvetica", 16, "bold"),
            "fg_color": "#3366cc",
            "hover_color": "#66d9cc",
        }

        # --- Navigation buttons ---
        ctk.CTkButton(self.sidebar, text="Home", command=self.load_home, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="My Profile", command=self.load_my_profile, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Prescriptions", command=self.load_prescriptions, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Doctor", command=self.load_doctor_profile, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Sleep Records", command=self.load_sleep_records, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Questionnaires", command=self.load_questionnaires, **button_style).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Notes", command=self.load_notes, **button_style).pack(pady=8)

        # --- Spacer ---
        ctk.CTkFrame(self.sidebar, fg_color="transparent", height=1).pack(expand=True, fill="both")

        # --- FAQ Circle Button ---
        ctk.CTkButton(self.sidebar, text="FAQ", **button_style).pack(pady=(0, 15))

        # --- Appearance Mode Switch ---
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar, values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
            width=180, fg_color="#3366cc", corner_radius=20,
            font=("Helvetica", 14, "bold")
        )
        self.appearance_mode_menu.pack(pady=(0, 30))

    def change_appearance_mode_event(self, new_appearance_mode):
            ctk.set_appearance_mode(new_appearance_mode)


    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            if widget not in [self.sidebar]:
                widget.destroy()


    def load_home(self):
        self.clear_content()

        # --- Main card ---
        card = ctk.CTkFrame(self.content_frame, corner_radius=30, fg_color="#1B263B", border_width=0)
        card.pack(pady=40, padx=80, fill="both", expand=True)

        # Add logo at top center
        logo_path = os.path.join(os.path.dirname(__file__), "../images/Hypnos.png")
        logo_image = ctk.CTkImage(Image.open(logo_path), size=(120, 120))
        ctk.CTkLabel(card, image=logo_image, text="", bg_color="transparent").pack(pady=(20, 10))

        # Welcome title
        welcome_title = ctk.CTkLabel(
            card,
            text=f"🌙 Hello {self.patient.name} {self.patient.surname}",
            font=("Helvetica", 30, "bold"),
            text_color="#F0EDEE"
        )
        welcome_title.pack(pady=(0, 10))

        # Subtitle in soft grey-blue
        subtitle = ctk.CTkLabel(
            card,
            text="Track, understand, and improve your sleep habits.",
            font=("Helvetica", 16),
            text_color="#CBD5E0"
        )
        subtitle.pack(pady=(0, 30))

        # --- Quick Actions ---
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(pady=10)

        button_style = {
            "width": 180,
            "height": 55,
            "corner_radius": 25,
            "font": ("Helvetica", 15, "bold")
        }

        ctk.CTkButton(
            actions_frame, text="📊 Sleep Records", command=self.load_sleep_records,
            fg_color="#63B3ED", hover_color="#7CC4F0", **button_style
        ).pack(side="left", padx=12)

        ctk.CTkButton(
            actions_frame, text="💊 Prescriptions", command=self.load_prescriptions,
            fg_color="#9F7AEA", hover_color="#B084F7", **button_style
        ).pack(side="left", padx=12)

        ctk.CTkButton(
            actions_frame, text="👩‍⚕️ My Doctor", command=self.load_doctor_profile,
            fg_color="#FFB347", hover_color="#FFC980", **button_style
        ).pack(side="left", padx=12)

        # Divider
        ctk.CTkFrame(card, height=1, fg_color="#2D3748").pack(fill="x", padx=60, pady=40)

        # --- Motivational Block ---
        tip_frame = ctk.CTkFrame(card, fg_color="#0D1B2A", corner_radius=20)
        tip_frame.pack(pady=10, padx=50, fill="x")

        tip_label = ctk.CTkLabel(
            tip_frame,
            text="💡 Tip:\nConsistent sleep and wake times support your circadian rhythm.\nLet’s build that routine.",
            font=("Helvetica", 16, "italic"),
            text_color="#63B3ED",
            justify="center"
        )
        tip_label.pack(pady=20, padx=20)

    def load_my_profile(self):
        self.clear_content()

        # --- Main card with dark background ---
        card = ctk.CTkFrame(self.content_frame, corner_radius=25, fg_color="#1B263B")
        card.pack(pady=50, padx=60, fill="both", expand=True)

        # --- Title with accent color ---
        title = ctk.CTkLabel(
            card,
            text="👤 My Profile",
            font=("Helvetica", 28, "bold"),
            text_color="#63B3ED"
        )
        title.pack(pady=(30, 10))

        # --- Info block in semi-transparent dark frame ---
        info_frame = ctk.CTkFrame(card, fg_color="#0D1B2A", corner_radius=20)
        info_frame.pack(pady=30, padx=50, fill="x")

        label_style = {
            "font": ("Helvetica", 16),
            "text_color": "#F0EDEE"
        }

        ctk.CTkLabel(info_frame, text=f"👤 Name: {self.patient.name} {self.patient.surname}", **label_style).pack(pady=10, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"🎂 Birthdate: {self.patient.birth_date}", **label_style).pack(pady=10, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"📧 Email: {self.patient.email}", **label_style).pack(pady=10, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"📞 Phone: {self.patient.phone_number}", **label_style).pack(pady=10, anchor="w", padx=20)

        # --- Decorative divider ---
        ctk.CTkFrame(card, height=2, fg_color="#63B3ED").pack(fill="x", padx=80, pady=30)

        # --- Update Button ---
        update_button = ctk.CTkButton(
            card,
            text="✏️ Update Info",
            fg_color="#3366CC",
            hover_color="#5588DD",
            width=180,
            height=50,
            corner_radius=25,
            font=("Helvetica", 16, "bold"),
            command=self.show_update_form
        )
        update_button.pack(pady=20)







    def load_sleep_records(self, selected_day=None):
        self.clear_content()

        # Example: Two days of sleep records (replace with your real data)
        sleep_records = {
            "2024-05-15": {
                "total_sleep": "7h 30m",
                "time_in_bed": "8h 15m",
                "efficiency": "91%",
                "hr_during_sleep": "65 bpm",
                "Sleep_Score": 82,
                "latency": "15 min",
                "rem_phase": "1h 20m",
                "deep_phase": "1h 45m",
                "light_phase": "4h 25m",
            },
            "2024-05-16": {
                "total_sleep": "6h 50m",
                "time_in_bed": "7h 40m",
                "efficiency": "89%",
                "hr_during_sleep": "67 bpm",
                "Sleep_Score": 75,
                "latency": "18 min",
                "rem_phase": "1h 10m",
                "deep_phase": "1h 30m",
                "light_phase": "4h 10m",
            }
        }
        days = list(sleep_records.keys())
        if not days:
            ctk.CTkLabel(self.content_frame, text="No sleep records available.", font=("Helvetica", 18), text_color="red").pack(pady=40)
            return
        if selected_day is None or selected_day not in days:
            selected_day = days[0]
        record = sleep_records[selected_day]

        # --- Sliding bar for days ---
        bar_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        bar_frame.pack(fill="x", padx=30, pady=(20, 10))

        for day in days:
            btn = ctk.CTkButton(
                bar_frame,
                text=day,
                fg_color="#5a86ff" if day == selected_day else "#d6d9e6",
                text_color="white" if day == selected_day else "#204080",
                corner_radius=15,
                command=lambda d=day: self.load_sleep_records(selected_day=d),
                width=120
            )
            btn.pack(side="left", padx=10)

        # --- Main card ---
        card = ctk.CTkFrame(self.content_frame, corner_radius=20, fg_color="#f0f4f7", border_width=5, border_color="#d6d9e6")
        card.pack(pady=20, padx=50, fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(card, text=f"Sleep Records - {self.patient.name} {self.patient.surname} ({selected_day})", font=("Helvetica", 24, "bold"), text_color="#5a86ff")
        title.pack(pady=(20, 10))

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=30, pady=5)

        widget_defs = [
            (0, 0, "Total Sleep", "total_sleep", "7h 30m"),
            (0, 1, "Time in Bed", "time_in_bed", "8h 15m"),
            (1, 0, "Sleep Efficiency", "efficiency", "91%"),
            (1, 1, "Avg HR During Sleep", "hr_during_sleep", "65 bpm"),
        ]

        for row, col, label, attr, default in widget_defs:
            widget = ctk.CTkFrame(grid_frame, corner_radius=15, fg_color="#d6d9e6", width=250, height=130)
            widget.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            container = ctk.CTkFrame(widget, fg_color="transparent")
            container.pack(fill="x", padx=15, pady=15)
            ctk.CTkLabel(container, text=label, font=("Helvetica", 22), text_color="#5a86ff").pack(side="left", expand=True, anchor="w")
            ctk.CTkLabel(container, text=record.get(attr, default), font=("Helvetica", 22, "bold"), text_color="#5a86ff").pack(side="right", anchor="e")

        # Widget 5: Sleep Score
        widget5 = ctk.CTkFrame(grid_frame, corner_radius=15, fg_color="#d6d9e6", width=510, height=130)
        widget5.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        container = ctk.CTkFrame(widget5, fg_color="transparent")
        container.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(container, text="Sleep Score", font=("Helvetica", 22), text_color="#5a86ff").pack(side="left", anchor="w")
        score = record.get("Sleep_Score", 66)
        ctk.CTkLabel(container, text=str(score), font=("Helvetica", 22, "bold"), text_color="#5a86ff").pack(side="right", anchor="e")
        progress_container = ctk.CTkFrame(widget5, fg_color="transparent")
        progress_container.pack(fill="x", padx=15, pady=(5, 10))
        score_bar = ctk.CTkProgressBar(progress_container, height=12, progress_color="#5a86ff")
        score_bar.set(float(score) / 100)
        score_bar.pack(fill="x")

        # Make columns and rows expandable
        for i in range(2):
            grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            grid_frame.grid_rowconfigure(i, weight=0)

        # Sleep Features Section Title
        features_title = ctk.CTkLabel(card, text="Sleep Features", font=("Helvetica", 20, "bold"), text_color="#204080")
        features_title.pack(pady=(20, 5), padx=30, anchor="w")

        # Features Frame (full width)
        features_frame = ctk.CTkFrame(card, fg_color="#e9ecf5", corner_radius=12)
        features_frame.pack(fill="x", padx=30, pady=(0, 20))

        features = [
            ("Total Sleep Amount", "total_sleep", "7h 30m"),
            ("Efficiency", "efficiency", "91%"),
            ("Latency", "latency", "15 min"),
            ("REM phase", "rem_phase", "1h 20m"),
            ("Deep state phase", "deep_phase", "1h 45m"),
            ("Light state phase", "light_phase", "4h 25m"),
        ]

        for name, attr, default in features:
            row = ctk.CTkFrame(features_frame, fg_color="transparent")
            row.pack(fill="x", pady=2, padx=10)
            # Fixed width for name label, no expand/fill
            ctk.CTkLabel(row, text=name, font=("Helvetica", 16), anchor="w", width=220, text_color="#204080").pack(side="left")
            # Value label right, no expand/fill
            ctk.CTkLabel(row, text=str(record.get(attr, default)), font=("Helvetica", 16, "bold"), anchor="e", text_color="#5a86ff").pack(side="right")

    def fetch_sleep_records(self):
        # Connect to your SQLite database
        conn = sqlite3.connect("insomnia_patient_30days.db")
        cursor = conn.cursor()
        # Adjust the table/column names as needed
        cursor.execute("""
            SELECT 
                date, total_sleep, time_in_bed, efficiency, hr_during_sleep, Sleep_Score,
                latency, rem_phase, deep_phase, light_phase
            FROM sleep_records
            WHERE patient_id = ?
            ORDER BY date DESC
            LIMIT 30
        """, (self.patient.patient_id,))
        rows = cursor.fetchall()
        conn.close()

        # Build a dict: {date: {...data...}}
        records = {}
        for row in rows:
            (date, total_sleep, time_in_bed, efficiency, hr_during_sleep, sleep_score,
            latency, rem_phase, deep_phase, light_phase) = row
            records[date] = {
                "total_sleep": total_sleep,
                "time_in_bed": time_in_bed,
                "efficiency": efficiency,
                "hr_during_sleep": hr_during_sleep,
                "Sleep_Score": sleep_score,
                "latency": latency,
                "rem_phase": rem_phase,
                "deep_phase": deep_phase,
                "light_phase": light_phase,
            }
        return records





    def show_update_form(self):
        self.clear_content()

        form_frame = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#f0f4f7")
        form_frame.pack(pady=50, padx=50, fill="both", expand=True)

        title = ctk.CTkLabel(form_frame, text="Update Profile Information", font=("Arial", 20, "bold"), text_color="#204080")
        title.pack(pady=(20, 10))

        # Email field
        email_label = ctk.CTkLabel(form_frame, text="Email:", font=("Arial", 14))
        email_label.pack(pady=(20, 5))
        self.email_entry = ctk.CTkEntry(form_frame, width=300)
        self.email_entry.insert(0, self.patient.email)
        self.email_entry.pack()

        # Phone field
        phone_label = ctk.CTkLabel(form_frame, text="Phone Number:", font=("Arial", 14))
        phone_label.pack(pady=(20, 5))
        self.phone_entry = ctk.CTkEntry(form_frame, width=300)
        self.phone_entry.insert(0, self.patient.phone_number)
        self.phone_entry.pack()

        # Save button
        save_button = ctk.CTkButton(
            form_frame, text="Save Changes", fg_color="#3366cc", hover_color="#5588dd",
            command=self.save_profile_changes
        )
        save_button.pack(pady=30)

    def save_profile_changes(self):
        new_email = self.email_entry.get()
        new_phone = self.phone_entry.get()

        # Aggiorna l'oggetto e salva (supponiamo ci sia un metodo .save())
        self.patient.email = new_email
        self.patient.phone_number = new_phone
        self.patient.save()  # implementa se non esiste

        # Torna al profilo aggiornato
        self.load_my_profile()

    def load_doctor_profile(self):
        self.clear_content()

        doctor = self.patient.get_doctor()

        # --- Main card with dark background ---
        card = ctk.CTkFrame(self.content_frame, corner_radius=25, fg_color="#1B263B")
        card.pack(pady=50, padx=60, fill="both", expand=True)

        # --- Title with accent color ---
        title = ctk.CTkLabel(
            card,
            text="👨‍⚕️ Your Sleep Specialist",
            font=("Helvetica", 28, "bold"),
            text_color="#63B3ED"
        )
        title.pack(pady=(30, 10))

        # --- Info block in semi-transparent dark frame ---
        info_frame = ctk.CTkFrame(card, fg_color="#0D1B2A", corner_radius=20)
        info_frame.pack(pady=30, padx=50, fill="x")

        label_style = {
            "font": ("Helvetica", 16),
            "text_color": "#F0EDEE"
        }

        ctk.CTkLabel(info_frame, text=f"👤 Name: {doctor.name} {doctor.surname}", **label_style).pack(pady=10, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"🩺 Specialty: {doctor.specialty}", **label_style).pack(pady=10, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"📧 Email: {doctor.email}", **label_style).pack(pady=10, anchor="w", padx=20)

        # --- Decorative divider ---
        ctk.CTkFrame(card, height=2, fg_color="#63B3ED").pack(fill="x", padx=80, pady=30)

        # --- Contact Button ---
        contact_button = ctk.CTkButton(
            card,
            text="✉️ Contact Doctor",
            fg_color="#3366CC",
            hover_color="#5588DD",
            width=200,
            height=50,
            corner_radius=25,
            font=("Helvetica", 16, "bold")
        )
        contact_button.pack(pady=20)


    def load_notes(self):
        self.clear_content()

        notes = self.patient.get_notes()  # List of note objects with .date and .content

        notes_label = ctk.CTkLabel(self.content_frame, text="Your Notes:", font=("Arial", 16))
        notes_label.pack(pady=10)

        header = ctk.CTkLabel(
            self.content_frame,
            text="Your Notes",
            font=("Helvetica", 26, "bold"),
            text_color="#63B3ED",
            anchor="w"
        )
        header.pack(padx=30, pady=(20, 10), fill="x")

        # Scrollable container for notes
        notes_scroll = ctk.CTkScrollableFrame(
            self.content_frame,
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

            # Note content, limited height, wrapped and left-aligned
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
        self.content_frame,
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
            self.patient.add_note(content)
            self.load_notes()






    def load_prescriptions(self):
        self.clear_content()

        title = ctk.CTkLabel(self.content_frame, text="My Prescriptions", font=("Arial", 24, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=20)

        # Icone esempio (da caricare precedentemente, anche PNG 32x32)
        """image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.drugs_icon = ctk.CTkImage(Image.open(os.path.join("assets/icons/pill.png")), size=(32, 32))
        self.sleep_icon = ctk.CTkImage(Image.open("assets/icons/bed.png"), size=(32, 32))
        self.exam_icon = ctk.CTkImage(Image.open("assets/icons/report.png"), size=(32, 32))"""

        # Bottoni per categorie
        self.prescriptions_button_1 = ctk.CTkButton(self.content_frame, text="Drugs", image=None, 
                                                    compound="top", command=self.show_drugs)
        self.prescriptions_button_1.grid(row=1, column=0, padx=40, pady=10)
        # self.prescriptions_button_1.place(x=50, y=50)
        

        self.prescriptions_button_2 = ctk.CTkButton(self.content_frame, text="Sleep Habits", image=None, 
                                                    compound="top", command=self.show_sleep_habits)
        self.prescriptions_button_2.grid(row=1, column=1, padx=40, pady=10)
        # self.prescriptions_button_2.place(x=150, y=50)

        self.prescriptions_button_3 = ctk.CTkButton(self.content_frame, text="Examinations", image=None, 
                                                    compound="top", command=self.show_examinations)
        self.prescriptions_button_3.grid(row=1, column=2, padx=40, pady=10)
        # self.prescriptions_button_3.place(x=250, y=50)

    # Drugs section in My prescriptions
    def show_drugs(self):
        self.clear_content()

        title = ctk.CTkLabel(self.content_frame, text="Prescribed Drugs", font=("Arial", 20, "bold"))
        title.pack(pady=(20, 10))

        # Dati mock
        drugs = [
            {"name": "Melatonin", "dosage": "3 mg", "instructions": "Take 1 tablet before bedtime"},
            {"name": "Zolpidem", "dosage": "5 mg", "instructions": "Take 1 tablet 30 minutes before sleep"},
            {"name": "Valerian Root", "dosage": "500 mg", "instructions": "Take 1 capsule in the evening"},
        ]

        for drug in drugs:
            frame = ctk.CTkFrame(self.content_frame)
            frame.pack(padx=20, pady=10, fill="x")

            name_label = ctk.CTkLabel(frame, text=f"{drug['name']} - {drug['dosage']}", font=("Arial", 14, "bold"))
            name_label.pack(anchor="w", padx=10, pady=5)

            instr_label = ctk.CTkLabel(frame, text=drug["instructions"], font=("Arial", 12))
            instr_label.pack(anchor="w", padx=10, pady=(0, 5))

    # Sleep habits section in My prescriptions
    def show_sleep_habits(self):
        self.clear_content()

        title = ctk.CTkLabel(self.content_frame, text="Recommended Sleep Habits", font=("Arial", 20, "bold"))
        title.pack(pady=(20, 10))

        habits = [
            "Maintain a consistent sleep schedule.",
            "Avoid caffeine and heavy meals before bedtime.",
            "Create a restful sleeping environment.",
            "Limit screen time before sleep.",
        ]

        for habit in habits:
            habit_label = ctk.CTkLabel(self.content_frame, text=f"• {habit}", font=("Arial", 12))
            habit_label.pack(anchor="w", padx=20, pady=5)

    # Instrumental examinations section in My prescriptions
    def show_examinations(self):
        self.clear_content()

        title = ctk.CTkLabel(self.content_frame, text="Scheduled Examinations", font=("Arial", 20, "bold"))
        title.pack(pady=(20, 10))

        exams = [
            {"name": "Polysomnography", "date": "2025-06-10", "location": "Sleep Center A"},
            {"name": "Home Sleep Test", "date": "2025-06-15", "location": "At Home"},
        ]

        for exam in exams:
            frame = ctk.CTkFrame(self.content_frame)
            frame.pack(padx=20, pady=10, fill="x")

            name_label = ctk.CTkLabel(frame, text=exam["name"], font=("Arial", 14, "bold"))
            name_label.pack(anchor="w", padx=10, pady=5)

            details_label = ctk.CTkLabel(frame, text=f"Date: {exam['date']} | Location: {exam['location']}", font=("Arial", 12))
            details_label.pack(anchor="w", padx=10, pady=(0, 5))

    def load_sleep_records(self, selected_day=None):
        self.clear_content()

        # Example sleep records (replace with your real data)
        sleep_records = {
            "2024-05-15": {
                "total_sleep": "7h 30m",
                "time_in_bed": "8h 15m",
                "efficiency": "91%",
                "hr_during_sleep": "65 bpm",
                "Sleep_Score": 82,
                "latency": "15 min",
                "rem_phase": "1h 20m",
                "deep_phase": "1h 45m",
                "light_phase": "4h 25m",
            },
            "2024-05-16": {
                "total_sleep": "6h 50m",
                "time_in_bed": "7h 40m",
                "efficiency": "89%",
                "hr_during_sleep": "67 bpm",
                "Sleep_Score": 75,
                "latency": "18 min",
                "rem_phase": "1h 10m",
                "deep_phase": "1h 30m",
                "light_phase": "4h 10m",
            }
        }

        days = list(sleep_records.keys())
        if not days:
            ctk.CTkLabel(self.content_frame, text="No sleep records available.", font=("Helvetica", 18), text_color="red").pack(pady=40)
            return

        if selected_day is None or selected_day not in days:
            selected_day = days[0]
        record = sleep_records[selected_day]

        # --- Top bar with day buttons ---
        bar_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        bar_frame.pack(fill="x", padx=30, pady=(20, 15))

        for day in days:
            btn = ctk.CTkButton(
                bar_frame,
                text=day,
                fg_color="#5a86ff" if day == selected_day else "#2D3748",
                text_color="white",
                hover_color="#7CC4F0",
                corner_radius=15,
                width=130,
                font=("Helvetica", 14, "bold"),
                command=lambda d=day: self.load_sleep_records(selected_day=d)
            )
            btn.pack(side="left", padx=8)

        # --- Main card with dark background ---
        card = ctk.CTkFrame(self.content_frame, corner_radius=25, fg_color="#1B263B", border_width=2, border_color="#2D3748")
        card.pack(pady=20, padx=50, fill="both", expand=True)

        # Scrollable frame inside card
        scroll_frame = ctk.CTkScrollableFrame(card, fg_color="#1B263B", corner_radius=0)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            scroll_frame,
            text=f"Sleep Records - {self.patient.name} {self.patient.surname} ({selected_day})",
            font=("Helvetica", 26, "bold"),
            text_color="#63B3ED"
        )
        title.pack(pady=(0, 20))

        # Grid container for main data
        grid_frame = ctk.CTkFrame(scroll_frame, fg_color="#223354")
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Data widgets definitions
        widget_defs = [
            (0, 0, "Total Sleep", "total_sleep", "7h 30m"),
            (0, 1, "Time in Bed", "time_in_bed", "8h 15m"),
            (1, 0, "Sleep Efficiency", "efficiency", "91%"),
            (1, 1, "Avg HR During Sleep", "hr_during_sleep", "65 bpm"),
        ]

        for row, col, label, attr, default in widget_defs:
            widget = ctk.CTkFrame(grid_frame, corner_radius=20, fg_color="#2D3B57", width=250, height=130)
            widget.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

            container = ctk.CTkFrame(widget, fg_color="transparent")
            container.pack(fill="x", padx=20, pady=20)

            ctk.CTkLabel(container, text=label, font=("Helvetica", 20, "bold"), text_color="#63B3ED").pack(side="left", anchor="w")
            ctk.CTkLabel(container, text=record.get(attr, default), font=("Helvetica", 20, "bold"), text_color="#F0EDEE").pack(side="right", anchor="e")

        # Sleep Score (wide widget)
        widget_score = ctk.CTkFrame(grid_frame, corner_radius=20, fg_color="#2D3B57", height=130)
        widget_score.grid(row=2, column=0, columnspan=2, padx=12, pady=12, sticky="nsew")

        score_container = ctk.CTkFrame(widget_score, fg_color="transparent")
        score_container.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(score_container, text="Sleep Score", font=("Helvetica", 22, "bold"), text_color="#63B3ED").pack(side="left", anchor="w")

        score = record.get("Sleep_Score", 0)
        ctk.CTkLabel(score_container, text=str(score), font=("Helvetica", 22, "bold"), text_color="#F0EDEE").pack(side="right", anchor="e")

        progress_container = ctk.CTkFrame(widget_score, fg_color="transparent")
        progress_container.pack(fill="x", padx=20, pady=(10, 20))

        progress_bar = ctk.CTkProgressBar(progress_container, height=14, progress_color="#63B3ED")
        progress_bar.set(float(score) / 100)
        progress_bar.pack(fill="x")

        # Configure grid expansion for uniform resizing
        for i in range(2):
            grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            grid_frame.grid_rowconfigure(i, weight=1)

        # --- Sleep Features Section ---
        features_title = ctk.CTkLabel(
            scroll_frame,
            text="Sleep Features",
            font=("Helvetica", 22, "bold"),
            text_color="#63B3ED"
        )
        features_title.pack(pady=(30, 10), padx=20, anchor="w")

        features_frame = ctk.CTkFrame(scroll_frame, fg_color="#2D3B57", corner_radius=15)
        features_frame.pack(fill="x", padx=20, pady=(0, 30))

        features = [
            ("Total Sleep Amount", "total_sleep", "7h 30m"),
            ("Efficiency", "efficiency", "91%"),
            ("Latency", "latency", "15 min"),
            ("REM Phase", "rem_phase", "1h 20m"),
            ("Deep Sleep Phase", "deep_phase", "1h 45m"),
            ("Light Sleep Phase", "light_phase", "4h 25m"),
        ]

        for name, attr, default in features:
            row = ctk.CTkFrame(features_frame, fg_color="transparent")
            row.pack(fill="x", pady=5, padx=20)

            ctk.CTkLabel(row, text=name, font=("Helvetica", 18), anchor="w", width=260, text_color="#63B3ED").pack(side="left")
            ctk.CTkLabel(row, text=str(record.get(attr, default)), font=("Helvetica", 18, "bold"), anchor="e", text_color="#F0EDEE").pack(side="right")


        
    def load_questionnaires(self, selected_day=None):
        self.clear_content()

        # Example ISI data for multiple days
        isi_data = {
            "2024-05-15": {"total_score": 18, "severity": "Moderate", "responses": [
                ("Difficulty falling asleep", 3),
                ("Difficulty staying asleep", 2),
                ("Problem waking up early", 3),
                ("Sleep dissatisfaction", 4),
                ("Interference with daily functioning", 3),
                ("Noticeable by others", 2),
                ("Worry about current sleep", 1)
            ]},
            "2024-05-16": {"total_score": 20, "severity": "Severe", "responses": [
                ("Difficulty falling asleep", 4),
                ("Difficulty staying asleep", 3),
                ("Problem waking up early", 4),
                ("Sleep dissatisfaction", 4),
                ("Interference with daily functioning", 4),
                ("Noticeable by others", 3),
                ("Worry about current sleep", 2)
            ]},
            "2024-05-17": {"total_score": 15, "severity": "Moderate", "responses": [
                ("Difficulty falling asleep", 2),
                ("Difficulty staying asleep", 2),
                ("Problem waking up early", 3),
                ("Sleep dissatisfaction", 3),
                ("Interference with daily functioning", 2),
                ("Noticeable by others", 2),
                ("Worry about current sleep", 1)
            ]},
            "2024-05-18": {"total_score": 10, "severity": "Mild", "responses": [
                ("Difficulty falling asleep", 1),
                ("Difficulty staying asleep", 1),
                ("Problem waking up early", 1),
                ("Sleep dissatisfaction", 2),
                ("Interference with daily functioning", 1),
                ("Noticeable by others", 1),
                ("Worry about current sleep", 1)
            ]},
            "2024-05-19": {"total_score": 22, "severity": "Severe", "responses": [
                ("Difficulty falling asleep", 4),
                ("Difficulty staying asleep", 4),
                ("Problem waking up early", 4),
                ("Sleep dissatisfaction", 4),
                ("Interference with daily functioning", 4),
                ("Noticeable by others", 3),
                ("Worry about current sleep", 3)
            ]}
        }

        days = list(isi_data.keys())
        if selected_day is None or selected_day not in isi_data:
            selected_day = days[0]
        record = isi_data[selected_day]

        # --- Top horizontal bar ---
        bar_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent", orientation="horizontal", height=60)
        bar_frame.pack(fill="x", padx=30, pady=(20, 10))

        for day in days:
            btn = ctk.CTkButton(
                bar_frame,
                text=day,
                fg_color="#5a86ff" if day == selected_day else "#2D3748",
                text_color="white",
                hover_color="#7CC4F0",
                corner_radius=15,
                width=130,
                command=lambda d=day: self.load_questionnaires(selected_day=d)  # Dynamic reload with selected day
            )
            btn.pack(side="left", padx=8)

        # --- Main card ---
        card = ctk.CTkFrame(self.content_frame, corner_radius=20, fg_color="#1B263B")
        card.pack(pady=20, padx=50, fill="both", expand=True)

        ctk.CTkLabel(
            card,
            text=f"ISI Questionnaire - {selected_day}",
            font=("Helvetica", 26, "bold"),
            text_color="#63B3ED"
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            card,
            text=f"Total Score: {record['total_score']} ({record['severity']})",
            font=("Helvetica", 20, "bold"),
            text_color="#F0EDEE"
        ).pack(pady=(0, 20))

        # --- Scrollable questionnaire ---
        scroll_frame = ctk.CTkScrollableFrame(card, fg_color="transparent", corner_radius=15, width=800, height=400)
        scroll_frame.pack(pady=10, padx=40, fill="both", expand=True)

        likert_labels = ["0 - None", "1 - Mild", "2 - Moderate", "3 - Severe", "4 - Very Severe"]

        for q_text, selected_score in record["responses"]:
            q_widget = ctk.CTkFrame(scroll_frame, fg_color="#0D1B2A", corner_radius=15, border_width=2, border_color="#2D3748")
            q_widget.pack(pady=15, padx=20, ipadx=10, ipady=10)

            # Centered question
            ctk.CTkLabel(
                q_widget,
                text=q_text,
                font=("Helvetica", 16, "bold"),
                text_color="#CBD5E0",
                wraplength=700,
                justify="center"
            ).pack(pady=(15, 10))

            # Centered Likert scale
            likert_frame = ctk.CTkFrame(q_widget, fg_color="transparent")
            likert_frame.pack(pady=10)

            for i, label in enumerate(likert_labels):
                color = "#63B3ED" if i == selected_score else "#2D3748"
                text_color = "white" if i == selected_score else "#CBD5E0"
                ctk.CTkLabel(
                    likert_frame,
                    text=label,
                    font=("Helvetica", 14),
                    fg_color=color,
                    text_color=text_color,
                    corner_radius=10,
                    width=120,
                    height=40
                ).pack(side="left", padx=6)

    def load_questionnaires_for_day(self, selected_day):
        # For now, just reload with selected day (simulate)
        self.load_questionnaires()
