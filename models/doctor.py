"""Doctor class — inherits from Person."""

from typing import Dict, Any
from .person import Person


class Doctor(Person):
    """Represents a doctor in the hospital."""

    total_doctors: int = 0  # Class variable

    def __init__(
        self,
        doctor_id: str,
        name: str,
        age: int,
        phone: str,
        gender: str,
        specialty: str,
        salary: float,
    ) -> None:
        super().__init__(doctor_id, name, age, phone, gender)
        self.__specialty = specialty
        self.__salary = salary  # Private — encapsulation
        Doctor.total_doctors += 1

    # --- Properties ---
    @property
    def specialty(self) -> str:
        return self.__specialty

    @specialty.setter
    def specialty(self, value: str) -> None:
        self.__specialty = value

    @property
    def salary(self) -> float:
        return self.__salary

    @salary.setter
    def salary(self, value: float) -> None:
        if value < 0:
            raise ValueError("Salary cannot be negative.")
        self.__salary = value

    # --- Polymorphism overrides ---
    def display_information(self) -> str:
        return f"Dr. {self.name} | ID: {self.id} | Specialty: {self.__specialty}"

    def show_details(self) -> str:
        base = super().show_details()
        return f"{base} | Specialty: {self.__specialty} | Salary: ${self.__salary:,.2f}"

    # --- Serialization ---
    def to_dict(self) -> Dict[str, Any]:
        return {
            "doctor_id": self.id,
            "name": self.name,
            "age": self.age,
            "phone": self.phone,
            "gender": self.gender,
            "specialty": self.__specialty,
            "salary": self.__salary,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Doctor":
        return cls(
            doctor_id=data["doctor_id"],
            name=data["name"],
            age=data["age"],
            phone=data["phone"],
            gender=data["gender"],
            specialty=data["specialty"],
            salary=data["salary"],
        )

    # --- Class methods ---
    @classmethod
    def get_total_doctors(cls) -> int:
        return cls.total_doctors

    @classmethod
    def reset_total(cls) -> None:
        cls.total_doctors = 0