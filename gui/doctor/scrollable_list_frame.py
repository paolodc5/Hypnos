import customtkinter as ctk
from gui.doctor.clickable_row_frame import ClickableRowFrame

class ScrollableListFrame(ctk.CTkFrame):
    def __init__(self, master, items, fields_formatter, detail_formatter, column_titles, select_callback=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.items = items
        self.fields_formatter = fields_formatter
        self.detail_formatter = detail_formatter
        self.column_titles = column_titles
        self.select_callback = select_callback
        self.selected_row = None
        self.selected_index = None
        self.row_widgets = []

        self.canvas = ctk.CTkCanvas(
            self, 
            borderwidth=0, 
            highlightthickness=0, 
            bg="#f8fafc"
        )        
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.inner_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10)

        self.populate()

    def populate(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        # Header row
        for col, title in enumerate(self.column_titles):
            header = ctk.CTkLabel(
                self.inner_frame,
                text=title,
                font=("Arial", 13, "bold"),
                anchor="w",
                text_color="#1d4ed8",
                fg_color="transparent"
            )
            header.grid(row=0, column=col, sticky="ew", padx=(24 if col == 0 else 12, 2), pady=(0, 2))
            self.inner_frame.grid_columnconfigure(col, weight=1)
        # Data rows
        self.row_widgets.clear()
        for i, item in enumerate(self.items):
            fields = self.fields_formatter(item)
            detail = self.detail_formatter(item)
            row_labels = []
            for col, (label, value, unit) in enumerate(fields):
                value_label = ctk.CTkLabel(
                    self.inner_frame,
                    text=f"{value} {unit}".strip(),
                    font=("Arial", 13),
                    text_color="#1e293b",
                    anchor="w"
                )
                value_label.grid(row=i+1, column=col, sticky="ew", padx=(24 if col == 0 else 12, 2), pady=8)
                value_label.bind("<Button-1>", lambda e, idx=i: self.select_row(idx))
                row_labels.append(value_label)
                self.inner_frame.grid_columnconfigure(col, weight=1)
            self.row_widgets.append(row_labels)

    def select_row(self, idx):
        # Remove highlight from previous
        if self.selected_index is not None:
            for widget in self.row_widgets[self.selected_index]:
                widget.configure(fg_color="transparent")
        # Highlight new
        for widget in self.row_widgets[idx]:
            widget.configure(fg_color="#bae6fd")
        self.selected_index = idx
        self.selected_row = self.items[idx]
        if self.select_callback:
            self.select_callback(self.selected_row)

    def show_detail_dialog(self, item, details):
        from gui.doctor.detail_dialog import DetailDialog
        # Determine type and date for title
        if hasattr(item, "precr_date"):
            title = f"Prescription {item.precr_date}"
        elif hasattr(item, "date") and hasattr(item, "note_id"):
            title = f"Note {item.date}"
        elif hasattr(item, "date"):
            title = f"Sleep Record {item.date}"
        else:
            title = "Details"
        DetailDialog(self, title, details)