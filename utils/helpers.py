"""Utility helper functions."""


class Helpers:
    """A collection of static utility methods."""

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Simple phone-number validation (at least 7 digits)."""
        cleaned = phone.replace("-", "").replace(" ", "").replace("+", "")
        return cleaned.isdigit() and len(cleaned) >= 7

    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Validate YYYY-MM-DD format loosely."""
        try:
            parts = date_str.split("-")
            if len(parts) != 3:
                return False
            y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
            return 1900 <= y <= 2100 and 1 <= m <= 12 and 1 <= d <= 31
        except (ValueError, IndexError):
            return False

    @staticmethod
    def generate_id(existing_ids: set, prefix: str = "") -> str:
        """Generate the next available integer ID."""
        n = 1
        while f"{prefix}{n}" in existing_ids:
            n += 1
        return f"{prefix}{n}"