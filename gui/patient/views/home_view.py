from .base_view import BaseView
import customtkinter as ctk
from PIL import Image
import os

class HomeView(BaseView):
    def show(self):
        self.app.clear_content()

        # Create a card frame
        card = ctk.CTkFrame(self.app.content_frame, corner_radius=30, fg_color="#1B263B", border_width=0)
        card.pack(pady=40, padx=80, fill="both", expand=True)

        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), "../../images/Hypnos.png")
        logo_image = ctk.CTkImage(Image.open(logo_path), size=(120, 120))
        ctk.CTkLabel(card, image=logo_image, text="", bg_color="transparent").pack(pady=(20, 10))

        # Welcome
        ctk.CTkLabel(card, text=f"🌙 Hello {self.app.patient.name} {self.app.patient.surname}",
                     font=("Helvetica", 30, "bold"), text_color="#F0EDEE").pack(pady=(0, 10))
        ctk.CTkLabel(card, text="Track, understand, and improve your sleep habits.",
                     font=("Helvetica", 16), text_color="#CBD5E0").pack(pady=(0, 30))

        # Quick Actions
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(pady=10)
        button_style = {
            "width": 180, "height": 55, "corner_radius": 25, "font": ("Helvetica", 15, "bold")
        }
        ctk.CTkButton(actions_frame, text="📊 Sleep Records", command=self.app.show_sleep_records, fg_color="#63B3ED", hover_color="#7CC4F0", **button_style).pack(side="left", padx=12)
        ctk.CTkButton(actions_frame, text="💊 Prescriptions", command=self.app.show_prescriptions, fg_color="#9F7AEA", hover_color="#B084F7", **button_style).pack(side="left", padx=12)
        ctk.CTkButton(actions_frame, text="👩‍⚕️ My Doctor", command=self.app.show_doctor_profile, fg_color="#FFB347", hover_color="#FFC980", **button_style).pack(side="left", padx=12)

        # Divider and tip
        ctk.CTkFrame(card, height=1, fg_color="#2D3748").pack(fill="x", padx=60, pady=40)
        tip_frame = ctk.CTkFrame(card, fg_color="#0D1B2A", corner_radius=20)
        tip_frame.pack(pady=10, padx=50, fill="x")
        ctk.CTkLabel(tip_frame, text="💡 Tip:\nConsistent sleep and wake times support your circadian rhythm.\nLet’s build that routine.",
                     font=("Helvetica", 16, "italic"), text_color="#63B3ED", justify="center").pack(pady=20, padx=20)