"""MAIN BASE FOUNDATION role models."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Role:
    """Represent a role assigned within an organization."""

    role_id: str
    role_name: str
    organization_id: str
    holder_id: str
    role_category: str
    authority_level: int
    scope: str
    appointment_type: str
    status: str = "ACTIVE"
    description: Optional[str] = None
