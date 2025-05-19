from .base_view import BaseView
import customtkinter as ctk
from PIL import Image
import os

class ProfileView(BaseView):
    def show(self):
        self.app.clear_content()

        # --- Main card with dark background ---
        card = ctk.CTkFrame(self.app.content_frame, corner_radius=25, fg_color="#1B263B")
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

        p = self.app.patient
        ctk.CTkLabel(info_frame, text=f"👤 Name: {p.name} {p.surname}", **label_style).pack(pady=5, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"🎂 Birthdate: {p.birth_date}", **label_style).pack(pady=5, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"🔢 Age: {p.age}", **label_style).pack(pady=5, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"⚧ Gender: {p.gender}", **label_style).pack(pady=5, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"🆔 Fiscal Code: {p.fiscal_code}", **label_style).pack(pady=5, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"📧 Email: {p.email}", **label_style).pack(pady=5, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"📞 Phone: {p.phone_number}", **label_style).pack(pady=5, anchor="w", padx=20)

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

    def show_update_form(self):
        from gui.patient.views.profile_update_dialog import ProfileUpdateDialog
        ProfileUpdateDialog(self.app, self.app.patient, on_success=self.show)

    def save_profile_changes(self):
        new_email = self.email_entry.get()
        new_phone = self.phone_entry.get()

        self.app.patient.email = new_email
        self.app.patient.phone_number = new_phone
        self.app.patient.save()  # This will update the DB

        # Optionally reload from DB
        self.app.patient.reload_from_db()

        # Reload the profile view
        self.show()