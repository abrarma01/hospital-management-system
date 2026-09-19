"""Medical records management tab inside the GUI."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

from models.medical_record import MedicalRecord
from exceptions.custom_exceptions import RecordNotFoundError

if TYPE_CHECKING:
    from services.hospital import Hospital


class RecordsFrame:
    """Tab for creating medical records and viewing patient history."""

    def __init__(self, parent: ttk.Notebook, hospital: "Hospital") -> None:
        self.hospital = hospital
        self.frame = ttk.Frame(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        top = ttk.LabelFrame(self.frame, text="Add / Update Medical Record", padding=10)
        top.pack(fill=tk.X, padx=5, pady=5)

        labels = [
            "Patient ID:",
            "Record ID:",
            "Diagnosis:",
            "Treatment:",
            "Date (YYYY-MM-DD):",
            "Notes:",
        ]
        keys = ["patient", "record", "diagnosis", "treatment", "date", "notes"]

        self.entries: dict[str, ttk.Entry] = {}
        for i, (lbl, key) in enumerate(zip(labels, keys)):
            ttk.Label(top, text=lbl).grid(row=i, column=0, sticky=tk.W, pady=2, padx=5)
            e = ttk.Entry(top, width=45)
            e.grid(row=i, column=1, pady=2, padx=5)
            self.entries[key] = e

        bf = ttk.Frame(top)
        bf.grid(row=len(labels), column=0, columnspan=2, pady=8)
        ttk.Button(bf, text="Create Record", command=self._create, width=15).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(bf, text="View History", command=self._view_history, width=15).pack(
            side=tk.LEFT, padx=5
        )

        bottom = ttk.LabelFrame(self.frame, text="Medical History", padding=10)
        bottom.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = ("Record ID", "Diagnosis", "Treatment", "Date", "Notes")
        self.tree = ttk.Treeview(bottom, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130, minwidth=80)

        sb = ttk.Scrollbar(bottom, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

    def _create(self) -> None:
        try:
            pid = self.entries["patient"].get().strip()
            rid = self.entries["record"].get().strip()
            diag = self.entries["diagnosis"].get().strip()
            treat = self.entries["treatment"].get().strip()
            date = self.entries["date"].get().strip()
            notes = self.entries["notes"].get().strip()

            if not all([pid, rid, diag, treat]):
                raise ValueError("Patient ID, Record ID, Diagnosis, and Treatment are required.")

            record = MedicalRecord(rid, diag, treat, date, notes)
            self.hospital.add_medical_record(pid, record)
            messagebox.showinfo("Success", "Medical record added!")
        except RecordNotFoundError as e:
            messagebox.showerror("Not Found", str(e))
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _view_history(self) -> None:
        try:
            pid = self.entries["patient"].get().strip()
            if not pid:
                raise ValueError("Please enter a Patient ID.")

            history = self.hospital.get_patient_medical_history(pid)
            self.tree.delete(*self.tree.get_children())

            if not history:
                messagebox.showinfo("Empty", "No medical records found for this patient.")
                return

            for r in history:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        r["record_id"],
                        r["diagnosis"],
                        r["treatment"],
                        r["date"],
                        r.get("notes", ""),
                    ),
                )
        except RecordNotFoundError as e:
            messagebox.showerror("Not Found", str(e))
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))