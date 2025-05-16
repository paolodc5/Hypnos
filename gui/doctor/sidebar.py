import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, command_callback):
        super().__init__(master)
        self.master = master
        self.command_callback = command_callback

        label = ctk.CTkLabel(self, text="E-Health System", font=("Arial", 16, "bold"), text_color="white", width=200, height=30, anchor="center")
        label.place(x=0, y=30)

        home_button = ctk.CTkButton(self, text="Home", command=lambda: self.command_callback("home"), width=160, fg_color="#3366cc", hover_color="#66d9cc")
        home_button.place(x=20, y=80)

        patient_button = ctk.CTkButton(self, text="Patients", command=lambda: self.command_callback("patients"), width=160, fg_color="#3366cc", hover_color="#66d9cc")
        patient_button.place(x=20, y=130)
