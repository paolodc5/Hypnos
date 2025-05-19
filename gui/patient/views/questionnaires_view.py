from .base_view import BaseView
import customtkinter as ctk

class QuestionnairesView(BaseView):
    def show(self, selected_day=None):
        self.app.clear_content()

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
        bar_frame = ctk.CTkScrollableFrame(self.app.content_frame, fg_color="transparent", orientation="horizontal", height=60)
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
                command=lambda d=day: self.show(selected_day=d)  # Dynamic reload with selected day
            )
            btn.pack(side="left", padx=8)

        # --- Main card ---
        card = ctk.CTkFrame(self.app.content_frame, corner_radius=20, fg_color="#1B263B")
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
        self.app.load_questionnaires()