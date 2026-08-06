from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class MasterIdentity:

    # Database
    id: Optional[int] = None

    # Global Identity
    master_id: str = ""
    identity_id: str = ""

    # Supreme Owner
    supreme_id: str = ""

    # Personal Information
    full_name: str = ""
    display_name: str = ""
    username: str = ""

    # Contact
    email: str = ""
    phone: str = ""

    # Location
    country: str = ""
    state: str = ""
    city: str = ""

    # Preferences
    language: str = "en"
    timezone: str = "UTC"

    # Status
    status: str = "ACTIVE"
    verified: bool = False

    # Audit
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
