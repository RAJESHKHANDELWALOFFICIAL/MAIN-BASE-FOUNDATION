"""MAIN BASE FOUNDATION identity models.

Core identity data models for the identity layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class MasterIdentity:
    """Represent the primary identity record."""

    # ------------------------------------------------------------------
    # DATABASE
    # ------------------------------------------------------------------

    id: Optional[int] = None

    # ------------------------------------------------------------------
    # GLOBAL IDENTITY
    # ------------------------------------------------------------------

    master_id: str = ""
    identity_id: str = ""

    # ------------------------------------------------------------------
    # SUPREME OWNER
    # ------------------------------------------------------------------

    supreme_id: str = ""

    # ------------------------------------------------------------------
    # PERSONAL INFORMATION
    # ------------------------------------------------------------------

    full_name: str = ""
    display_name: str = ""
    username: str = ""

    # ------------------------------------------------------------------
    # CONTACT
    # ------------------------------------------------------------------

    email: str = ""
    phone: str = ""

    # ------------------------------------------------------------------
    # LOCATION
    # ------------------------------------------------------------------

    country: str = ""
    state: str = ""
    city: str = ""

    # ------------------------------------------------------------------
    # PREFERENCES
    # ------------------------------------------------------------------

    language: str = "en"
    timezone: str = "UTC"

    # ------------------------------------------------------------------
    # STATUS
    # ------------------------------------------------------------------

    status: str = "ACTIVE"
    verified: bool = False

    # ------------------------------------------------------------------
    # AUDIT
    # ------------------------------------------------------------------

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    # ------------------------------------------------------------------
    # SERIALIZATION
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return the identity record as a dictionary."""

        return {
            "id": self.id,
            "master_id": self.master_id,
            "identity_id": self.identity_id,
            "supreme_id": self.supreme_id,
            "full_name": self.full_name,
            "display_name": self.display_name,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "language": self.language,
            "timezone": self.timezone,
            "status": self.status,
            "verified": self.verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


__all__ = [
    "MasterIdentity",
]
