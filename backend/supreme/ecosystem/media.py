"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Media Models

Central media models for:
- Profile pictures
- Cover pictures
- General ecosystem media

Design principle:
- Preserve original media dimensions
- Preserve original aspect ratio
- Do not require forced cropping
- Support responsive full-image presentation
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


class MediaType(str, Enum):
    """Supported ecosystem media types."""

    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    DOCUMENT = "DOCUMENT"
    OTHER = "OTHER"


class MediaPurpose(str, Enum):
    """Purpose of an ecosystem media asset."""

    PROFILE_IMAGE = "PROFILE_IMAGE"
    COVER_IMAGE = "COVER_IMAGE"
    GENERAL = "GENERAL"


@dataclass
class MediaAsset:
    """
    Central ecosystem media asset.

    The model records the original dimensions and aspect ratio
    so presentation layers can display the complete image without
    requiring destructive cropping.
    """

    media_id: str
    owner_id: str

    media_type: MediaType = MediaType.IMAGE
    purpose: MediaPurpose = MediaPurpose.GENERAL

    file_name: str = ""
    mime_type: str = ""

    storage_key: str = ""

    original_width: Optional[int] = None
    original_height: Optional[int] = None

    preserve_aspect_ratio: bool = True
    allow_forced_crop: bool = False

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    active: bool = True

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.media_id.strip():
            raise ValueError(
                "media_id cannot be empty."
            )

        if not self.owner_id.strip():
            raise ValueError(
                "owner_id cannot be empty."
            )

        if self.original_width is not None:
            if self.original_width <= 0:
                raise ValueError(
                    "original_width must be greater than zero."
                )

        if self.original_height is not None:
            if self.original_height <= 0:
                raise ValueError(
                    "original_height must be greater than zero."
                )

        if self.media_type == MediaType.IMAGE:
            self.preserve_aspect_ratio = True
            self.allow_forced_crop = False

    @property
    def aspect_ratio(self) -> Optional[float]:
        """Return the original image aspect ratio."""

        if (
            self.original_width is None
            or self.original_height is None
        ):
            return None

        return (
            self.original_width
            / self.original_height
        )

    @property
    def is_profile_image(self) -> bool:
        """Return whether this asset is a profile image."""

        return (
            self.purpose
            == MediaPurpose.PROFILE_IMAGE
        )

    @property
    def is_cover_image(self) -> bool:
        """Return whether this asset is a cover image."""

        return (
            self.purpose
            == MediaPurpose.COVER_IMAGE
        )


__all__ = [
    "MediaType",
    "MediaPurpose",
    "MediaAsset",
]
