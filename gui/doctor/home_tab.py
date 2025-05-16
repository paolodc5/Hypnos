import customtkinter as ctk
from models.doctor import Doctor

class HomeTab(ctk.CTkFrame):
    def __init__(self, master, doctor: Doctor):
        super().__init__(master)
        ctk.CTkLabel(self, text=f"Welcome back, Dr. {doctor.surname}", font=("Arial", 18), text_color="#204080").pack(pady=200)
