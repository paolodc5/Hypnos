import customtkinter as ctk
from PIL import Image, ImageTk
import os


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, command_callback):
        super().__init__(master, fg_color="#223366", corner_radius=0)
        self.master = master
        self.command_callback = command_callback

        # Logo image (replace with your own .png)
        logo_path = os.path.join(os.path.dirname(__file__), "../images/logo_hypnos.png")
        logo_img = ctk.CTkImage(light_image=Image.open(logo_path), size=(80, 80))
        logo_label = ctk.CTkLabel(self, image=logo_img, text="")
        logo_label.grid(row=0, column=0, padx=20, pady=(24, 8))

        # App name
        # ctk.CTkLabel(self, text="Hypnos", font=("Arial", 22, "bold"), text_color="#f8fafc").grid(row=1, column=0, padx=20, pady=(0, 18))

        # Navigation buttons
        self.home_button = ctk.CTkButton(self, text="Home", command=lambda: self.command_callback("home"),
                                         fg_color="#3366cc", hover_color="#204080", font=("Arial", 14, "bold"), width=160)
        self.home_button.grid(row=2, column=0, padx=20, pady=8)
        self.patient_button = ctk.CTkButton(self, text="Patients", command=lambda: self.command_callback("patients"),
                                            fg_color="#3366cc", hover_color="#204080", font=("Arial", 14, "bold"), width=160)
        self.patient_button.grid(row=3, column=0, padx=20, pady=8)

        # Spacer
        self.grid_rowconfigure(4, weight=1)

        # Appearance mode
        ctk.CTkLabel(self, text="Appearance Mode:", font=("Arial", 12), text_color="#f8fafc").grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                            command=self.change_appearance_mode,
                                                            fg_color="#3366cc", button_color="#204080", width=140)
        self.appearance_mode_optionemenu.set("System")
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(4, 10), sticky="w")

        # UI Scaling
        ctk.CTkLabel(self, text="UI Scaling:", font=("Arial", 12), text_color="#f8fafc").grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        self.scaling_optionemenu = ctk.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"],
                                                     command=self.change_scaling, fg_color="#3366cc", button_color="#204080", width=140)
        self.scaling_optionemenu.set("100%")
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(4, 20), sticky="w")

        self.grid_columnconfigure(0, weight=1)

    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)

    def change_scaling(self, scaling):
        scaling_float = int(scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(scaling_float)
