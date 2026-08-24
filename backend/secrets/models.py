"""MAIN BASE FOUNDATION secret models."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SecretReference:
    """Represent a reference to a protected secret."""

    secret_id: str
    owner_id: str
    secret_type: str
    provider_id: Optional[str] = None
    status: str = "REGISTERED"
    enabled: bool = True
