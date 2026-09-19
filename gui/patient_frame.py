"""Patient management tab inside the GUI."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

from models.patient import Patient
from exceptions.custom_exceptions import DuplicateIDError, RecordNotFoundError

if TYPE_CHECKING:
    from services.hospital import Hospital


class PatientFrame:
    """Tab for adding, updating, removing, and searching patients."""

    def __init__(self, parent: ttk.Notebook, hospital: "Hospital") -> None:
        self.hospital = hospital
        self.frame = ttk.Frame(parent)
        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self) -> None:
        # --- Left: form ---
        left = ttk.LabelFrame(self.frame, text="Patient Details", padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        labels = [
            "Patient ID:",
            "Name:",
            "Age:",
            "Phone:",
            "Gender:",
            "Blood Type:",
        ]
        keys = ["id", "name", "age", "phone", "gender", "blood"]

        self.entries: dict[str, ttk.Entry] = {}
        for i, (lbl, key) in enumerate(zip(labels, keys)):
            ttk.Label(left, text=lbl).grid(row=i, column=0, sticky=tk.W, pady=2)
            e = ttk.Entry(left, width=25)
            e.grid(row=i, column=1, pady=2, padx=5)
            self.entries[key] = e

        # Buttons
        bf = ttk.Frame(left)
        bf.grid(row=len(labels), column=0, columnspan=2, pady=10)
        ttk.Button(bf, text="Add", command=self._add, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(bf, text="Update", command=self._update, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(bf, text="Remove", command=self._remove, width=8).pack(side=tk.LEFT, padx=2)

        # Search row
        sf = ttk.Frame(left)
        sf.grid(row=len(labels) + 1, column=0, columnspan=2, pady=5)
        ttk.Label(sf, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        ttk.Entry(sf, textvariable=self.search_var, width=16).pack(side=tk.LEFT, padx=4)
        ttk.Button(sf, text="Go", command=self._search, width=4).pack(side=tk.LEFT)
        ttk.Button(sf, text="Show All", command=self._refresh, width=8).pack(side=tk.LEFT, padx=3)

        # --- Right: treeview ---
        right = ttk.LabelFrame(self.frame, text="Patient List", padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = ("ID", "Name", "Age", "Phone", "Gender", "Blood")
        self.tree = ttk.Treeview(right, columns=cols, show="headings", height=22)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=85, minwidth=60)

        sb = ttk.Scrollbar(right, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self._refresh()

    # -------------------------------------------------------------- Actions
    def _add(self) -> None:
        try:
            pid = self.entries["id"].get().strip()
            if not self.hospital.validate_id(pid):
                raise ValueError("Patient ID must be a positive number.")
            p = Patient(
                patient_id=pid,
                name=self.entries["name"].get().strip(),
                age=int(self.entries["age"].get().strip()),
                phone=self.entries["phone"].get().strip(),
                gender=self.entries["gender"].get().strip(),
                blood_type=self.entries["blood"].get().strip() or "Unknown",
            )
            self.hospital.add_patient(p)
            self._clear()
            self._refresh()
            messagebox.showinfo("Success", f"Patient '{p.name}' added!")
        except DuplicateIDError as e:
            messagebox.showerror("Duplicate ID", str(e))
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update(self) -> None:
        try:
            pid = self.entries["id"].get().strip()
            self.hospital.update_patient(
                patient_id=pid,
                name=self.entries["name"].get().strip() or None,
                age=(
                    int(self.entries["age"].get().strip())
                    if self.entries["age"].get().strip()
                    else None
                ),
                phone=self.entries["phone"].get().strip() or None,
                gender=self.entries["gender"].get().strip() or None,
                blood_type=self.entries["blood"].get().strip() or None,
            )
            self._refresh()
            messagebox.showinfo("Success", "Patient updated!")
        except RecordNotFoundError as e:
            messagebox.showerror("Not Found", str(e))
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _remove(self) -> None:
        try:
            pid = self.entries["id"].get().strip()
            if not pid:
                return
            if messagebox.askyesno("Confirm", f"Remove patient '{pid}'?"):
                self.hospital.remove_patient(pid)
                self._clear()
                self._refresh()
                messagebox.showinfo("Success", "Patient removed!")
        except RecordNotFoundError as e:
            messagebox.showerror("Not Found", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _search(self) -> None:
        kw = self.search_var.get().strip()
        if not kw:
            self._refresh()
            return
        try:
            self._populate(self.hospital.search_patients(kw))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _refresh(self) -> None:
        try:
            self._populate(self.hospital.get_all_patients())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _populate(self, patients: list) -> None:
        self.tree.delete(*self.tree.get_children())
        for p in patients:
            self.tree.insert(
                "", tk.END, values=(p.id, p.name, p.age, p.phone, p.gender, p.blood_type)
            )

    def _on_select(self, _event) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0], "values")
        for key, val in zip(["id", "name", "age", "phone", "gender", "blood"], v):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, val)

    def _clear(self) -> None:
        for e in self.entries.values():
            e.delete(0, tk.END)