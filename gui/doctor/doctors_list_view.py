import customtkinter as ctk
from services.doctor_services import get_all_doctors

class DoctorsListView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#121927")  # Match patient app background

        ctk.CTkLabel(
            self,
            text="All Doctors",
            font=("Helvetica", 28, "bold"),
            text_color="#63B3ED"
        ).pack(pady=(30, 10))

        doctors = get_all_doctors()
        if not doctors:
            ctk.CTkLabel(self, text="No doctors found.", font=("Helvetica", 18), text_color="#F0EDEE").pack(pady=40)
            return

        # Scrollable area for cards
        scroll = ctk.CTkScrollableFrame(self, fg_color="#121927")
        scroll.pack(fill="both", expand=True, padx=40, pady=20)

        for doc in doctors:
            card = ctk.CTkFrame(scroll, corner_radius=25, fg_color="#1B263B")
            card.pack(pady=24, padx=40, fill="x", expand=True)

            # Title
            ctk.CTkLabel(
                card,
                text=f"👤 Dr. {doc.get('name', '')} {doc.get('surname', '')}",
                font=("Helvetica", 22, "bold"),
                text_color="#63B3ED"
            ).pack(pady=(18, 6), anchor="w", padx=30)

            # Info block with grid for labels and button
            info_frame = ctk.CTkFrame(card, fg_color="#0D1B2A", corner_radius=20)
            info_frame.pack(pady=10, padx=30, fill="x")

            label_style = {
                "font": ("Helvetica", 16),
                "text_color": "#F0EDEE"
            }

            # Place labels in column 0
            ctk.CTkLabel(info_frame, text=f"🩺 Specialty: {doc.get('specialty', '')}", **label_style).grid(row=0, column=0, sticky="w", padx=20, pady=(14, 6))
            ctk.CTkLabel(info_frame, text=f"📧 Email: {doc.get('email', '')}", **label_style).grid(row=1, column=0, sticky="w", padx=20, pady=(6, 14))

            # Contact Button in column 1, vertically centered
            contact_btn = ctk.CTkButton(
                info_frame,
                text="Contact",
                fg_color="#63B3ED",
                hover_color="#7A8FF7",
                text_color="#121927",
                font=("Helvetica", 15, "bold"),
                width=110,
                command=lambda: None  # No action for now
            )
            contact_btn.grid(row=0, column=1, rowspan=2, padx=(20, 24), pady=10, sticky="e")

            # Make column 0 expand to push the button to the right
            info_frame.grid_columnconfigure(0, weight=1)