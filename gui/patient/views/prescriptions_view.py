from .base_view import BaseView
import customtkinter as ctk

class PrescriptionsView(BaseView):
    def show(self):
        self.app.clear_content()

        title = ctk.CTkLabel(self.app.content_frame, text="My Prescriptions", font=("Arial", 24, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=20)

        # Category buttons
        btn_style = {"width": 140, "height": 60, "corner_radius": 20, "font": ("Helvetica", 15, "bold")}
        ctk.CTkButton(
            self.app.content_frame, text="Drugs", command=self.show_drugs, **btn_style
        ).grid(row=1, column=0, padx=40, pady=10)
        ctk.CTkButton(
            self.app.content_frame, text="Sleep Habits", command=self.show_sleep_habits, **btn_style
        ).grid(row=1, column=1, padx=40, pady=10)
        ctk.CTkButton(
            self.app.content_frame, text="Examinations", command=self.show_examinations, **btn_style
        ).grid(row=1, column=2, padx=40, pady=10)

    def show_drugs(self):
        self.app.clear_content()
        title = ctk.CTkLabel(self.app.content_frame, text="Prescribed Drugs", font=("Arial", 20, "bold"))
        title.pack(pady=(20, 10))

        drugs = [
            {"name": "Melatonin", "dosage": "3 mg", "instructions": "Take 1 tablet before bedtime"},
            {"name": "Zolpidem", "dosage": "5 mg", "instructions": "Take 1 tablet 30 minutes before sleep"},
            {"name": "Valerian Root", "dosage": "500 mg", "instructions": "Take 1 capsule in the evening"},
        ]

        for drug in drugs:
            frame = ctk.CTkFrame(self.app.content_frame)
            frame.pack(padx=20, pady=10, fill="x")
            name_label = ctk.CTkLabel(frame, text=f"{drug['name']} - {drug['dosage']}", font=("Arial", 14, "bold"))
            name_label.pack(anchor="w", padx=10, pady=5)
            instr_label = ctk.CTkLabel(frame, text=drug["instructions"], font=("Arial", 12))
            instr_label.pack(anchor="w", padx=10, pady=(0, 5))

    def show_sleep_habits(self):
        self.app.clear_content()
        title = ctk.CTkLabel(self.app.content_frame, text="Recommended Sleep Habits", font=("Arial", 20, "bold"))
        title.pack(pady=(20, 10))

        habits = [
            "Maintain a consistent sleep schedule.",
            "Avoid caffeine and heavy meals before bedtime.",
            "Create a restful sleeping environment.",
            "Limit screen time before sleep.",
        ]

        for habit in habits:
            habit_label = ctk.CTkLabel(self.app.content_frame, text=f"• {habit}", font=("Arial", 12))
            habit_label.pack(anchor="w", padx=20, pady=5)

    def show_examinations(self):
        self.app.clear_content()
        title = ctk.CTkLabel(self.app.content_frame, text="Scheduled Examinations", font=("Arial", 20, "bold"))
        title.pack(pady=(20, 10))

        exams = [
            {"name": "Polysomnography", "date": "2025-06-10", "location": "Sleep Center A"},
            {"name": "Home Sleep Test", "date": "2025-06-15", "location": "At Home"},
        ]

        for exam in exams:
            frame = ctk.CTkFrame(self.app.content_frame)
            frame.pack(padx=20, pady=10, fill="x")
            name_label = ctk.CTkLabel(frame, text=exam["name"], font=("Arial", 14, "bold"))
            name_label.pack(anchor="w", padx=10, pady=5)
            details_label = ctk.CTkLabel(frame, text=f"Date: {exam['date']} | Location: {exam['location']}", font=("Arial", 12))
            details_label.pack(anchor="w", padx=10, pady=(0, 5))