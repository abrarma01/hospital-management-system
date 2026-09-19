"""Abstract base class Person — parent of Patient, Doctor, and Employee."""

from abc import ABC, abstractmethod


class Person(ABC):
    """Abstract Base Class representing a person in the hospital.

    Every person has an ID, name, age, phone, and gender.
    Subclasses must implement display_information().
    """

    total_persons: int = 0  # Class variable

    def __init__(
        self, person_id: str, name: str, age: int, phone: str, gender: str
    ) -> None:
        self.__id = person_id      # Private — encapsulation
        self.__name = name
        self.__age = age
        self.__phone = phone
        self.__gender = gender
        Person.total_persons += 1

    # --- Properties (getters / setters) ---
    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, value: int) -> None:
        self.__age = value

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str) -> None:
        self.__phone = value

    @property
    def gender(self) -> str:
        return self.__gender

    @gender.setter
    def gender(self, value: str) -> None:
        self.__gender = value

    # --- Abstract method (abstraction) ---
    @abstractmethod
    def display_information(self) -> str:
        """Each subclass must provide its own implementation."""
        pass

    # --- Polymorphism: can be overridden ---
    def show_details(self) -> str:
        """Return a summary string. Subclasses may override this."""
        return (
            f"ID: {self.__id} | Name: {self.__name} | "
            f"Age: {self.__age} | Phone: {self.__phone} | Gender: {self.__gender}"
        )

    # --- Magic methods ---
    def __str__(self) -> str:
        return f"{self.__name} (ID: {self.__id})"

    def __repr__(self) -> str:
        return f"Person(id='{self.__id}', name='{self.__name}')"

    # --- Class methods ---
    @classmethod
    def get_total_persons(cls) -> int:
        """Return the total number of Person objects created."""
        return cls.total_persons

    @classmethod
    def reset_total(cls) -> None:
        """Reset the counter (used when loading saved data)."""
        cls.total_persons = 0