import re


class IdentityValidator:

    @staticmethod
    def validate_username(username):
        return len(username) >= 3

    @staticmethod
    def validate_email(email):
        pattern = r"^[^@]+@[^@]+\.[^@]+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        return phone.isdigit() and 10 <= len(phone) <= 15

    @staticmethod
    def validate_master_id(master_id):
        return master_id.startswith("MBF-")

    @staticmethod
    def validate_status(status):
        return status.upper() in [
            "ACTIVE",
            "INACTIVE",
            "BLOCKED",
            "DELETED",
        ]
