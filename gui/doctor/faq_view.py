import customtkinter as ctk
from models.forum_question import ForumQuestion
import datetime
from tkinter import messagebox
from services import doctor_services

# This is a simple FAQ view for the Doctor's app.

class FAQView(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.configure(fg_color="#121927")
        self.text_input = None  # Will hold the textbox widget

        self._build_ui()

    def _build_ui(self):
        # Main container (like 'card' in CalendarView)
        card = ctk.CTkFrame(self, corner_radius=25, fg_color="#1B263B")
        card.pack(padx=30, pady=30, fill="both", expand=True)

        title = ctk.CTkLabel(
            card,
            text="Frequently Asked Questions",
            font=("Helvetica", 26, "bold"),
            text_color="#63B3ED"
        )
        title.pack(pady=(10, 20))

        # Your FAQ entries here (could be put in a scrollable frame if needed)
        faqs = [
            {"question": "How do I record my sleep?", "answer": "Go to the 'Sleep Records' section and follow the instructions."},
            {"question": "Can I update my profile information?", "answer": "Yes, click on 'My Profile' in the sidebar and then 'Update Info'."},
            {"question": "How do I contact my doctor?", "answer": "Visit the 'Doctor' section to see contact info."},
            {"question": "What if I forget my password?", "answer": "Use password recovery or contact support."},
            {"question": "Where can I find my prescriptions?", "answer": "Available in 'Prescriptions' section."}
        ]

        for faq in faqs:
            q_label = ctk.CTkLabel(card, text=f"Q: {faq['question']}", font=("Helvetica", 16, "bold"), text_color="#F0EDEE", anchor="w", justify="left")
            q_label.pack(fill="x", padx=20, pady=(5, 0))
            a_label = ctk.CTkLabel(card, text=f"A: {faq['answer']}", font=("Helvetica", 15), text_color="#CBD5E0", anchor="w", justify="left", wraplength=500)
            a_label.pack(fill="x", padx=40, pady=(0, 10))

        # Button frame for nicer layout
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(pady=10)

        ask_button = ctk.CTkButton(
            btn_frame,
            text="Ask Support",
            fg_color="#3366cc",
            hover_color="#5599ee",
            width=150,
            command=self.open_support_popup
        )
        ask_button.pack()

    def open_support_popup(self):
        popup = ctk.CTkToplevel(self.app)
        popup.title("Ask Support")
        popup.geometry("500x400")
        popup.configure(fg_color="#121927")
        popup.grab_set()  # modal window

        card = ctk.CTkFrame(popup, corner_radius=25, fg_color="#1B263B")
        card.pack(padx=20, pady=20, fill="both", expand=True)

        label = ctk.CTkLabel(card, text="Write your question or issue below:", font=("Helvetica", 16), text_color="#F0EDEE", anchor="w")
        label.pack(padx=20, pady=(10, 10), fill="x")

        self.text_input = ctk.CTkTextbox(card, width=440, height=150)
        self.text_input.pack(padx=20, pady=10, fill="x", expand=True)

        submit_btn = ctk.CTkButton(card, text="Submit", width=100, command=lambda: self.submit_support_question(popup))
        submit_btn.pack(pady=15)

    def submit_support_question(self, popup):
        content = self.text_input.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Warning", "Please enter a question before submitting.")
            return

        # Replace below with your actual user info and forum submission logic
        user_type = getattr(self.app, "current_user_type", "Patient")
        user_id = getattr(self.app, "current_user_id", 1)

        now = datetime.datetime.now()
        new_question = ForumQuestion(
            user_type=user_type,
            user_id=user_id,
            request_id=None,  # will be assigned by DB
            request=content,
            filling_date=now.date().isoformat(),
            filling_time=now.time().strftime("%H:%M:%S"),
            taken=False
        )

        # Assuming patient_services.add_forum_question exists and is imported properly
        from services import patient_services
        patient_services.add_forum_question(new_question)

        messagebox.showinfo("Submitted", "Your question has been submitted to support.")
        popup.destroy()
