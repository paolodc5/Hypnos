import customtkinter as ctk
from gui.doctor.scrollable_list_frame import ScrollableListFrame
from gui.doctor.add_prescription_dialog import AddPrescriptionDialog
from gui.doctor.add_note_dialog import AddNoteDialog
from gui.doctor.section_config import get_section_config

class AdministrationFrame(ctk.CTkFrame):
    def __init__(self, master, patient=None):
        super().__init__(master)
        self.patient = patient
        self.selected_item = None
        self.configure(fg_color="#eaf0fb", corner_radius=12)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=2)  # 2/3 for scrollable
        self.grid_columnconfigure(1, weight=1)  # 1/3 for actions

        self.seg_button = ctk.CTkSegmentedButton(
            self, 
            values=["Sleep", "Notes", "Prescriptions"],
            command=self.show_section,
            font=("Arial", 14, "bold"),
            fg_color="#e2e8f0",
            selected_color="#2563eb",
            selected_hover_color="#3b82f6",
            unselected_color="#cbd5e1",
            unselected_hover_color="#e2e8f0",
            text_color="#1e293b",
            height=30,
            width=500,
            corner_radius=12
        )
        self.seg_button.grid(row=0, column=0, columnspan=2, pady=(18, 10), padx=0, sticky="n")

        # Left: Scrollable list (2/3)
        self.content_frame = ctk.CTkFrame(self, fg_color="#f8fafc", corner_radius=10)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)

        # Right: Actions (1/3)
        self.action_frame = ctk.CTkFrame(self, fg_color="#e0e7ef", corner_radius=10)
        self.action_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.action_frame.grid_rowconfigure((0,1,2,3), weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)

        self.current_section = None
        self.show_section("Sleep")  # Default

    def set_patient(self, patient):
        self.patient = patient
        self.show_section(self.current_section or "Sleep")

    def show_section(self, section):
        self.current_section = section
        self.selected_item = None  # Reset selection
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        for widget in self.action_frame.winfo_children():
            widget.destroy()

        if not self.patient:
            ctk.CTkLabel(self.content_frame, text="No patient selected", font=("Arial", 14, "italic"), text_color="gray").pack(pady=30)
            return

        config = get_section_config(self.patient)
        section_conf = config.get(section)
        if not section_conf:
            ctk.CTkLabel(self.content_frame, text="Invalid section", font=("Arial", 14, "italic"), text_color="gray").pack(pady=30)
            return

        section_conf["loader"]()
        items = section_conf["items"]()

        def on_select(item):
            self.selected_item = item
            self.update_action_buttons(section)

        ScrollableListFrame(
            self.content_frame,
            items,
            fields_formatter=section_conf["fields_formatter"],
            detail_formatter=section_conf["detail_formatter"],
            column_titles=section_conf["column_titles"],
            select_callback=on_select
        ).pack(fill="both", expand=True, padx=10, pady=10)

        self.update_action_buttons(section)

    def update_action_buttons(self, section):
        for widget in self.action_frame.winfo_children():
            widget.destroy()

        button_config = {
            "font": ("Arial", 14, "bold"),
            "height": 42,
            "corner_radius": 8,
            "width": 180
        }

        if section == "Notes":
            # Add Note (Primary)
            ctk.CTkButton(
                self.action_frame,
                text="📝 Add Note",
                fg_color="#3b82f6",
                hover_color="#2563eb",
                command=self.open_add_note_dialog,
                **button_config
            ).grid(row=0, column=0, padx=20, pady=(10, 6), sticky="ew")

            # Edit Note (Neutral Gray)
            ctk.CTkButton(
                self.action_frame,
                text="✏️ Edit Note",
                fg_color="#64748b",
                hover_color="#475569",
                state="normal" if self.selected_item else "disabled",
                command=self.open_edit_note_dialog,
                **button_config
            ).grid(row=1, column=0, padx=20, pady=6, sticky="ew")

            # Delete Note (Soft Red)
            ctk.CTkButton(
                self.action_frame,
                text="🗑️ Delete Note",
                fg_color="#ef4444",
                hover_color="#dc2626",
                state="normal" if self.selected_item else "disabled",
                command=self.delete_note,
                **button_config
            ).grid(row=2, column=0, padx=20, pady=(6, 10), sticky="ew")

        elif section == "Prescriptions":
            ctk.CTkButton(
                self.action_frame,
                text="💊 Add Prescription",
                fg_color="#3b82f6",
                hover_color="#2563eb",
                command=self.open_add_prescription_dialog,
                **button_config
            ).grid(row=0, column=0, padx=20, pady=(10, 6), sticky="ew")

            ctk.CTkButton(
                self.action_frame,
                text="✏️ Edit Prescription",
                fg_color="#64748b",
                hover_color="#475569",
                state="normal" if self.selected_item else "disabled",
                command=self.open_edit_prescription_dialog,
                **button_config
            ).grid(row=1, column=0, padx=20, pady=6, sticky="ew")

            ctk.CTkButton(
                self.action_frame,
                text="🗑️ Delete Prescription",
                fg_color="#ef4444",
                hover_color="#dc2626",
                state="normal" if self.selected_item else "disabled",
                command=self.delete_prescription,
                **button_config
            ).grid(row=2, column=0, padx=20, pady=(6, 10), sticky="ew")

    def open_add_note_dialog(self):
        dialog = AddNoteDialog(self, self.patient)
        self.wait_window(dialog)
        self.show_section("Notes")  # Refresh after adding

    def open_edit_note_dialog(self):
        if not self.selected_item:
            return
        from gui.doctor.edit_note_dialog import EditNoteDialog
        dialog = EditNoteDialog(self, self.patient, self.selected_item)
        self.wait_window(dialog)
        self.show_section("Notes")

    def delete_note(self):
        if not self.selected_item:
            return
        from services.doctor_services import delete_note
        import tkinter.messagebox as mb
        if mb.askyesno("Confirm Delete", "Are you sure you want to delete this note?"):
            delete_note(self.selected_item.note_id)
            self.show_section("Notes")

    def open_add_prescription_dialog(self):
        dialog = AddPrescriptionDialog(self, self.patient)
        self.wait_window(dialog)
        self.show_section("Prescriptions")  # Refresh after adding

    def open_edit_prescription_dialog(self):
        if not self.selected_item:
            return
        from gui.doctor.edit_prescription_dialog import EditPrescriptionDialog
        dialog = EditPrescriptionDialog(self, self.patient, self.selected_item)
        self.wait_window(dialog)
        self.show_section("Prescriptions")

    def delete_prescription(self):
        if not self.selected_item:
            return
        from services.doctor_services import delete_prescription
        import tkinter.messagebox as mb
        if mb.askyesno("Confirm Delete", "Are you sure you want to delete this prescription?"):
            delete_prescription(self.selected_item.prescription_id)
            self.show_section("Prescriptions")




