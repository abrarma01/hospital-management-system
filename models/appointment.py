"""Appointment class — uses aggregation with Doctor and Patient."""

from typing import Dict, Any
from .patient import Patient
from .doctor import Doctor


class Appointment:
    """Represents an appointment between a patient and a doctor.

    The Appointment *references* a Doctor and a Patient but does NOT own them.
    They can exist independently — this is **aggregation**.
    """

    def __init__(
        self,
        appointment_id: str,
        patient: Patient,
        doctor: Doctor,
        date: str,
        time: str,
        reason: str = "",
    ) -> None:
        self.__id = appointment_id
        self.__patient = patient    # Aggregation
        self.__doctor = doctor      # Aggregation
        self.__date = date
        self.__time = time
        self.__reason = reason
        self.__status = "Scheduled"

    # --- Properties ---
    @property
    def id(self) -> str:
        return self.__id

    @property
    def patient(self) -> Patient:
        return self.__patient

    @property
    def doctor(self) -> Doctor:
        return self.__doctor

    @property
    def date(self) -> str:
        return self.__date

    @date.setter
    def date(self, value: str) -> None:
        self.__date = value

    @property
    def time(self) -> str:
        return self.__time

    @time.setter
    def time(self, value: str) -> None:
        self.__time = value

    @property
    def reason(self) -> str:
        return self.__reason

    @reason.setter
    def reason(self, value: str) -> None:
        self.__reason = value

    @property
    def status(self) -> str:
        return self.__status

    def cancel(self) -> None:
        """Mark this appointment as cancelled."""
        self.__status = "Cancelled"

    # --- Magic methods ---
    def __str__(self) -> str:
        return (
            f"Appointment {self.__id}: {self.__patient.name} "
            f"with Dr. {self.__doctor.name} on {self.__date} at {self.__time}"
        )

    def __repr__(self) -> str:
        return (
            f"Appointment(id='{self.__id}', "
            f"patient='{self.__patient.name}', doctor='{self.__doctor.name}')"
        )

    # --- Serialization (stores IDs only, not full objects) ---
    def to_dict(self) -> Dict[str, Any]:
        return {
            "appointment_id": self.__id,
            "patient_id": self.__patient.id,
            "doctor_id": self.__doctor.id,
            "date": self.__date,
            "time": self.__time,
            "reason": self.__reason,
            "status": self.__status,
        }

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], patient: Patient, doctor: Doctor
    ) -> "Appointment":
        """Rebuild an Appointment from a dict + live Patient/Doctor objects."""
        appt = cls(
            appointment_id=data["appointment_id"],
            patient=patient,
            doctor=doctor,
            date=data["date"],
            time=data["time"],
            reason=data.get("reason", ""),
        )
        if data.get("status") == "Cancelled":
            appt.cancel()
        return appt