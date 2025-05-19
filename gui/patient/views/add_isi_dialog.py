import customtkinter as ctk
import datetime

ISI_QUESTIONS = [
    "Difficulty falling asleep",
    "Difficulty staying asleep",
    "Problem waking up early",
    "Sleep dissatisfaction",
    "Interference with daily functioning",
    "Noticeable by others",
    "Worry about current sleep"
]

SCALE_LABELS = ["0", "1", "2", "3", "4"]
SCALE_DESCRIPTIONS = {
    0: "None",
    4: "Very Severe"
}

class AddISIDialog(ctk.CTkToplevel):
    def __init__(self, master, patient, on_success=None):
        super().__init__(master)
        self.title("Add Today's ISI Report")
        self.geometry("600x600")
        self.patient = patient
        self.on_success = on_success
        self.answers = [ctk.IntVar(value=0) for _ in ISI_QUESTIONS]

        ctk.CTkLabel(self, text="ISI Questionnaire - Today", font=("Helvetica", 22, "bold")).pack(pady=20)

        # --- Scrollable frame for questions ---
        scroll_frame = ctk.CTkScrollableFrame(self, width=540, height=400)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        for idx, question in enumerate(ISI_QUESTIONS):
            q_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            q_frame.pack(pady=10, fill="x")
            ctk.CTkLabel(q_frame, text=question, font=("Helvetica", 16)).pack(anchor="w", pady=4)

            scale_row = ctk.CTkFrame(q_frame, fg_color="transparent")
            scale_row.pack(anchor="w", fill="x", padx=10)

            # Left description
            ctk.CTkLabel(scale_row, text=f"0 - {SCALE_DESCRIPTIONS[0]}", font=("Helvetica", 12)).pack(side="left", padx=(0, 8))

            # Radio buttons
            for val in range(5):
                ctk.CTkRadioButton(
                    scale_row,
                    text=str(val),
                    variable=self.answers[idx],
                    value=val
                ).pack(side="left", padx=4)

            # Right description
            ctk.CTkLabel(scale_row, text=f"4 - {SCALE_DESCRIPTIONS[4]}", font=("Helvetica", 12)).pack(side="left", padx=(8, 0))

        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 12, "bold"))
        self.error_label.pack(pady=(0, 0))

        ctk.CTkButton(self, text="Submit", fg_color="#3366cc", hover_color="#5588dd", command=self.submit).pack(pady=18)

    def submit(self):
        today = datetime.date.today().isoformat()
        from db.connection import get_connection

        # Check if today's questionnaire already exists
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM Questionnaires WHERE Date=? AND PatID=?",
            (today, self.patient.patient_id)
        )
        if cursor.fetchone():
            self.error_label.configure(text="Today's ISI questionnaire has already been submitted.")
            conn.close()
            return

        # Save questionnaire summary
        score = sum(var.get() for var in self.answers)
        cursor.execute(
            "INSERT INTO Questionnaires (Date, Score, PatID, DocID) VALUES (?, ?, ?, ?)",
            (today, score, self.patient.patient_id, self.patient.doctor_id)
        )
        # Save each answer
        for idx, var in enumerate(self.answers):
            cursor.execute(
                "INSERT INTO QuestionnaireAnswers (PatID, Date, Question, Answer) VALUES (?, ?, ?, ?)",
                (self.patient.patient_id, today, ISI_QUESTIONS[idx], str(var.get()))
            )
        conn.commit()
        conn.close()

        if self.on_success:
            self.on_success()
        self.destroy()