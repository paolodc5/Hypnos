from .base_view import BaseView
import customtkinter as ctk
from models.forum_question import ForumQuestion
import datetime
from tkinter import messagebox
from services import patient_services

# This is a simple FAQ view for the Patient's app.

class FAQView(BaseView):
    def show(self):
        self.app.clear_content()
        self.app.content_frame.configure(fg_color="#121927")


        card = ctk.CTkFrame(self.app.content_frame, corner_radius=25, fg_color="#1B263B")
        card.pack(padx=30, pady=30, fill="both", expand=True)

        title = ctk.CTkLabel(
            card,
            text="Frequently Asked Questions",
            font=("Helvetica", 26, "bold"),
            text_color="#63B3ED"
        )
        title.pack(pady=(30, 10))

        faqs = [
            {
                "question": "How do I record my sleep?",
                "answer": "Go to the 'Sleep Records' section and follow the instructions to add a new record."
            },
            {
                "question": "Can I update my profile information?",
                "answer": "Yes, click on 'My Profile' in the sidebar and then the 'Update Info' button."
            },
            {
                "question": "How do I contact my doctor?",
                "answer": "Visit the 'Doctor' section to see your doctor's contact information."
            },
            {
                "question": "What should I do if I forget my password?",
                "answer": "Use the password recovery option on the login page or contact support."
            },
            {
                "question": "Where can I find my prescriptions?",
                "answer": "All your prescriptions are available in the 'Prescriptions' section."
            }
        ]

        for faq in faqs:
            q_label = ctk.CTkLabel(
                card,
                text=f"Q: {faq['question']}",
                font=("Helvetica", 16, "bold"),
                text_color="#F0EDEE",
                anchor="w",
                justify="left"
            )
            q_label.pack(fill="x", padx=40, pady=(15, 0))

            a_label = ctk.CTkLabel(
                card,
                text=f"A: {faq['answer']}",
                font=("Helvetica", 15),
                text_color="#CBD5E0",
                anchor="w",
                justify="left",
                wraplength=800
            )
            a_label.pack(fill="x", padx=60, pady=(0, 10))

        # Button frame for nicer layout
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(pady=20)

        # Add the "Ask Support" button below FAQs
        ask_button = ctk.CTkButton(
            btn_frame,
            text="Ask Support",
            fg_color="#3366cc",
            hover_color="#5599ee",
            width=150,
            command=self.open_support_popup
        )
        ask_button.pack(pady=30)

    def open_support_popup(self):
        popup = ctk.CTkToplevel(self.app)
        popup.title("Ask Support")
        popup.geometry("500x300")
        popup.grab_set()  # Make modal

        label = ctk.CTkLabel(popup, text="Write your question or issue below:", font=("Helvetica", 16))
        label.pack(pady=(20, 10), padx=20, anchor="w")

        self.text_input = ctk.CTkTextbox(popup, width=460, height=150)
        self.text_input.pack(padx=20, pady=10)

        submit_btn = ctk.CTkButton(popup, text="Submit", width=100, command=lambda: self.submit_support_question(popup))
        submit_btn.pack(pady=15)
    
    def submit_support_question(self, popup):
        content = self.text_input.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Warning", "Please enter a question before submitting.")
            return

        # Here you connect to your forum submission method:
        # For example:
        # user_type = self.app.current_user_type  # "Patient" or "Doctor" (you decide how to get this)
        # user_id = self.app.current_user_id
        # You would create a ForumQuestion instance and submit it to your DB

        # Example user info placeholders, replace with actual logged user info
        user_type = getattr(self.app, "current_user_type", "Patient")
        user_id = getattr(self.app, "current_user_id", 1)

        now = datetime.datetime.now()
        new_question = ForumQuestion(
            user_type=user_type,
            user_id=user_id,
            request_id=None,  # will be assigned by DB
            request=content,
            filling_date=now.date().isoformat(), # convert to string like '2024-05-16'
            filling_time=now.time().strftime("%H:%M:%S"),  # convert to string like '10:00:00'
            taken=False
        )

        # Assuming you have an add_forum_question function in your forum services
        patient_services.add_forum_question(new_question)

        messagebox.showinfo("Submitted", "Your question has been submitted to support.")
        popup.destroy()


    