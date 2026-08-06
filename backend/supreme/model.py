from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class SupremeOwner:

    # Database ID
    id: Optional[int] = None

    # Supreme Identity
    supreme_id: str = ""

    # Main Identity
    owner_name: str = ""

    username: str = ""

    email: str = ""

    phone: str = ""

    password: str = ""

    # Access
    role: str = "SUPREME_OWNER"

    level: int = 100

    status: str = "ACTIVE"

    # Security
    two_factor_enabled: bool = False

    recovery_email: Optional[str] = None

    recovery_phone: Optional[str] = None

    # Theme
    dashboard_name: str = "🔱 🕉️ SUPREME SHIV SHAKTI SYSTEM 🕉️ 🔱"

    # Audit
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
