from .base_view import BaseView
import customtkinter as ctk

class DoctorView(BaseView):
    def show(self):
        self.app.clear_content()  # <-- Use self.app.clear_content()

        doctor = self.app.patient.get_doctor()  # Make sure your Patient class has this method

        # --- Main card with dark background ---
        card = ctk.CTkFrame(self.app.content_frame, corner_radius=25, fg_color="#1B263B")
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