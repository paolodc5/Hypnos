import customtkinter as ctk

class ScrollableListFrame(ctk.CTkFrame):
    def __init__(self, master, items, item_formatter=str, **kwargs):
        super().__init__(master, **kwargs)
        self.items = items
        self.item_formatter = item_formatter

        self.canvas = ctk.CTkCanvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.inner_frame = ctk.CTkFrame(self)

        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.populate()

    def populate(self):
        # Clear previous widgets
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        # Add new widgets
        for i, item in enumerate(self.items):
            text = self.item_formatter(item)
            ctk.CTkLabel(self.inner_frame, text=text, anchor="w", justify="left").pack(fill="x", padx=10, pady=2)