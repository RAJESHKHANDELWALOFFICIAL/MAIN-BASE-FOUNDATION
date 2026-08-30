"""
MAIN BASE FOUNDATION

SUPREME — Profile Link Model

Reusable links for ecosystem profiles.

Features:
- Multiple links per profile
- Custom title
- Custom icon / emoji
- Custom URL
- Display ordering
- Active / inactive state

Design principles:
- No fixed 5-link limit
- Users may create multiple profile links
- A profile link can later be referenced by posts
- Link data remains separate from post data
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
class ProfileLink:
    """
    Reusable link belonging to an ecosystem profile.
    """

    profile_id: str

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
            self.profile_id,
            str,
        ) or not self.profile_id.strip():

            raise ValueError(
                "profile_id cannot be empty."
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
    "ProfileLink",
]
