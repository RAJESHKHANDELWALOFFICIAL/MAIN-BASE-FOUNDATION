"""MAIN BASE FOUNDATION database models.

Core data models for the database layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseInfo:
    """Database connection and configuration information."""

    database_path: str
    engine: str = "sqlite"
    version: str = "1.0"
    status: str = "UNKNOWN"
    connected: bool = False
    description: Optional[str] = None

    def to_dict(self) -> dict:
        """Return database information as a dictionary."""

        return {
            "database_path": self.database_path,
            "engine": self.engine,
            "version": self.version,
            "status": self.status,
            "connected": self.connected,
            "description": self.description,
        }


__all__ = [
    "DatabaseInfo",
]
