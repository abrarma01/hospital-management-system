"""Doctor management tab inside the GUI."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

from models.doctor import Doctor
from exceptions.custom_exceptions import DuplicateIDError, RecordNotFoundError

if TYPE_CHECKING:
    from services.hospital import Hospital


class DoctorFrame:
    """Tab for managing doctors."""

    def __init__(self, parent: ttk.Notebook, hospital: "Hospital") -> None:
        self.hospital = hospital
        self.frame = ttk.Frame(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        left = ttk.LabelFrame(self.frame, text="Doctor Details", padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        labels = [
            "Doctor ID:",
            "Name:",
            "Age:",
            "Phone:",
            "Gender:",
            "Specialty:",
            "Salary:",
        ]
        keys = ["id", "name", "age", "phone", "gender", "specialty", "salary"]

        self.entries: dict[str, ttk.Entry] = {}
        for i, (lbl, key) in enumerate(zip(labels, keys)):
            ttk.Label(left, text=lbl).grid(row=i, column=0, sticky=tk.W, pady=2)
            e = ttk.Entry(left, width=25)
            e.grid(row=i, column=1, pady=2, padx=5)
            self.entries[key] = e

        bf = ttk.Frame(left)
        bf.grid(row=len(labels), column=0, columnspan=2, pady=10)
        ttk.Button(bf, text="Add", command=self._add, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(bf, text="Update", command=self._update, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(bf, text="Remove", command=self._remove, width=8).pack(side=tk.LEFT, padx=2)

        sf = ttk.Frame(left)
        sf.grid(row=len(labels) + 1, column=0, columnspan=2, pady=5)
        ttk.Label(sf, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        ttk.Entry(sf, textvariable=self.search_var, width=16).pack(side=tk.LEFT, padx=4)
        ttk.Button(sf, text="Go", command=self._search, width=4).pack(side=tk.LEFT)
        ttk.Button(sf, text="Show All", command=self._refresh, width=8).pack(side=tk.LEFT, padx=3)

        right = ttk.LabelFrame(self.frame, text="Doctor List", padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = ("ID", "Name", "Age", "Specialty", "Salary")
        self.tree = ttk.Treeview(right, columns=cols, show="headings", height=22)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100, minwidth=70)

        sb = ttk.Scrollbar(right, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self._refresh()

    def _add(self) -> None:
        try:
            did = self.entries["id"].get().strip()
            if not self.hospital.validate_id(did):
                raise ValueError("Doctor ID must be a positive number.")
            d = Doctor(
                doctor_id=did,
                name=self.entries["name"].get().strip(),
                age=int(self.entries["age"].get().strip()),
                phone=self.entries["phone"].get().strip(),
                gender=self.entries["gender"].get().strip(),
                specialty=self.entries["specialty"].get().strip(),
                salary=float(self.entries["salary"].get().strip()),
            )
            self.hospital.add_doctor(d)
            self._clear()
            self._refresh()
            messagebox.showinfo("Success", f"Dr. {d.name} added!")
        except DuplicateIDError as e:
            messagebox.showerror("Duplicate ID", str(e))
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update(self) -> None:
        try:
            did = self.entries["id"].get().strip()
            self.hospital.update_doctor(
                doctor_id=did,
                name=self.entries["name"].get().strip() or None,
                age=(
                    int(self.entries["age"].get().strip())
                    if self.entries["age"].get().strip()
                    else None
                ),
                phone=self.entries["phone"].get().strip() or None,
                specialty=self.entries["specialty"].get().strip() or None,
                salary=(
                    float(self.entries["salary"].get().strip())
                    if self.entries["salary"].get().strip()
                    else None
                ),
            )
            self._refresh()
            messagebox.showinfo("Success", "Doctor updated!")
        except RecordNotFoundError as e:
            messagebox.showerror("Not Found", str(e))
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _remove(self) -> None:
        try:
            did = self.entries["id"].get().strip()
            if not did:
                return
            if messagebox.askyesno("Confirm", f"Remove doctor '{did}'?"):
                self.hospital.remove_doctor(did)
                self._clear()
                self._refresh()
                messagebox.showinfo("Success", "Doctor removed!")
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
            self._populate(self.hospital.search_doctors(kw))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _refresh(self) -> None:
        try:
            self._populate(self.hospital.get_all_doctors())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _populate(self, doctors: list) -> None:
        self.tree.delete(*self.tree.get_children())
        for d in doctors:
            self.tree.insert(
                "", tk.END, values=(d.id, d.name, d.age, d.specialty, f"${d.salary:,.2f}")
            )

    def _on_select(self, _event) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0], "values")
        mapping = ["id", "name", "age", "specialty", "salary"]
        for key, val in zip(mapping, v):
            self.entries[key].delete(0, tk.END)
            clean = val.replace("$", "").replace(",", "") if key == "salary" else val
            self.entries[key].insert(0, clean)
        # Phone & gender not in tree — leave them
        self.entries["phone"].delete(0, tk.END)
        self.entries["gender"].delete(0, tk.END)

    def _clear(self) -> None:
        for e in self.entries.values():
            e.delete(0, tk.END)