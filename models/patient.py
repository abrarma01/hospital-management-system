"""Patient class — inherits from Person."""

from typing import List, Dict, Any
from .person import Person
from .medical_record import MedicalRecord


class Patient(Person):
    """Represents a hospital patient.

    A Patient *owns* their MedicalRecords (composition).
    """

    total_patients: int = 0  # Class variable

    def __init__(
        self,
        patient_id: str,
        name: str,
        age: int,
        phone: str,
        gender: str,
        blood_type: str = "Unknown",
    ) -> None:
        super().__init__(patient_id, name, age, phone, gender)
        self.__blood_type = blood_type
        self.__medical_records: List[MedicalRecord] = []  # Composition
        Patient.total_patients += 1

    # --- Properties ---
    @property
    def blood_type(self) -> str:
        return self.__blood_type

    @blood_type.setter
    def blood_type(self, value: str) -> None:
        self.__blood_type = value

    @property
    def medical_records(self) -> List[MedicalRecord]:
        return self.__medical_records

    # --- Methods ---
    def add_medical_record(self, record: MedicalRecord) -> None:
        """Add a new medical record to this patient."""
        self.__medical_records.append(record)

    # --- Polymorphism overrides ---
    def display_information(self) -> str:
        return (
            f"Patient: {self.name} | ID: {self.id} | "
            f"Blood Type: {self.__blood_type} | Records: {len(self.__medical_records)}"
        )

    def show_details(self) -> str:
        base = super().show_details()
        return f"{base} | Blood Type: {self.__blood_type}"

    def get_medical_history(self) -> List[Dict[str, Any]]:
        """Return all records as a list of dictionaries."""
        return [r.to_dict() for r in self.__medical_records]

    # --- Magic method ---
    def __len__(self) -> int:
        """Return the number of medical records this patient has."""
        return len(self.__medical_records)

    # --- Serialization ---
    def to_dict(self) -> Dict[str, Any]:
        return {
            "patient_id": self.id,
            "name": self.name,
            "age": self.age,
            "phone": self.phone,
            "gender": self.gender,
            "blood_type": self.__blood_type,
            "medical_records": [r.to_dict() for r in self.__medical_records],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Patient":
        """Create a Patient from a dictionary (used when loading JSON)."""
        patient = cls(
            patient_id=data["patient_id"],
            name=data["name"],
            age=data["age"],
            phone=data["phone"],
            gender=data["gender"],
            blood_type=data.get("blood_type", "Unknown"),
        )
        for rd in data.get("medical_records", []):
            patient.add_medical_record(MedicalRecord.from_dict(rd))
        return patient

    # --- Class methods ---
    @classmethod
    def get_total_patients(cls) -> int:
        return cls.total_patients

    @classmethod
    def reset_total(cls) -> None:
        cls.total_patients = 0