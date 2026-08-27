"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Service

Central service for managing:
- Personal profiles
- Professional profiles
- Pages
- Groups
- Channels
- Communities
- Media assets

The service provides an in-memory ecosystem registry.
Persistent database integration can be added through the
existing SUPREME/database architecture without mixing
business logic into the models.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Union

from backend.supreme.ecosystem.media import (
    MediaAsset,
)

from backend.supreme.ecosystem.profile import (
    PersonalProfile,
    ProfessionalProfile,
)

from backend.supreme.ecosystem.page import (
    EcosystemPage,
)

from backend.supreme.ecosystem.community import (
    EcosystemGroup,
    EcosystemChannel,
    EcosystemCommunity,
)


EcosystemEntity = Union[
    PersonalProfile,
    ProfessionalProfile,
    EcosystemPage,
    EcosystemGroup,
    EcosystemChannel,
    EcosystemCommunity,
    MediaAsset,
]


class EcosystemService:
    """Central SUPREME ecosystem service."""

    def __init__(self) -> None:

        self._personal_profiles: Dict[
            str,
            PersonalProfile,
        ] = {}

        self._professional_profiles: Dict[
            str,
            ProfessionalProfile,
        ] = {}

        self._pages: Dict[
            str,
            EcosystemPage,
        ] = {}

        self._groups: Dict[
            str,
            EcosystemGroup,
        ] = {}

        self._channels: Dict[
            str,
            EcosystemChannel,
        ] = {}

        self._communities: Dict[
            str,
            EcosystemCommunity,
        ] = {}

        self._media: Dict[
            str,
            MediaAsset,
        ] = {}

        self._initialized = False

    # =========================================================
    # 🚀 INITIALIZE
    # =========================================================

    def initialize(self) -> dict:
        """Initialize the ecosystem service."""

        self._initialized = True

        return {
            "service": "SUPREME_ECOSYSTEM",
            "status": "READY",
            "initialized": True,
        }

    # =========================================================
    # 👤 PERSONAL PROFILE
    # =========================================================

    def create_personal_profile(
        self,
        profile: PersonalProfile,
    ) -> PersonalProfile:

        self._personal_profiles[
            profile.profile_id
        ] = profile

        return profile

    def get_personal_profile(
        self,
        profile_id: str,
    ) -> Optional[PersonalProfile]:

        return self._personal_profiles.get(
            profile_id
        )

    def delete_personal_profile(
        self,
        profile_id: str,
    ) -> bool:

        return (
            self._personal_profiles.pop(
                profile_id,
                None,
            )
            is not None
        )

    def list_personal_profiles(
        self,
    ) -> List[PersonalProfile]:

        return list(
            self._personal_profiles.values()
        )

    # =========================================================
    # 💼 PROFESSIONAL PROFILE
    # =========================================================

    def create_professional_profile(
        self,
        profile: ProfessionalProfile,
    ) -> ProfessionalProfile:

        self._professional_profiles[
            profile.profile_id
        ] = profile

        return profile

    def get_professional_profile(
        self,
        profile_id: str,
    ) -> Optional[ProfessionalProfile]:

        return self._professional_profiles.get(
            profile_id
        )

    def delete_professional_profile(
        self,
        profile_id: str,
    ) -> bool:

        return (
            self._professional_profiles.pop(
                profile_id,
                None,
            )
            is not None
        )

    def list_professional_profiles(
        self,
    ) -> List[ProfessionalProfile]:

        return list(
            self._professional_profiles.values()
        )

    # =========================================================
    # 📄 PAGE
    # =========================================================

    def create_page(
        self,
        page: EcosystemPage,
    ) -> EcosystemPage:

        self._pages[
            page.page_id
        ] = page

        return page

    def get_page(
        self,
        page_id: str,
    ) -> Optional[EcosystemPage]:

        return self._pages.get(
            page_id
        )

    def delete_page(
        self,
        page_id: str,
    ) -> bool:

        return (
            self._pages.pop(
                page_id,
                None,
            )
            is not None
        )

    def list_pages(
        self,
    ) -> List[EcosystemPage]:

        return list(
            self._pages.values()
        )

    # =========================================================
    # 👥 GROUP
    # =========================================================

    def create_group(
        self,
        group: EcosystemGroup,
    ) -> EcosystemGroup:

        self._groups[
            group.group_id
        ] = group

        return group

    def get_group(
        self,
        group_id: str,
    ) -> Optional[EcosystemGroup]:

        return self._groups.get(
            group_id
        )

    def delete_group(
        self,
        group_id: str,
    ) -> bool:

        return (
            self._groups.pop(
                group_id,
                None,
            )
            is not None
        )

    def list_groups(
        self,
    ) -> List[EcosystemGroup]:

        return list(
            self._groups.values()
        )

    # =========================================================
    # 📢 CHANNEL
    # =========================================================

    def create_channel(
        self,
        channel: EcosystemChannel,
    ) -> EcosystemChannel:

        self._channels[
            channel.channel_id
        ] = channel

        return channel

    def get_channel(
        self,
        channel_id: str,
    ) -> Optional[EcosystemChannel]:

        return self._channels.get(
            channel_id
        )

    def delete_channel(
        self,
        channel_id: str,
    ) -> bool:

        return (
            self._channels.pop(
                channel_id,
                None,
            )
            is not None
        )

    def list_channels(
        self,
    ) -> List[EcosystemChannel]:

        return list(
            self._channels.values()
        )

    # =========================================================
    # 🌐 COMMUNITY
    # =========================================================

    def create_community(
        self,
        community: EcosystemCommunity,
    ) -> EcosystemCommunity:

        self._communities[
            community.community_id
        ] = community

        return community

    def get_community(
        self,
        community_id: str,
    ) -> Optional[EcosystemCommunity]:

        return self._communities.get(
            community_id
        )

    def delete_community(
        self,
        community_id: str,
    ) -> bool:

        return (
            self._communities.pop(
                community_id,
                None,
            )
            is not None
        )

    def list_communities(
        self,
    ) -> List[EcosystemCommunity]:

        return list(
            self._communities.values()
        )

    # =========================================================
    # 🖼️ MEDIA
    # =========================================================

    def register_media(
        self,
        media: MediaAsset,
    ) -> MediaAsset:

        self._media[
            media.media_id
        ] = media

        return media

    def get_media(
        self,
        media_id: str,
    ) -> Optional[MediaAsset]:

        return self._media.get(
            media_id
        )

    def delete_media(
        self,
        media_id: str,
    ) -> bool:

        return (
            self._media.pop(
                media_id,
                None,
            )
            is not None
        )

    def list_media(
        self,
    ) -> List[MediaAsset]:

        return list(
            self._media.values()
        )

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return ecosystem service status."""

        return {
            "service": "SUPREME_ECOSYSTEM",
            "initialized": self._initialized,
            "personal_profiles": len(
                self._personal_profiles
            ),
            "professional_profiles": len(
                self._professional_profiles
            ),
            "pages": len(
                self._pages
            ),
            "groups": len(
                self._groups
            ),
            "channels": len(
                self._channels
            ),
            "communities": len(
                self._communities
            ),
            "media": len(
                self._media
            ),
        }


__all__ = [
    "EcosystemService",
]
