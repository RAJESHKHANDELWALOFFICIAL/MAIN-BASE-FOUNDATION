from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class SupremeOwner:

    # Database
    id: Optional[int] = None

    # Supreme Identity
    supreme_id: str = ""

    # Personal Information
    owner_name: str = ""
    username: str = ""
    email: str = ""
    phone: str = ""
    password: str = ""

    # Access Control
    role: str = "SUPREME_OWNER"
    level: int = 100
    status: str = "ACTIVE"

    # Security
    two_factor_enabled: bool = False
    recovery_email: Optional[str] = None
    recovery_phone: Optional[str] = None

    # Dashboard
    dashboard_name: str = "🔱 🕉️ SUPREME SHIV SHAKTI SYSTEM 🕉️ 🔱"
    dashboard_theme: str = "SUPREME"

    # System
    system_version: str = "1.0.0"

    # Audit
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
