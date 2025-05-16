import customtkinter as ctk

class DetailDialog(ctk.CTkToplevel):
    def __init__(self, master, title, details):
        super().__init__(master)
        self.title(title)
        self.geometry("480x440")
        self.attributes("-topmost", True)
        self.configure(bg="#eaf0fb")
        self.resizable(False, False)
        # Fancy border frame
        border = ctk.CTkFrame(self, fg_color="#3366cc", corner_radius=16)
        border.pack(fill="both", expand=True, padx=16, pady=16)
        # Content frame
        content = ctk.CTkFrame(border, fg_color="#f8fafc", corner_radius=12)
        content.pack(fill="both", expand=True, padx=8, pady=8)
        ctk.CTkLabel(content, text=title, font=("Arial", 20, "bold"), text_color="#204080").pack(pady=(18, 10))
        textbox = ctk.CTkTextbox(content, width=420, height=280, font=("Arial", 14), wrap="word")
        textbox.pack(padx=12, pady=10, fill="both", expand=True)
        textbox.insert("1.0", details)
        textbox.configure(state="disabled")
        ctk.CTkButton(content, text="Close", font=("Arial", 13, "bold"), command=self.destroy, fg_color="#3366cc", hover_color="#204080").pack(pady=10)
        self.lift()
        self.focus_force()