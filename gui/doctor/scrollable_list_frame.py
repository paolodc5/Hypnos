import customtkinter as ctk
from gui.doctor.clickable_row_frame import ClickableRowFrame

class ScrollableListFrame(ctk.CTkFrame):
    def __init__(self, master, items, fields_formatter, detail_formatter, column_titles, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.items = items
        self.fields_formatter = fields_formatter
        self.detail_formatter = detail_formatter
        self.column_titles = column_titles

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
            header.grid(row=0, column=col, sticky="new", padx=(24 if col == 0 else 12, 2), pady=(0, 2))
            self.inner_frame.grid_columnconfigure(col, weight=1)
        # Data rows
        for i, item in enumerate(self.items):
            fields = self.fields_formatter(item)
            detail = self.detail_formatter(item)
            row = ClickableRowFrame(
                self.inner_frame,
                fields=fields,
                detail_callback=lambda d=detail, it=item: self.show_detail_dialog(it, d)
            )
            row.grid(row=i+1, column=0, columnspan=len(self.column_titles), sticky="ew", padx=10, pady=4)
            self.inner_frame.grid_rowconfigure(i+1, weight=0)

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