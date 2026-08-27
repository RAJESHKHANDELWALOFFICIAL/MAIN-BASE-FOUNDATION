"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Community Models

Central models for:
- Groups
- Channels
- Communities

Design principles:
- Every ecosystem space has an explicit owner.
- Groups, channels and communities remain separate entity types.
- Profile and cover media are referenced through media IDs.
- Original media aspect ratio is preserved by the media layer.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


class CommunityVisibility(str, Enum):
    """Visibility states for ecosystem spaces."""

    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    UNLISTED = "UNLISTED"


class CommunityType(str, Enum):
    """Supported ecosystem space types."""

    GROUP = "GROUP"
    CHANNEL = "CHANNEL"
    COMMUNITY = "COMMUNITY"


@dataclass
class EcosystemGroup:
    """Central ecosystem group."""

    group_id: str
    owner_id: str

    name: str
    username: str = ""

    description: str = ""

    profile_media_id: Optional[str] = None
    cover_media_id: Optional[str] = None

    visibility: CommunityVisibility = (
        CommunityVisibility.PUBLIC
    )

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

        if not self.group_id.strip():
            raise ValueError(
                "group_id cannot be empty."
            )

        if not self.owner_id.strip():
            raise ValueError(
                "owner_id cannot be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "group name cannot be empty."
            )


@dataclass
class EcosystemChannel:
    """Central ecosystem channel."""

    channel_id: str
    owner_id: str

    name: str
    username: str = ""

    description: str = ""

    profile_media_id: Optional[str] = None
    cover_media_id: Optional[str] = None

    visibility: CommunityVisibility = (
        CommunityVisibility.PUBLIC
    )

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

        if not self.channel_id.strip():
            raise ValueError(
                "channel_id cannot be empty."
            )

        if not self.owner_id.strip():
            raise ValueError(
                "owner_id cannot be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "channel name cannot be empty."
            )


@dataclass
class EcosystemCommunity:
    """Central ecosystem community."""

    community_id: str
    owner_id: str

    name: str
    username: str = ""

    description: str = ""

    profile_media_id: Optional[str] = None
    cover_media_id: Optional[str] = None

    visibility: CommunityVisibility = (
        CommunityVisibility.PUBLIC
    )

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

        if not self.community_id.strip():
            raise ValueError(
                "community_id cannot be empty."
            )

        if not self.owner_id.strip():
            raise ValueError(
                "owner_id cannot be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "community name cannot be empty."
            )


__all__ = [
    "CommunityVisibility",
    "CommunityType",
    "EcosystemGroup",
    "EcosystemChannel",
    "EcosystemCommunity",
]
