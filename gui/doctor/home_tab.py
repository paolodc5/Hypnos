import customtkinter as ctk
from models.doctor import Doctor
from PIL import Image, ImageTk
import os


class HomeTab(ctk.CTkFrame):
    def __init__(self, master, doctor: Doctor):
        super().__init__(master)
        self.configure(fg_color="#0f172a")  # dark navy

        # Load and place logo
        logo_path = os.path.join(os.path.dirname(__file__), "..", "images", "logo_hypnos.png")
        logo_img = ctk.CTkImage(light_image=Image.open(logo_path), size=(180, 180))
        ctk.CTkLabel(self, image=logo_img, text="").pack(pady=(36, 10))

        # Welcome message
        ctk.CTkLabel(
            self,
            text=f"Welcome back, Dr. {doctor.surname}",
            font=("Arial", 28, "bold"),
            text_color="#f1f5f9"
        ).pack(pady=(0, 6))

        # Subtitle
        ctk.CTkLabel(
            self,
            text="Ready to help your patients sleep better?",
            font=("Arial", 16, "italic"),
            text_color="#94a3b8"
        ).pack(pady=(0, 30))

        # Divider
        ctk.CTkFrame(self, height=2, fg_color="#1e293b").pack(fill="x", padx=80, pady=(0, 24))

        # Info cards container
        cards = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=16)
        cards.pack(pady=10, padx=40, fill="x")
        cards.grid_rowconfigure(0, weight=1)
        cards.grid_columnconfigure((0,1,2), weight=1)

        card_font = ("Arial", 16, "bold")
        card_color = "#e2e8f0"

        ctk.CTkLabel(cards, text="👥 Patients", font=card_font, text_color=card_color).grid(row=0, column=0, padx=20, pady=24)
        ctk.CTkLabel(cards, text="📅 Appointments", font=card_font, text_color=card_color).grid(row=0, column=1, padx=20, pady=24)
        ctk.CTkLabel(cards, text="💤 Sleep Records", font=card_font, text_color=card_color).grid(row=0, column=2, padx=20, pady=24)

        # Motivational quote
        ctk.CTkLabel(
            self,
            text="“The best bridge between despair and hope is a good night’s sleep.”",
            font=("Arial", 13, "italic"),
            text_color="#cbd5e1"
        ).pack(pady=(40, 0))
