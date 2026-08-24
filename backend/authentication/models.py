"""MAIN BASE FOUNDATION authentication models."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Credential:
    """Represent an authentication credential reference."""

    credential_id: str
    owner_id: str
    credential_type: str
    provider_id: Optional[str] = None
    status: str = "REGISTERED"
    enabled: bool = True
