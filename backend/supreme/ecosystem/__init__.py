"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Public Package Interface

Central public interface for the SUPREME ecosystem.

Exposes:
- Personal Profile
- Professional Profile
- Pages
- Groups
- Channels
- Communities
- Media
- Ecosystem Service
- Ecosystem Controller
"""

# =========================================================
# 🖼️ MEDIA
# =========================================================

from .media import (
    MediaType,
    MediaPurpose,
    MediaAsset,
)


# =========================================================
# 👤 PROFILES
# =========================================================

from .profile import (
    PersonalProfile,
    ProfessionalProfile,
    ProfileMediaBinding,
)


# =========================================================
# 📄 PAGES
# =========================================================

from .page import (
    PageType,
    PageVisibility,
    EcosystemPage,
)


# =========================================================
# 🌐 COMMUNITY
# =========================================================

from .community import (
    CommunityVisibility,
    CommunityType,
    EcosystemGroup,
    EcosystemChannel,
    EcosystemCommunity,
)


# =========================================================
# 🧠 SERVICE
# =========================================================

from .service import (
    EcosystemService,
)


# =========================================================
# 🎛️ CONTROLLER
# =========================================================

from .controller import (
    EcosystemController,
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [

    # Media
    "MediaType",
    "MediaPurpose",
    "MediaAsset",

    # Profiles
    "PersonalProfile",
    "ProfessionalProfile",
    "ProfileMediaBinding",

    # Pages
    "PageType",
    "PageVisibility",
    "EcosystemPage",

    # Community
    "CommunityVisibility",
    "CommunityType",
    "EcosystemGroup",
    "EcosystemChannel",
    "EcosystemCommunity",

    # Service
    "EcosystemService",

    # Controller
    "EcosystemController",
]
