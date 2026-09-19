"""Statistics / info tab inside the GUI."""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.hospital import Hospital


class StatsFrame:
    """Tab that shows hospital statistics and lists OOP concepts used."""

    def __init__(self, parent: ttk.Notebook, hospital: "Hospital") -> None:
        self.hospital = hospital
        self.frame = ttk.Frame(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.frame, padding=15)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            container, text="Hospital Statistics", font=("Arial", 16, "bold")
        ).pack(pady=(0, 15))

        # --- Stats ---
        sf = ttk.LabelFrame(container, text="Summary", padding=12)
        sf.pack(fill=tk.X, padx=15, pady=5)

        items = [
            ("hospital_name", "Hospital Name:"),
            ("total_patients", "Total Patients:"),
            ("total_doctors", "Total Doctors:"),
            ("total_employees", "Total Employees:"),
            ("total_appointments", "Total Appointments:"),
            ("active_appointments", "Active Appointments:"),
            ("cancelled_appointments", "Cancelled Appointments:"),
        ]

        self.labels: dict[str, ttk.Label] = {}
        for i, (key, text) in enumerate(items):
            ttk.Label(sf, text=text, font=("Arial", 11)).grid(
                row=i, column=0, sticky=tk.W, pady=2, padx=(0, 20)
            )
            lbl = ttk.Label(sf, text="—", font=("Arial", 11, "bold"))
            lbl.grid(row=i, column=1, sticky=tk.W, pady=2)
            self.labels[key] = lbl

        ttk.Button(container, text="Refresh Statistics", command=self._refresh).pack(
            pady=12
        )

        # --- OOP concepts list ---
        oop = ttk.LabelFrame(container, text="OOP Concepts Implemented", padding=12)
        oop.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        concepts = [
            "Classes & Objects — Person, Patient, Doctor, Employee, Appointment, MedicalRecord, Hospital",
            "Constructors — __init__ in every class",
            "Inheritance — Patient, Doctor, Employee extend Person (ABC)",
            "Encapsulation — private __attributes with @property getters/setters",
            "Abstraction — Person is an Abstract Base Class (abc module)",
            "Polymorphism — display_information() and show_details() overridden per subclass",
            "Composition — Hospital contains Patients/Doctors/Appointments; Patient owns MedicalRecords",
            "Aggregation — Appointment references Doctor & Patient (they exist independently)",
            "Class Variables — total_patients, total_doctors, total_employees, total_persons",
            "Class Methods — @classmethod: from_dict(), get_total_*(), reset_total()",
            "Static Methods — @staticmethod: validate_id(), format_currency()",
            "Magic Methods — __str__, __repr__, __len__",
            "Exception Handling — try/except throughout the application",
            "Custom Exceptions — DuplicateIDError, InvalidIDError, SchedulingConflictError, RecordNotFoundError",
            "File Handling — JSON save/load with auto-load on start and auto-save on exit",
            "Packages & Modules — multi-file project structure with __init__.py",
            "Type Hints — used in all major classes and methods",
            "Documentation — docstrings on every class and important method",
        ]

        for c in concepts:
            ttk.Label(oop, text=f"  \u2022 {c}", wraplength=750, font=("Arial", 9)).pack(
                anchor=tk.W, pady=1
            )

        self._refresh()

    def _refresh(self) -> None:
        try:
            stats = self.hospital.get_statistics()
            for key, lbl in self.labels.items():
                lbl.config(text=str(stats.get(key, "—")))
        except Exception:
            pass