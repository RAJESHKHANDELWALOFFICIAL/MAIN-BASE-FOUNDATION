from backend.identity.service import IdentityService


class AuthenticationService:

    def __init__(self):
        self.identity_service = IdentityService()

    def authenticate(self, master_id):
        identity = self.identity_service.get_identity(master_id)

        if identity is None:
            return {
                "authenticated": False,
                "message": "Identity not found"
            }

        return {
            "authenticated": True,
            "master_id": identity.master_id,
            "full_name": identity.full_name,
            "username": identity.primary_username,
            "status": identity.status
        }

    def initialize(self):
        return self.authenticate("MBF-000001")
