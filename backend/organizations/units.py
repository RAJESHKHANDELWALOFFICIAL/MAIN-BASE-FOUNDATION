"""MAIN BASE FOUNDATION organization units."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class OrganizationUnit:
    """Represent an operational unit inside an organization."""

    unit_id: str
    organization_id: str
    parent_unit_id: Optional[str]
    unit_name: str
    unit_type: str
    country: str
    region: str
    status: str = "ACTIVE"
    enabled: bool = True
    description: Optional[str] = None
