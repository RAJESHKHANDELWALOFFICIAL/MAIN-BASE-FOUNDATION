from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from backend.identity.service import IdentityService
from backend.users.service import UserService
from backend.database.service import DatabaseService
from backend.auth.model import AuthenticationInfo


class AuthenticationService:

    SESSION_DURATION_HOURS = 24

    def __init__(self):

        self.identity_service = IdentityService()
        self.user_service = UserService()
        self.database_service = DatabaseService()

        self.initialize_sessions()

    # ------------------------------------------------------------------
    # SESSION DATABASE
    # ------------------------------------------------------------------

    def initialize_sessions(self):

        self.database_service.initialize()

        self.database_service.execute(
            """
            CREATE TABLE IF NOT EXISTS auth_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL UNIQUE,
                token_hash TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                revoked_at TEXT,
                updated_at TEXT NOT NULL
            )
            """
        )

        return {
            "success": True,
            "message": "Authentication session storage initialized"
        }

    # ------------------------------------------------------------------
    # TOKEN SECURITY
    # ------------------------------------------------------------------

    @staticmethod
    def hash_token(token: str) -> str:
        """Return a one-way hash of an authentication token."""

        return hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()

    # ------------------------------------------------------------------
    # IDENTITY AUTHENTICATION
    # ------------------------------------------------------------------

    def authenticate(self, master_id):

        identity = self.identity_service.get_identity(
            master_id
        )

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

    # ------------------------------------------------------------------
    # PASSWORD LOGIN
    # ------------------------------------------------------------------

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

        now = datetime.now(timezone.utc)

        created_at = now.isoformat()

        expires_at = (
            now + timedelta(
                hours=self.SESSION_DURATION_HOURS
            )
        ).isoformat()

        session_id = secrets.token_urlsafe(32)

        token = secrets.token_urlsafe(48)

        token_hash = self.hash_token(token)

        self.database_service.execute(
            """
            INSERT INTO auth_sessions (
                session_id,
                token_hash,
                username,
                status,
                created_at,
                expires_at,
                revoked_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                token_hash,
                user.username,
                "ACTIVE",
                created_at,
                expires_at,
                None,
                created_at,
            )
        )

        return AuthenticationInfo(

            full_name=user.full_name,
            username=user.username,
            email=user.email,
            phone=user.phone,

            authenticated=True,

            session_id=session_id,
            token=token,

            status=user.status,

            last_login=created_at,
            created_at=created_at,
            updated_at=created_at

        )

    # ------------------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # TOKEN VALIDATION
    # ------------------------------------------------------------------

    def validate_token(self, token: str):

        if not token:

            return {
                "authenticated": False,
                "message": "Authentication token required"
            }

        token_hash = self.hash_token(token)

        session = self.database_service.fetchone(
            """
            SELECT
                session_id,
                username,
                status,
                created_at,
                expires_at,
                revoked_at
            FROM auth_sessions
            WHERE token_hash = ?
            """,
            (token_hash,)
        )

        if session is None:

            return {
                "authenticated": False,
                "message": "Invalid authentication token"
            }

        if session["status"] != "ACTIVE":

            return {
                "authenticated": False,
                "message": "Authentication session is not active"
            }

        if session["revoked_at"] is not None:

            return {
                "authenticated": False,
                "message": "Authentication session has been revoked"
            }

        expires_at = datetime.fromisoformat(
            session["expires_at"]
        )

        if expires_at <= datetime.now(timezone.utc):

            self.database_service.execute(
                """
                UPDATE auth_sessions
                SET
                    status = ?,
                    updated_at = ?
                WHERE token_hash = ?
                """,
                (
                    "EXPIRED",
                    datetime.now(timezone.utc).isoformat(),
                    token_hash,
                )
            )

            return {
                "authenticated": False,
                "message": "Authentication session has expired"
            }

        return {
            "authenticated": True,
            "message": "Authentication token is valid",
            "session_id": session["session_id"],
            "username": session["username"],
            "status": session["status"],
            "created_at": session["created_at"],
            "expires_at": session["expires_at"],
        }

    # ------------------------------------------------------------------
    # LOGOUT
    # ------------------------------------------------------------------

    def logout(
        self,
        token: str | None = None,
        session_id: str | None = None
    ):

        if token is None and session_id is None:

            return {
                "authenticated": False,
                "message": "Authentication token or session ID required"
            }

        now = datetime.now(timezone.utc).isoformat()

        if token is not None:

            token_hash = self.hash_token(token)

            session = self.database_service.fetchone(
                """
                SELECT session_id
                FROM auth_sessions
                WHERE token_hash = ?
                """,
                (token_hash,)
            )

            if session is None:

                return {
                    "authenticated": False,
                    "message": "Authentication session not found"
                }

            self.database_service.execute(
                """
                UPDATE auth_sessions
                SET
                    status = ?,
                    revoked_at = ?,
                    updated_at = ?
                WHERE token_hash = ?
                """,
                (
                    "REVOKED",
                    now,
                    now,
                    token_hash,
                )
            )

        else:

            session = self.database_service.fetchone(
                """
                SELECT session_id
                FROM auth_sessions
                WHERE session_id = ?
                """,
                (session_id,)
            )

            if session is None:

                return {
                    "authenticated": False,
                    "message": "Authentication session not found"
                }

            self.database_service.execute(
                """
                UPDATE auth_sessions
                SET
                    status = ?,
                    revoked_at = ?,
                    updated_at = ?
                WHERE session_id = ?
                """,
                (
                    "REVOKED",
                    now,
                    now,
                    session_id,
                )
            )

        return {
            "authenticated": False,
            "message": "Logout Successful"
        }

    # ------------------------------------------------------------------
    # INITIALIZE
    # ------------------------------------------------------------------

    def initialize(self):

        return self.authenticate(
            "MBF-000001"
        )
