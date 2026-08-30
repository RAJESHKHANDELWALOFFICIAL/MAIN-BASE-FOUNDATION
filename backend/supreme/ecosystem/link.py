"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Link Model

Reusable link model for all SUPREME ecosystem entities.

Supported owners:
- Personal Profile
- Personal Page
- Personal Channel
- Personal Group
- Personal Community
- Business Profile
- Business Page
- Business Channel
- Business Group
- Business Community
- Organization Profile
- Organization Page
- Organization Channel
- Organization Group
- Organization Community

Features:
- Multiple links per entity
- Custom title
- Custom icon / emoji
- Custom URL
- Display ordering
- Active / inactive state

Design principles:
- No fixed five-link limit
- Link data remains separate from content
- The same architecture is reusable across the ecosystem
- Posts can reference saved ecosystem links later
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(
        timezone.utc
    ).isoformat()


@dataclass
class EcosystemLink:
    """
    Reusable link belonging to an ecosystem entity.
    """

    owner_type: str

    owner_id: str

    title: str

    url: str

    icon: str = ""

    display_order: int = 0

    active: bool = True

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not isinstance(
            self.owner_type,
            str,
        ) or not self.owner_type.strip():

            raise ValueError(
                "owner_type cannot be empty."
            )

        if not isinstance(
            self.owner_id,
            str,
        ) or not self.owner_id.strip():

            raise ValueError(
                "owner_id cannot be empty."
            )

        if not isinstance(
            self.title,
            str,
        ) or not self.title.strip():

            raise ValueError(
                "title cannot be empty."
            )

        if not isinstance(
            self.url,
            str,
        ) or not self.url.strip():

            raise ValueError(
                "url cannot be empty."
            )

        if self.display_order < 0:

            raise ValueError(
                "display_order cannot be negative."
            )


__all__ = [
    "EcosystemLink",
]
