from datetime import datetime, timezone
import secrets

from backend.identity.service import IdentityService
from backend.users.service import UserService
from backend.auth.model import AuthenticationInfo


class AuthenticationService:

    def __init__(self):

        self.identity_service = IdentityService()
        self.user_service = UserService()

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

    def login_with_password(
        self,
        username: str,
        password: str
    ):

        user = self.user_service.search_user_by_username(
            username
        )

        if user is None:

            return {
                "authenticated": False,
                "message": "Invalid username or password"
            }

        verified = self.user_service.verify_user_password(
            username,
            password
        )

        if not verified:

            return {
                "authenticated": False,
                "message": "Invalid username or password"
            }

        if user.status != "ACTIVE":

            return {
                "authenticated": False,
                "message": "User account is not active"
            }

        now = datetime.now(timezone.utc).isoformat()

        session_id = secrets.token_urlsafe(32)
        token = secrets.token_urlsafe(48)

        return AuthenticationInfo(

            full_name=user.full_name,
            username=user.username,
            email=user.email,
            phone=user.phone,

            authenticated=True,

            session_id=session_id,
            token=token,

            status=user.status,

            last_login=now,
            created_at=now,
            updated_at=now

        )

    def login(
        self,
        master_id=None,
        username=None,
        password=None
    ):

        if username is not None and password is not None:

            return self.login_with_password(
                username,
                password
            )

        if master_id is not None:

            return self.authenticate(
                master_id
            )

        return {
            "authenticated": False,
            "message": "Authentication credentials required"
        }

    def logout(self):

        return {
            "authenticated": False,
            "message": "Logout Successful"
        }

    def initialize(self):

        return self.authenticate(
            "MBF-000001"
        )
