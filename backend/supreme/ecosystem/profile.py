"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Profile Models

Central profile models for:
- Personal Profile
- Professional Profile

Media:
- Profile image
- Cover image

Design principles:
- Personal and professional identity remain separate.
- Profile ownership is explicit.
- Media references use MediaAsset.
- Original image aspect ratio is preserved.
- Forced image cropping is not required.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional

from backend.supreme.ecosystem.media import (
    MediaAsset,
)


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class PersonalProfile:
    """
    Personal ecosystem profile.

    Represents the owner's personal-facing identity data.
    """

    profile_id: str
    owner_id: str

    display_name: str = ""
    username: str = ""

    bio: str = ""

    profile_media_id: Optional[str] = None
    cover_media_id: Optional[str] = None

    location: str = ""
    website: str = ""

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

        if not self.profile_id.strip():
            raise ValueError(
                "profile_id cannot be empty."
            )

        if not self.owner_id.strip():
            raise ValueError(
                "owner_id cannot be empty."
            )

        if not self.display_name.strip():
            raise ValueError(
                "display_name cannot be empty."
            )


@dataclass
class ProfessionalProfile:
    """
    Professional ecosystem profile.

    Represents the professional/business-facing identity.
    """

    profile_id: str
    owner_id: str

    display_name: str = ""
    username: str = ""

    professional_title: str = ""
    headline: str = ""
    bio: str = ""

    company_name: str = ""
    designation: str = ""

    profile_media_id: Optional[str] = None
    cover_media_id: Optional[str] = None

    website: str = ""
    location: str = ""

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

        if not self.profile_id.strip():
            raise ValueError(
                "profile_id cannot be empty."
            )

        if not self.owner_id.strip():
            raise ValueError(
                "owner_id cannot be empty."
            )

        if not self.display_name.strip():
            raise ValueError(
                "display_name cannot be empty."
            )


@dataclass
class ProfileMediaBinding:
    """
    Connect a profile with its media assets.

    The media objects themselves remain managed by MediaAsset.
    """

    profile_id: str
    profile_media: Optional[MediaAsset] = None
    cover_media: Optional[MediaAsset] = None

    def __post_init__(self) -> None:

        if not self.profile_id.strip():
            raise ValueError(
                "profile_id cannot be empty."
            )

        if self.profile_media is not None:

            if not self.profile_media.is_profile_image:
                raise ValueError(
                    "profile_media must use "
                    "MediaPurpose.PROFILE_IMAGE."
                )

        if self.cover_media is not None:

            if not self.cover_media.is_cover_image:
                raise ValueError(
                    "cover_media must use "
                    "MediaPurpose.COVER_IMAGE."
                )


__all__ = [
    "PersonalProfile",
    "ProfessionalProfile",
    "ProfileMediaBinding",
]
