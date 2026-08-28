"""MAIN BASE FOUNDATION provider models."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Provider:
    """Registered infrastructure provider."""

    provider_id: str
    provider_name: str
    provider_type: str
    country: str
    region: str
    environment: str
    status: str = "REGISTERED"
    authorized: bool = False
    enabled: bool = True
    website: Optional[str] = None
    api_endpoint: Optional[str] = None
