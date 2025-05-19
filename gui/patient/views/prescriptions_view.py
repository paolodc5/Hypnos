from .base_view import BaseView
import customtkinter as ctk
from services.patient_services import get_prescriptions

class PrescriptionsView(BaseView):
    def show(self):
        self.app.clear_content()

        # Main card/frame for the whole view
        card = ctk.CTkFrame(self.app.content_frame, corner_radius=25, fg_color="#1B263B")
        card.pack(pady=40, padx=60, fill="both", expand=True)

        title = ctk.CTkLabel(
            card,
            text="My Prescriptions",
            font=("Helvetica", 28, "bold"),
            text_color="#63B3ED"
        )
        title.pack(pady=(30, 10))

        # Fetch all prescriptions once
        prescriptions = get_prescriptions(self.app.patient.patient_id)

        # --- Drugs Category ---
        drugs_frame = ctk.CTkFrame(card, fg_color="#0D1B2A", corner_radius=18)
        drugs_frame.pack(pady=18, padx=40, fill="x")
        ctk.CTkLabel(drugs_frame, text="💊 Drugs", font=("Helvetica", 20, "bold"), text_color="#63B3ED").pack(anchor="w", padx=20, pady=(10, 5))
        drugs = [p for p in prescriptions if p.treatm_type.lower() == "drug"]
        if not drugs:
            ctk.CTkLabel(drugs_frame, text="No drugs prescribed.", font=("Helvetica", 14), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=10)
        else:
            for drug in drugs:
                ctk.CTkLabel(drugs_frame, text=f"• {drug.content} (Date: {drug.prescr_date})", font=("Helvetica", 15), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=4)

        # --- Sleep Habits Category ---
        habits_frame = ctk.CTkFrame(card, fg_color="#0D1B2A", corner_radius=18)
        habits_frame.pack(pady=18, padx=40, fill="x")
        ctk.CTkLabel(habits_frame, text="🛌 Sleep Habits", font=("Helvetica", 20, "bold"), text_color="#63B3ED").pack(anchor="w", padx=20, pady=(10, 5))
        habits = [p for p in prescriptions if p.treatm_type.lower() == "sleep habit"]
        if not habits:
            ctk.CTkLabel(habits_frame, text="No sleep habits prescribed.", font=("Helvetica", 14), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=10)
        else:
            for habit in habits:
                ctk.CTkLabel(habits_frame, text=f"• {habit.content} (Date: {habit.prescr_date})", font=("Helvetica", 15), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=4)

        # --- Examinations Category ---
        exams_frame = ctk.CTkFrame(card, fg_color="#0D1B2A", corner_radius=18)
        exams_frame.pack(pady=18, padx=40, fill="x")
        ctk.CTkLabel(exams_frame, text="📝 Examinations", font=("Helvetica", 20, "bold"), text_color="#63B3ED").pack(anchor="w", padx=20, pady=(10, 5))
        exams = [p for p in prescriptions if p.treatm_type.lower() == "examination"]
        if not exams:
            ctk.CTkLabel(exams_frame, text="No examinations prescribed.", font=("Helvetica", 14), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=10)
        else:
            for exam in exams:
                ctk.CTkLabel(exams_frame, text=f"• {exam.content} (Date: {exam.prescr_date})", font=("Helvetica", 15), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=4)