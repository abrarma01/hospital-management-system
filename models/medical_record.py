"""MedicalRecord class — owned by a Patient (composition)."""

from datetime import datetime
from typing import Dict, Any


class MedicalRecord:
    """A single medical record entry attached to a patient."""

    def __init__(
        self,
        record_id: str,
        diagnosis: str,
        treatment: str,
        date: str = "",
        notes: str = "",
    ) -> None:
        self.__id = record_id
        self.__diagnosis = diagnosis
        self.__treatment = treatment
        self.__date = date if date else datetime.now().strftime("%Y-%m-%d")
        self.__notes = notes

    # --- Properties ---
    @property
    def id(self) -> str:
        return self.__id

    @property
    def diagnosis(self) -> str:
        return self.__diagnosis

    @diagnosis.setter
    def diagnosis(self, value: str) -> None:
        self.__diagnosis = value

    @property
    def treatment(self) -> str:
        return self.__treatment

    @treatment.setter
    def treatment(self, value: str) -> None:
        self.__treatment = value

    @property
    def date(self) -> str:
        return self.__date

    @property
    def notes(self) -> str:
        return self.__notes

    @notes.setter
    def notes(self, value: str) -> None:
        self.__notes = value

    # --- Magic methods ---
    def __str__(self) -> str:
        return f"Record {self.__id}: {self.__diagnosis} — {self.__treatment} ({self.__date})"

    def __repr__(self) -> str:
        return f"MedicalRecord(id='{self.__id}', diagnosis='{self.__diagnosis}')"

    # --- Serialization ---
    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.__id,
            "diagnosis": self.__diagnosis,
            "treatment": self.__treatment,
            "date": self.__date,
            "notes": self.__notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MedicalRecord":
        return cls(
            record_id=data["record_id"],
            diagnosis=data["diagnosis"],
            treatment=data["treatment"],
            date=data.get("date", ""),
            notes=data.get("notes", ""),
        )