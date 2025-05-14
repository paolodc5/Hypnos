# gui/main.py
import customtkinter as ctk
from gui.login import LoginWindow

def start_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    start_gui()