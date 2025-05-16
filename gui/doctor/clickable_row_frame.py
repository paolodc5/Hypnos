# gui/doctor/clickable_row_frame.py
import customtkinter as ctk

class ClickableRowFrame(ctk.CTkFrame):
    def __init__(self, master, fields, detail_callback, **kwargs):
        super().__init__(master, corner_radius=12, fg_color="#f1f5f9", **kwargs)

        self.configure(height=50)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", lambda e: detail_callback())

        self.default_color = "#f1f5f9"
        self.hover_color = "#e0e7ff"

        self.grid_columnconfigure(tuple(range(len(fields))), weight=1)

        for col, (label, value, unit) in enumerate(fields):
            value_label = ctk.CTkLabel(
                self, 
                text=f"{value} {unit}".strip(), 
                font=("Arial", 13),
                text_color="#1e293b",
                anchor="w"
            )
            value_label.grid(row=0, column=col, sticky="w", padx=(24 if col == 0 else 12, 6), pady=10)
            value_label.bind("<Button-1>", lambda e: detail_callback())

    def on_hover(self, event=None):
        self.configure(fg_color=self.hover_color)

    def on_leave(self, event=None):
        self.configure(fg_color=self.default_color)
