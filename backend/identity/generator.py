import random
import string


class IdentityGenerator:

    @staticmethod
    def generate_master_id():
        return "MBF-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

    @staticmethod
    def generate_identity_id():
        return "IDT-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

    @staticmethod
    def generate_user_id():
        return "USR-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

    @staticmethod
    def generate_organization_id():
        return "ORG-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

    @staticmethod
    def generate_business_id():
        return "BUS-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

    @staticmethod
    def generate_team_id():
        return "TEM-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

    @staticmethod
    def generate_project_id():
        return "PRJ-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

    @staticmethod
    def generate_profile_id():
        return "PRO-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

    @staticmethod
    def generate_session_id():
        return "SES-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
