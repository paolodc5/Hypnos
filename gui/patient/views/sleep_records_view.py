from .base_view import BaseView
import customtkinter as ctk

class SleepRecordsView(BaseView):
    def show(self, selected_day=None):
        self.app.clear_content()

        # Example sleep records (replace with your real data source)
        sleep_records = {
            "2024-05-15": {
                "total_sleep": "7h 30m",
                "time_in_bed": "8h 15m",
                "efficiency": "91%",
                "hr_during_sleep": "65 bpm",
                "Sleep_Score": 82,
                "latency": "15 min",
                "rem_phase": "1h 20m",
                "deep_phase": "1h 45m",
                "light_phase": "4h 25m",
            },
            "2024-05-16": {
                "total_sleep": "6h 50m",
                "time_in_bed": "7h 40m",
                "efficiency": "89%",
                "hr_during_sleep": "67 bpm",
                "Sleep_Score": 75,
                "latency": "18 min",
                "rem_phase": "1h 10m",
                "deep_phase": "1h 30m",
                "light_phase": "4h 10m",
            }
        }

        days = list(sleep_records.keys())
        if not days:
            ctk.CTkLabel(self.app.content_frame, text="No sleep records available.", font=("Helvetica", 18), text_color="red").pack(pady=40)
            return

        if selected_day is None or selected_day not in days:
            selected_day = days[0]
        record = sleep_records[selected_day]

        # --- Top bar with day buttons ---
        bar_frame = ctk.CTkFrame(self.app.content_frame, fg_color="transparent")
        bar_frame.pack(fill="x", padx=30, pady=(20, 15))

        for day in days:
            btn = ctk.CTkButton(
                bar_frame,
                text=day,
                fg_color="#5a86ff" if day == selected_day else "#2D3748",
                text_color="white",
                hover_color="#7CC4F0",
                corner_radius=15,
                width=130,
                font=("Helvetica", 14, "bold"),
                command=lambda d=day: self.show(selected_day=d)
            )
            btn.pack(side="left", padx=8)

        # --- Main card with dark background ---
        card = ctk.CTkFrame(self.app.content_frame, corner_radius=25, fg_color="#1B263B", border_width=2, border_color="#2D3748")
        card.pack(pady=20, padx=50, fill="both", expand=True)

        # Scrollable frame inside card
        scroll_frame = ctk.CTkScrollableFrame(card, fg_color="#1B263B", corner_radius=0)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            scroll_frame,
            text=f"Sleep Records - {self.app.patient.name} {self.app.patient.surname} ({selected_day})",
            font=("Helvetica", 26, "bold"),
            text_color="#63B3ED"
        )
        title.pack(pady=(0, 20))

        # Grid container for main data
        grid_frame = ctk.CTkFrame(scroll_frame, fg_color="#223354")
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Data widgets definitions
        widget_defs = [
            (0, 0, "Total Sleep", "total_sleep", "7h 30m"),
            (0, 1, "Time in Bed", "time_in_bed", "8h 15m"),
            (1, 0, "Sleep Efficiency", "efficiency", "91%"),
            (1, 1, "Avg HR During Sleep", "hr_during_sleep", "65 bpm"),
        ]

        for row, col, label, attr, default in widget_defs:
            widget = ctk.CTkFrame(grid_frame, corner_radius=20, fg_color="#2D3B57", width=250, height=130)
            widget.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

            container = ctk.CTkFrame(widget, fg_color="transparent")
            container.pack(fill="x", padx=20, pady=20)

            ctk.CTkLabel(container, text=label, font=("Helvetica", 20, "bold"), text_color="#63B3ED").pack(side="left", anchor="w")
            ctk.CTkLabel(container, text=record.get(attr, default), font=("Helvetica", 20, "bold"), text_color="#F0EDEE").pack(side="right", anchor="e")

        # Sleep Score (wide widget)
        widget_score = ctk.CTkFrame(grid_frame, corner_radius=20, fg_color="#2D3B57", height=130)
        widget_score.grid(row=2, column=0, columnspan=2, padx=12, pady=12, sticky="nsew")

        score_container = ctk.CTkFrame(widget_score, fg_color="transparent")
        score_container.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(score_container, text="Sleep Score", font=("Helvetica", 22, "bold"), text_color="#63B3ED").pack(side="left", anchor="w")

        score = record.get("Sleep_Score", 0)
        ctk.CTkLabel(score_container, text=str(score), font=("Helvetica", 22, "bold"), text_color="#F0EDEE").pack(side="right", anchor="e")

        progress_container = ctk.CTkFrame(widget_score, fg_color="transparent")
        progress_container.pack(fill="x", padx=20, pady=(10, 20))

        progress_bar = ctk.CTkProgressBar(progress_container, height=14, progress_color="#63B3ED")
        progress_bar.set(float(score) / 100)
        progress_bar.pack(fill="x")

        # Configure grid expansion for uniform resizing
        for i in range(2):
            grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            grid_frame.grid_rowconfigure(i, weight=1)

        # --- Sleep Features Section ---
        features_title = ctk.CTkLabel(
            scroll_frame,
            text="Sleep Features",
            font=("Helvetica", 22, "bold"),
            text_color="#63B3ED"
        )
        features_title.pack(pady=(30, 10), padx=20, anchor="w")

        features_frame = ctk.CTkFrame(scroll_frame, fg_color="#2D3B57", corner_radius=15)
        features_frame.pack(fill="x", padx=20, pady=(0, 30))

        features = [
            ("Total Sleep Amount", "total_sleep", "7h 30m"),
            ("Efficiency", "efficiency", "91%"),
            ("Latency", "latency", "15 min"),
            ("REM Phase", "rem_phase", "1h 20m"),
            ("Deep Sleep Phase", "deep_phase", "1h 45m"),
            ("Light Sleep Phase", "light_phase", "4h 25m"),
        ]

        for name, attr, default in features:
            row = ctk.CTkFrame(features_frame, fg_color="transparent")
            row.pack(fill="x", pady=5, padx=20)

            ctk.CTkLabel(row, text=name, font=("Helvetica", 18), anchor="w", width=260, text_color="#63B3ED").pack(side="left")
            ctk.CTkLabel(row, text=str(record.get(attr, default)), font=("Helvetica", 18, "bold"), anchor="e", text_color="#F0EDEE").pack(side="right")

