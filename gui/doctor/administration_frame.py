import customtkinter as ctk
from gui.doctor.scrollable_list_frame import ScrollableListFrame

class AdministrationFrame(ctk.CTkFrame):
    def __init__(self, master, patient=None):
        super().__init__(master)
        self.patient = patient
        self.configure(fg_color="#eaf0fb", corner_radius=12)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.seg_button = ctk.CTkSegmentedButton(
            self, 
            values=["Sleep", "Notes", "Prescriptions"],
            command=self.show_section,
            font=("Arial", 14, "bold"),
            fg_color="#e2e8f0",
            selected_color="#2563eb",
            selected_hover_color="#3b82f6",
            unselected_color="#cbd5e1",
            unselected_hover_color="#e2e8f0",
            text_color="#1e293b",
            height=48,
            width=500,
            corner_radius=12
        )
        self.seg_button.grid(row=0, column=0, pady=(18, 10), padx=0, sticky="n")

        self.content_frame = ctk.CTkFrame(self, fg_color="#f8fafc", corner_radius=10)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.current_section = None
        self.show_section("Sleep")  # Default

    def set_patient(self, patient):
        self.patient = patient
        self.show_section(self.current_section or "Sleep")

    def show_section(self, section):
        self.current_section = section
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.patient:
            ctk.CTkLabel(self.content_frame, text="No patient selected", font=("Arial", 14, "italic"), text_color="gray").pack(pady=30)
            return

        config = {
            "Sleep": {
                "loader": self.patient.load_sleep_records,
                "items": lambda: sorted(self.patient.sleep_records, key=lambda r: r.date, reverse=True),
                "title": "🛌 Sleep Records",
                "fields_formatter": lambda r: [
                    ("Date", r.date, ""),
                    ("HR", r.hr, "bpm"),
                    ("SpO₂", r.spo2, "%"),
                    ("MovIdx", r.movement_idx, ""),
                    ("Cycles", r.sleep_cycles, ""),
                ],
                "column_titles": ["Date", "HR", "SpO₂", "MovIdx", "Cycles"],
                "detail_formatter": lambda r: (
                    f"Date: {r.date}\n"
                    f"Device ID: {r.device_id}\n"
                    f"HR: {r.hr} bpm\n"
                    f"SpO₂: {r.spo2} %\n"
                    f"Movement Index: {r.movement_idx}\n"
                    f"Cycles: {r.sleep_cycles}\n"
                    f"Patient ID: {r.patient_id}"
                )
            },
            "Notes": {
                "loader": self.patient.load_notes,
                "items": lambda: sorted(self.patient.notes, key=lambda n: n.date, reverse=True),
                "title": "📝 Notes",
                "fields_formatter": lambda n: [
                    ("Date", n.date, ""),
                    ("Doctor", n.doctor_id, ""),
                    ("Preview", n.content[:40] + ("..." if len(n.content) > 40 else ""), ""),
                ],
                "column_titles": ["Date", "Doctor", "Preview"],
                "detail_formatter": lambda n: (
                    f"Date: {n.date}\n"
                    f"Doctor ID: {n.doctor_id}\n"
                    f"Patient ID: {n.patient_id}\n"
                    f"Note ID: {n.note_id}\n"
                    f"Content:\n{n.content}"
                )
            },
            "Prescriptions": {
                "loader": self.patient.load_prescriptions,
                "items": lambda: sorted(self.patient.prescriptions, key=lambda p: p.precr_date, reverse=True),
                "title": "💊 Prescriptions",
                "fields_formatter": lambda p: [
                    ("Date", p.precr_date, ""),
                    ("Type", p.treatm_type, ""),
                    ("Preview", p.content[:30] + ("..." if len(p.content) > 30 else ""), ""),
                ],
                "column_titles": ["Date", "Type", "Preview"],
                "detail_formatter": lambda p: (
                    f"Date: {p.precr_date}\n"
                    f"Type: {p.treatm_type}\n"
                    f"Doctor ID: {p.doctor_id}\n"
                    f"Patient ID: {p.patient_id}\n"
                    f"Prescription ID: {p.prescription_id}\n"
                    f"Content:\n{p.content}"
                )
            }
        }

        section_conf = config.get(section)
        if not section_conf:
            ctk.CTkLabel(self.content_frame, text="Invalid section", font=("Arial", 14, "italic"), text_color="gray").pack(pady=30)
            return

        section_conf["loader"]()
        items = section_conf["items"]()
        # ctk.CTkLabel(self.content_frame, text=section_conf["title"], font=("Arial", 16, "bold"), text_color="#204080").pack(pady=(10, 10))
        ScrollableListFrame(
            self.content_frame,
            items,
            fields_formatter=section_conf["fields_formatter"],
            detail_formatter=section_conf["detail_formatter"],
            column_titles=section_conf["column_titles"]
        ).pack(fill="both", expand=True, padx=10, pady=10)




