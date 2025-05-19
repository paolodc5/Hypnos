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
        ctk.CTkLabel(info_frame, text=f"👤 Name: {p.name} {p.surname}", **label_style).pack(pady=10, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"🎂 Birthdate: {p.birth_date}", **label_style).pack(pady=10, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"📧 Email: {p.email}", **label_style).pack(pady=10, anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text=f"📞 Phone: {p.phone_number}", **label_style).pack(pady=10, anchor="w", padx=20)

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