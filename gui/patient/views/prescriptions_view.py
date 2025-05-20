from .base_view import BaseView
import customtkinter as ctk
from services.patient_services import get_prescriptions

class PrescriptionsView(BaseView):
    def show(self):
        self.app.clear_content()

        # Use a scrollable frame for the whole content
        scrollable = ctk.CTkScrollableFrame(self.app.content_frame, corner_radius=25, fg_color="#1B263B")
        scrollable.pack(pady=40, padx=60, fill="both", expand=True)

        title = ctk.CTkLabel(
            scrollable,
            text="My Prescriptions",
            font=("Helvetica", 28, "bold"),
            text_color="#63B3ED"
        )
        title.pack(pady=(30, 10))

        prescriptions = get_prescriptions(self.app.patient.patient_id)

        # --- Drugs Category ---
        drugs_frame = ctk.CTkFrame(scrollable, fg_color="#0D1B2A", corner_radius=18)
        drugs_frame.pack(pady=18, padx=40, fill="x")
        ctk.CTkLabel(drugs_frame, text="💊 Drugs", font=("Helvetica", 20, "bold"), text_color="#63B3ED").pack(anchor="w", padx=20, pady=(10, 5))
        drugs = [p for p in prescriptions if p.treatm_type.lower() == "drug"]
        if not drugs:
            ctk.CTkLabel(drugs_frame, text="No drugs prescribed.", font=("Helvetica", 14), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=10)
        else:
            for drug in drugs:
                ctk.CTkLabel(drugs_frame, text=f"• {drug.content} (Date: {drug.precr_date})", font=("Helvetica", 15), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=4)

        # --- Remedies Category ---
        remedies_frame = ctk.CTkFrame(scrollable, fg_color="#0D1B2A", corner_radius=18)
        remedies_frame.pack(pady=18, padx=40, fill="x")
        ctk.CTkLabel(remedies_frame, text="🛌 Remedies", font=("Helvetica", 20, "bold"), text_color="#63B3ED").pack(anchor="w", padx=20, pady=(10, 5))
        remedies = [p for p in prescriptions if p.treatm_type.lower() == "remedies"]
        if not remedies:
            ctk.CTkLabel(remedies_frame, text="No remedies prescribed.", font=("Helvetica", 14), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=10)
        else:
            for remedy in remedies:
                ctk.CTkLabel(remedies_frame, text=f"• {remedy.content} (Date: {remedy.precr_date})", font=("Helvetica", 15), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=4)

        # --- Examinations Category ---
        exams_frame = ctk.CTkFrame(scrollable, fg_color="#0D1B2A", corner_radius=18)
        exams_frame.pack(pady=18, padx=40, fill="x")
        ctk.CTkLabel(exams_frame, text="📝 Examinations", font=("Helvetica", 20, "bold"), text_color="#63B3ED").pack(anchor="w", padx=20, pady=(10, 5))
        exams = [p for p in prescriptions if p.treatm_type.lower() == "visits"]
        if not exams:
            ctk.CTkLabel(exams_frame, text="No examinations prescribed.", font=("Helvetica", 14), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=10)
        else:
            for exam in exams:
                ctk.CTkLabel(exams_frame, text=f"• {exam.content} (Date: {exam.precr_date})", font=("Helvetica", 15), text_color="#F0EDEE").pack(anchor="w", padx=30, pady=4)