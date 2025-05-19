import customtkinter as ctk

class BaseView:
    def __init__(self, app):
        self.app = app  # Reference to PatientApp

    def show(self):
        """Override in subclasses to render the view."""
        raise NotImplementedError