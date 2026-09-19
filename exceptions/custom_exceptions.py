"""Custom exception classes for the Hospital Management System."""


class HospitalManagementError(Exception):
    """Base exception for all hospital management errors."""

    pass


class DuplicateIDError(HospitalManagementError):
    """Raised when a duplicate ID is used."""

    def __init__(self, id_value: str, entity: str = "Record") -> None:
        self.id_value = id_value
        self.entity = entity
        super().__init__(f"{entity} with ID '{id_value}' already exists.")


class InvalidIDError(HospitalManagementError):
    """Raised when an invalid ID format is provided."""

    def __init__(self, id_value: str) -> None:
        self.id_value = id_value
        super().__init__(f"Invalid ID: '{id_value}'. ID must be a positive number.")


class SchedulingConflictError(HospitalManagementError):
    """Raised when an appointment conflicts with an existing one."""

    def __init__(self, doctor_name: str, date_time: str) -> None:
        self.doctor_name = doctor_name
        self.date_time = date_time
        super().__init__(
            f"Doctor '{doctor_name}' already has an appointment at {date_time}."
        )


class RecordNotFoundError(HospitalManagementError):
    """Raised when a requested record does not exist."""

    def __init__(self, id_value: str, entity: str = "Record") -> None:
        self.id_value = id_value
        self.entity = entity
        super().__init__(f"{entity} with ID '{id_value}' not found.")