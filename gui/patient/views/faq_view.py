from .base_view import BaseView
import customtkinter as ctk

class FAQView(BaseView):
    def show(self):
        self.app.clear_content()

        title = ctk.CTkLabel(
            self.app.content_frame,
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
                self.app.content_frame,
                text=f"Q: {faq['question']}",
                font=("Helvetica", 16, "bold"),
                text_color="#F0EDEE",
                anchor="w",
                justify="left"
            )
            q_label.pack(fill="x", padx=40, pady=(15, 0))

            a_label = ctk.CTkLabel(
                self.app.content_frame,
                text=f"A: {faq['answer']}",
                font=("Helvetica", 15),
                text_color="#CBD5E0",
                anchor="w",
                justify="left",
                wraplength=800
            )
            a_label.pack(fill="x", padx=60, pady=(0, 10))