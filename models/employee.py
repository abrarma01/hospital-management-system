"""Employee class — inherits from Person (non-doctor staff)."""

from typing import Dict, Any
from .person import Person


class Employee(Person):
    """Represents a hospital employee who is not a doctor."""

    total_employees: int = 0  # Class variable

    def __init__(
        self,
        emp_id: str,
        name: str,
        age: int,
        phone: str,
        gender: str,
        role: str,
        salary: float,
    ) -> None:
        super().__init__(emp_id, name, age, phone, gender)
        self.__role = role
        self.__salary = salary
        Employee.total_employees += 1

    # --- Properties ---
    @property
    def role(self) -> str:
        return self.__role

    @role.setter
    def role(self, value: str) -> None:
        self.__role = value

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
        return f"{self.name} | ID: {self.id} | Role: {self.__role}"

    def show_details(self) -> str:
        base = super().show_details()
        return f"{base} | Role: {self.__role} | Salary: ${self.__salary:,.2f}"

    # --- Serialization ---
    def to_dict(self) -> Dict[str, Any]:
        return {
            "emp_id": self.id,
            "name": self.name,
            "age": self.age,
            "phone": self.phone,
            "gender": self.gender,
            "role": self.__role,
            "salary": self.__salary,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Employee":
        return cls(
            emp_id=data["emp_id"],
            name=data["name"],
            age=data["age"],
            phone=data["phone"],
            gender=data["gender"],
            role=data["role"],
            salary=data["salary"],
        )

    # --- Class methods ---
    @classmethod
    def get_total_employees(cls) -> int:
        return cls.total_employees

    @classmethod
    def reset_total(cls) -> None:
        cls.total_employees = 0