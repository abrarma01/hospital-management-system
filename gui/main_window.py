"""Main application window — creates the root Tk window and all tab frames."""

import tkinter as tk
from tkinter import ttk, messagebox
from services.hospital import Hospital
from .patient_frame import PatientFrame
from .doctor_frame import DoctorFrame
from .appointment_frame import AppointmentFrame
from .records_frame import RecordsFrame
from .stats_frame import StatsFrame


class MainWindow:
    """Top-level GUI window for the Hospital Management System."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("🏥 Hospital Management System")
        self.root.geometry("950x620")
        self.root.minsize(850, 520)

        # Hospital instance (composition)
        self.hospital = Hospital()
        self.hospital.load_all_data()

        # Notebook (tabs)
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=[12, 4])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create each tab frame
        self.patient_frame = PatientFrame(self.notebook, self.hospital)
        self.doctor_frame = DoctorFrame(self.notebook, self.hospital)
        self.appointment_frame = AppointmentFrame(self.notebook, self.hospital)
        self.records_frame = RecordsFrame(self.notebook, self.hospital)
        self.stats_frame = StatsFrame(self.notebook, self.hospital)

        self.notebook.add(self.patient_frame.frame, text="  Patients  ")
        self.notebook.add(self.doctor_frame.frame, text="  Doctors  ")
        self.notebook.add(self.appointment_frame.frame, text="  Appointments  ")
        self.notebook.add(self.records_frame.frame, text="  Records  ")
        self.notebook.add(self.stats_frame.frame, text="  Statistics  ")

        # Save on close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self) -> None:
        """Save data before destroying the window."""
        try:
            self.hospital.save_all_data()
            messagebox.showinfo("Saved", "All data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save data:\n{e}")
        finally:
            self.root.destroy()

    def run(self) -> None:
        """Start the main loop."""
        self.root.mainloop()