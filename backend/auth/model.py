from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class AuthenticationInfo:

    # Database
    id: Optional[int] = None

    # Identity
    master_id: str = ""
    identity_id: str = ""
    supreme_id: str = ""

    # User
    full_name: str = ""
    username: str = ""
    email: str = ""
    phone: str = ""

    # Authentication
    authenticated: bool = False

    # Session
    session_id: str = ""
    token: str = ""

    # Status
    status: str = "ACTIVE"

    # Login
    last_login: Optional[str] = None

    # Audit
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        """Return a safe authentication response."""

        return {
            "id": self.id,
            "master_id": self.master_id,
            "identity_id": self.identity_id,
            "supreme_id": self.supreme_id,
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "authenticated": self.authenticated,
            "session_id": self.session_id,
            "token": self.token,
            "status": self.status,
            "last_login": self.last_login,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


__all__ = ["AuthenticationInfo"]
