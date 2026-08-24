"""MAIN BASE FOUNDATION organization models."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Organization:
    """Represent a registered organization or operational entity."""

    organization_id: str
    organization_name: str
    organization_type: str
    operating_model: str
    country: str
    region: str

    owner_id: Optional[str] = None

    facility_type: Optional[str] = None

    status: str = "ACTIVE"
    verified: bool = False
    enabled: bool = True

    description: Optional[str] = None
