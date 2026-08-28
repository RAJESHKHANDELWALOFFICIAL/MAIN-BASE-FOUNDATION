```python
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
- Ownership
- Vault
- Integrations
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
# 👑 OWNERSHIP
# =========================================================

from .ownership import (
    EcosystemRole,
    OwnershipStatus,
    OwnershipAssignment,
    EntityOwnership,
    OwnershipTransfer,
    EcosystemPermission,
    PermissionScope,
    RolePermission,
    AccessDecision,
    OwnershipService,
    OwnershipController,
)


# =========================================================
# 🔐 VAULT
# =========================================================

from .vault import (
    VaultType,
    VaultStatus,
    VaultSecretType,
    VaultIntegrationReference,
    EcosystemVault,
    VaultAccessPolicy,
    VaultAccessDecision,
    VaultSecurity,
    VaultService,
    VaultController,
)


# =========================================================
# 🔌 INTEGRATION
# =========================================================

from .integration import (
    IntegrationProvider,
    IntegrationType,
    IntegrationStatus,
    IntegrationCredentialReference,
    EcosystemIntegration,
    IntegrationAuthorization,
    IntegrationAccessDecision,
    IntegrationService,
    IntegrationController,
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

    # -----------------------------------------------------
    # Media
    # -----------------------------------------------------

    "MediaType",
    "MediaPurpose",
    "MediaAsset",

    # -----------------------------------------------------
    # Profiles
    # -----------------------------------------------------

    "PersonalProfile",
    "ProfessionalProfile",
    "ProfileMediaBinding",

    # -----------------------------------------------------
    # Pages
    # -----------------------------------------------------

    "PageType",
    "PageVisibility",
    "EcosystemPage",

    # -----------------------------------------------------
    # Community
    # -----------------------------------------------------

    "CommunityVisibility",
    "CommunityType",
    "EcosystemGroup",
    "EcosystemChannel",
    "EcosystemCommunity",

    # -----------------------------------------------------
    # Ownership
    # -----------------------------------------------------

    "EcosystemRole",
    "OwnershipStatus",
    "OwnershipAssignment",
    "EntityOwnership",
    "OwnershipTransfer",
    "EcosystemPermission",
    "PermissionScope",
    "RolePermission",
    "AccessDecision",
    "OwnershipService",
    "OwnershipController",

    # -----------------------------------------------------
    # Vault
    # -----------------------------------------------------

    "VaultType",
    "VaultStatus",
    "VaultSecretType",
    "VaultIntegrationReference",
    "EcosystemVault",
    "VaultAccessPolicy",
    "VaultAccessDecision",
    "VaultSecurity",
    "VaultService",
    "VaultController",

    # -----------------------------------------------------
    # Integration
    # -----------------------------------------------------

    "IntegrationProvider",
    "IntegrationType",
    "IntegrationStatus",
    "IntegrationCredentialReference",
    "EcosystemIntegration",
    "IntegrationAuthorization",
    "IntegrationAccessDecision",
    "IntegrationService",
    "IntegrationController",

    # -----------------------------------------------------
    # Core Ecosystem
    # -----------------------------------------------------

    "EcosystemService",
    "EcosystemController",
]
```
