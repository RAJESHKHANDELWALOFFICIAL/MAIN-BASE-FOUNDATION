from dataclasses import dataclass, field
from datetime import datetime
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
    password: str = ""
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
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
