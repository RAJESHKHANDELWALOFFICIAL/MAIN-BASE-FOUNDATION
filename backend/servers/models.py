"""MAIN BASE FOUNDATION server models."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Server:
    """Registered server definition."""

    server_id: str
    server_name: str
    provider_id: str
    server_type: str
    server_role: str
    country: str
    region: str
    environment: str
    status: str = "REGISTERED"
    authorized: bool = False
    enabled: bool = True
    endpoint: Optional[str] = None
    protocol: Optional[str] = None
