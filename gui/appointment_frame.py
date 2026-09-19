"""Appointment management tab inside the GUI."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

from models.appointment import Appointment
from exceptions.custom_exceptions import (
    DuplicateIDError,
    RecordNotFoundError,
    SchedulingConflictError,
)

if TYPE_CHECKING:
    from services.hospital import Hospital


class AppointmentFrame:
    """Tab for scheduling and cancelling appointments."""

    def __init__(self, parent: ttk.Notebook, hospital: "Hospital") -> None:
        self.hospital = hospital
        self.frame = ttk.Frame(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        left = ttk.LabelFrame(self.frame, text="Appointment Details", padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        labels = [
            "Appointment ID:",
            "Patient ID:",
            "Doctor ID:",
            "Date (YYYY-MM-DD):",
            "Time (HH:MM):",
            "Reason:",
        ]
        keys = ["id", "patient", "doctor", "date", "time", "reason"]

        self.entries: dict[str, ttk.Entry] = {}
        for i, (lbl, key) in enumerate(zip(labels, keys)):
            ttk.Label(left, text=lbl).grid(row=i, column=0, sticky=tk.W, pady=2)
            e = ttk.Entry(left, width=25)
            e.grid(row=i, column=1, pady=2, padx=5)
            self.entries[key] = e

        bf = ttk.Frame(left)
        bf.grid(row=len(labels), column=0, columnspan=2, pady=10)
        ttk.Button(bf, text="Schedule", command=self._schedule, width=10).pack(
            side=tk.LEFT, padx=3
        )
        ttk.Button(bf, text="Cancel", command=self._cancel, width=10).pack(
            side=tk.LEFT, padx=3
        )

        ttk.Button(left, text="Refresh", command=self._refresh).grid(
            row=len(labels) + 1, column=0, columnspan=2, pady=5
        )

        right = ttk.LabelFrame(self.frame, text="Appointments", padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = ("ID", "Patient", "Doctor", "Date", "Time", "Status")
        self.tree = ttk.Treeview(right, columns=cols, show="headings", height=22)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100, minwidth=60)

        sb = ttk.Scrollbar(right, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self._refresh()

    def _schedule(self) -> None:
        try:
            aid = self.entries["id"].get().strip()
            pid = self.entries["patient"].get().strip()
            did = self.entries["doctor"].get().strip()
            date = self.entries["date"].get().strip()
            time = self.entries["time"].get().strip()
            reason = self.entries["reason"].get().strip()

            if not all([aid, pid, did, date, time]):
                raise ValueError("Please fill in ID, Patient ID, Doctor ID, Date, and Time.")

            patient = self.hospital.get_patient(pid)
            doctor = self.hospital.get_doctor(did)

            appt = Appointment(aid, patient, doctor, date, time, reason)
            self.hospital.schedule_appointment(appt)
            self._clear()
            self._refresh()
            messagebox.showinfo("Success", "Appointment scheduled!")
        except (RecordNotFoundError, DuplicateIDError, SchedulingConflictError) as e:
            messagebox.showerror(type(e).__name__, str(e))
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _cancel(self) -> None:
        try:
            aid = self.entries["id"].get().strip()
            if not aid:
                return
            if messagebox.askyesno("Confirm", f"Cancel appointment '{aid}'?"):
                self.hospital.cancel_appointment(aid)
                self._refresh()
                messagebox.showinfo("Success", "Appointment cancelled!")
        except RecordNotFoundError as e:
            messagebox.showerror("Not Found", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _refresh(self) -> None:
        try:
            self.tree.delete(*self.tree.get_children())
            for a in self.hospital.get_all_appointments():
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        a.id,
                        a.patient.name,
                        a.doctor.name,
                        a.date,
                        a.time,
                        a.status,
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_select(self, _event) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0], "values")
        self.entries["id"].delete(0, tk.END)
        self.entries["id"].insert(0, v[0])
        for k in ["patient", "doctor", "reason"]:
            self.entries[k].delete(0, tk.END)
        self.entries["date"].delete(0, tk.END)
        self.entries["date"].insert(0, v[3])
        self.entries["time"].delete(0, tk.END)
        self.entries["time"].insert(0, v[4])

    def _clear(self) -> None:
        for e in self.entries.values():
            e.delete(0, tk.END)