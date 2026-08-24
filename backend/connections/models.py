"""MAIN BASE FOUNDATION connection models."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Connection:
    """Represent an authorized provider/server connection."""

    connection_id: str
    provider_id: str
    server_id: str
    connection_type: str
    protocol: str
    status: str = "REGISTERED"
    authorized: bool = False
    enabled: bool = True
    endpoint: Optional[str] = None
    error: Optional[str] = None
