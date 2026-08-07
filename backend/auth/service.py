from backend.identity.service import IdentityService
from backend.auth.model import AuthenticationInfo


class AuthenticationService:

    def __init__(self):

        self.identity_service = IdentityService()

    def authenticate(self, master_id):

        identity = self.identity_service.get_identity(master_id)

        if identity is None:

            return {
                "authenticated": False,
                "message": "Identity Not Found"
            }

        return AuthenticationInfo(

            master_id=identity.master_id,
            identity_id=identity.identity_id,
            supreme_id=identity.supreme_id,

            full_name=identity.full_name,
            username=identity.username,
            email=identity.email,
            phone=identity.phone,

            authenticated=True,
            status=identity.status

        )

    def login(self, master_id):

        return self.authenticate(master_id)

    def logout(self):

        return {
            "authenticated": False,
            "message": "Logout Successful"
        }

    def initialize(self):

        return self.authenticate("MBF-000001")
