"""Hospital class — the central service that manages all entities.

Uses **composition** to contain patients, doctors, employees, and appointments.
Handles all file I/O (JSON save / load).
"""

import json
import os
from typing import Dict, List, Any, Optional

from models.person import Person
from models.patient import Patient
from models.doctor import Doctor
from models.employee import Employee
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from exceptions.custom_exceptions import (
    DuplicateIDError,
    SchedulingConflictError,
    RecordNotFoundError,
)


class Hospital:
    """Central management class for the hospital.

    Composition relationships:
        - Hospital *contains* Patients, Doctors, Employees, Appointments.
    """

    DATA_DIR = "data"
    PATIENTS_FILE = os.path.join(DATA_DIR, "patients.json")
    DOCTORS_FILE = os.path.join(DATA_DIR, "doctors.json")
    EMPLOYEES_FILE = os.path.join(DATA_DIR, "employees.json")
    APPOINTMENTS_FILE = os.path.join(DATA_DIR, "appointments.json")

    def __init__(self, name: str = "General Hospital") -> None:
        self.__name = name
        self.__patients: Dict[str, Patient] = {}
        self.__doctors: Dict[str, Doctor] = {}
        self.__employees: Dict[str, Employee] = {}
        self.__appointments: Dict[str, Appointment] = {}
        self._ensure_data_dir()

    # --- Properties ---
    @property
    def name(self) -> str:
        return self.__name

    @property
    def patients(self) -> Dict[str, Patient]:
        return self.__patients

    @property
    def doctors(self) -> Dict[str, Doctor]:
        return self.__doctors

    @property
    def appointments(self) -> Dict[str, Appointment]:
        return self.__appointments

    @property
    def employees(self) -> Dict[str, Employee]:
        return self.__employees

    def _ensure_data_dir(self) -> None:
        os.makedirs(self.DATA_DIR, exist_ok=True)

    # ================================================================
    #  PATIENT MANAGEMENT
    # ================================================================
    def add_patient(self, patient: Patient) -> None:
        if patient.id in self.__patients:
            raise DuplicateIDError(patient.id, "Patient")
        self.__patients[patient.id] = patient

    def update_patient(
        self,
        patient_id: str,
        name: Optional[str] = None,
        age: Optional[int] = None,
        phone: Optional[str] = None,
        gender: Optional[str] = None,
        blood_type: Optional[str] = None,
    ) -> None:
        if patient_id not in self.__patients:
            raise RecordNotFoundError(patient_id, "Patient")
        p = self.__patients[patient_id]
        if name is not None:
            p.name = name
        if age is not None:
            p.age = age
        if phone is not None:
            p.phone = phone
        if gender is not None:
            p.gender = gender
        if blood_type is not None:
            p.blood_type = blood_type

    def remove_patient(self, patient_id: str) -> None:
        if patient_id not in self.__patients:
            raise RecordNotFoundError(patient_id, "Patient")
        del self.__patients[patient_id]

    def get_patient(self, patient_id: str) -> Patient:
        if patient_id not in self.__patients:
            raise RecordNotFoundError(patient_id, "Patient")
        return self.__patients[patient_id]

    def search_patients(self, keyword: str) -> List[Patient]:
        kw = keyword.lower()
        return [
            p
            for p in self.__patients.values()
            if kw in p.name.lower() or kw in p.id.lower()
        ]

    def get_all_patients(self) -> List[Patient]:
        return list(self.__patients.values())

    # ================================================================
    #  DOCTOR MANAGEMENT
    # ================================================================
    def add_doctor(self, doctor: Doctor) -> None:
        if doctor.id in self.__doctors:
            raise DuplicateIDError(doctor.id, "Doctor")
        self.__doctors[doctor.id] = doctor

    def update_doctor(
        self,
        doctor_id: str,
        name: Optional[str] = None,
        age: Optional[int] = None,
        phone: Optional[str] = None,
        specialty: Optional[str] = None,
        salary: Optional[float] = None,
    ) -> None:
        if doctor_id not in self.__doctors:
            raise RecordNotFoundError(doctor_id, "Doctor")
        d = self.__doctors[doctor_id]
        if name is not None:
            d.name = name
        if age is not None:
            d.age = age
        if phone is not None:
            d.phone = phone
        if specialty is not None:
            d.specialty = specialty
        if salary is not None:
            d.salary = salary

    def remove_doctor(self, doctor_id: str) -> None:
        if doctor_id not in self.__doctors:
            raise RecordNotFoundError(doctor_id, "Doctor")
        del self.__doctors[doctor_id]

    def get_doctor(self, doctor_id: str) -> Doctor:
        if doctor_id not in self.__doctors:
            raise RecordNotFoundError(doctor_id, "Doctor")
        return self.__doctors[doctor_id]

    def search_doctors(self, keyword: str) -> List[Doctor]:
        kw = keyword.lower()
        return [
            d
            for d in self.__doctors.values()
            if kw in d.name.lower() or kw in d.id.lower() or kw in d.specialty.lower()
        ]

    def get_all_doctors(self) -> List[Doctor]:
        return list(self.__doctors.values())

    # ================================================================
    #  EMPLOYEE MANAGEMENT
    # ================================================================
    def add_employee(self, employee: Employee) -> None:
        if employee.id in self.__employees:
            raise DuplicateIDError(employee.id, "Employee")
        self.__employees[employee.id] = employee

    def get_all_employees(self) -> List[Employee]:
        return list(self.__employees.values())

    # ================================================================
    #  APPOINTMENT MANAGEMENT
    # ================================================================
    def schedule_appointment(self, appointment: Appointment) -> None:
        if appointment.id in self.__appointments:
            raise DuplicateIDError(appointment.id, "Appointment")

        # Check for scheduling conflicts
        for existing in self.__appointments.values():
            if (
                existing.doctor.id == appointment.doctor.id
                and existing.date == appointment.date
                and existing.time == appointment.time
                and existing.status == "Scheduled"
            ):
                raise SchedulingConflictError(
                    appointment.doctor.name,
                    f"{appointment.date} at {appointment.time}",
                )

        self.__appointments[appointment.id] = appointment

    def cancel_appointment(self, appointment_id: str) -> None:
        if appointment_id not in self.__appointments:
            raise RecordNotFoundError(appointment_id, "Appointment")
        self.__appointments[appointment_id].cancel()

    def get_all_appointments(self) -> List[Appointment]:
        return list(self.__appointments.values())

    # ================================================================
    #  MEDICAL RECORDS
    # ================================================================
    def add_medical_record(
        self, patient_id: str, record: MedicalRecord
    ) -> None:
        if patient_id not in self.__patients:
            raise RecordNotFoundError(patient_id, "Patient")
        self.__patients[patient_id].add_medical_record(record)

    def get_patient_medical_history(self, patient_id: str) -> List[Dict[str, Any]]:
        if patient_id not in self.__patients:
            raise RecordNotFoundError(patient_id, "Patient")
        return self.__patients[patient_id].get_medical_history()

    # ================================================================
    #  STATISTICS
    # ================================================================
    def get_statistics(self) -> Dict[str, Any]:
        active = sum(
            1 for a in self.__appointments.values() if a.status == "Scheduled"
        )
        return {
            "hospital_name": self.__name,
            "total_patients": len(self.__patients),
            "total_doctors": len(self.__doctors),
            "total_employees": len(self.__employees),
            "total_appointments": len(self.__appointments),
            "active_appointments": active,
            "cancelled_appointments": len(self.__appointments) - active,
        }

    # ================================================================
    #  STATIC METHODS
    # ================================================================
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format a number as US-dollar currency string."""
        return f"${amount:,.2f}"

    @staticmethod
    def validate_id(id_value: str) -> bool:
        """Return True if id_value is a valid positive integer string."""
        try:
            return int(id_value) > 0
        except (ValueError, TypeError):
            return False

    # ================================================================
    #  FILE HANDLING  (JSON)
    # ================================================================
    def save_all_data(self) -> None:
        """Save every entity to its own JSON file."""
        with open(self.PATIENTS_FILE, "w") as f:
            json.dump([p.to_dict() for p in self.__patients.values()], f, indent=2)

        with open(self.DOCTORS_FILE, "w") as f:
            json.dump([d.to_dict() for d in self.__doctors.values()], f, indent=2)

        with open(self.EMPLOYEES_FILE, "w") as f:
            json.dump([e.to_dict() for e in self.__employees.values()], f, indent=2)

        with open(self.APPOINTMENTS_FILE, "w") as f:
            json.dump([a.to_dict() for a in self.__appointments.values()], f, indent=2)

    def load_all_data(self) -> None:
        """Load all entities from JSON files (called once at startup)."""
        # Reset class counters before loading
        Patient.reset_total()
        Doctor.reset_total()
        Employee.reset_total()
        Person.reset_total()

        # Patients
        if os.path.exists(self.PATIENTS_FILE):
            with open(self.PATIENTS_FILE, "r") as f:
                for pd in json.load(f):
                    p = Patient.from_dict(pd)
                    self.__patients[p.id] = p

        # Doctors
        if os.path.exists(self.DOCTORS_FILE):
            with open(self.DOCTORS_FILE, "r") as f:
                for dd in json.load(f):
                    d = Doctor.from_dict(dd)
                    self.__doctors[d.id] = d

        # Employees
        if os.path.exists(self.EMPLOYEES_FILE):
            with open(self.EMPLOYEES_FILE, "r") as f:
                for ed in json.load(f):
                    e = Employee.from_dict(ed)
                    self.__employees[e.id] = e

        # Appointments (need live Patient & Doctor objects — aggregation)
        if os.path.exists(self.APPOINTMENTS_FILE):
            with open(self.APPOINTMENTS_FILE, "r") as f:
                for ad in json.load(f):
                    patient = self.__patients.get(ad["patient_id"])
                    doctor = self.__doctors.get(ad["doctor_id"])
                    if patient and doctor:
                        appt = Appointment.from_dict(ad, patient, doctor)
                        self.__appointments[appt.id] = appt