"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Public Interface

Central public interface for:

- Mukti Mahal
- Family members
- Household staff
- Estate areas
- Pratap Group
- Business divisions
- Executive roles
- Capability evaluations
- Family visits
- Mukti principles
- Seed data
- Bootstrap
- Mukti Mahal service
- Mukti Mahal controller

No credentials or secrets are exposed here.
"""


# =========================================================
# 🏰 MUKTI MAHAL MODELS
# =========================================================

from .model import (
    utc_now,

    # World
    MuktiMahalSetting,

    # Family
    FamilyGeneration,
    CharacterGender,
    FamilyRole,

    # Business
    BusinessExecutiveRole,
    BusinessDivision,
    PratapGroup,
    BusinessCapabilityEvaluation,

    # Estate
    EstateAreaType,
    MuktiMahalEstateArea,
    MuktiMahal,

    # People
    MuktiMahalFamilyMember,
    MuktiMahalStaffMember,

    # Visit
    MuktiMahalFamilyVisit,

    # Principles
    MuktiPrinciples,
)


# =========================================================
# 🧠 MUKTI MAHAL SERVICE
# =========================================================

from .service import (
    MuktiMahalService,
)


# =========================================================
# 🎛️ MUKTI MAHAL CONTROLLER
# =========================================================

from .controller import (
    MuktiMahalController,
    mukti_mahal_controller,
)


# =========================================================
# 🌱 SEED DATA
# =========================================================

from .seed import (
    MUKTI_MAHAL_ID,
    PRATAP_GROUP_ID,

    MUKTI_MAHAL,
    PRATAP_GROUP,

    DADA,
    DADI,
    PAPA,
    MAA,
    BADE_PAPA,
    BADI_MAA,
    CHACHA,
    CHACHI,

    YOUNG_GENERATION,
    FAMILY_MEMBERS,

    CORE_STAFF,
    ESTATE_AREAS,

    seed_summary,
)


# =========================================================
# 🚀 BOOTSTRAP
# =========================================================

from .bootstrap import (
    bootstrap_mukti_mahal,
    create_default_mukti_mahal_service,
    bootstrap_summary,
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [

    # Time
    "utc_now",

    # World
    "MuktiMahalSetting",

    # Family
    "FamilyGeneration",
    "CharacterGender",
    "FamilyRole",

    # Business
    "BusinessExecutiveRole",
    "BusinessDivision",
    "PratapGroup",
    "BusinessCapabilityEvaluation",

    # Estate
    "EstateAreaType",
    "MuktiMahalEstateArea",
    "MuktiMahal",

    # People
    "MuktiMahalFamilyMember",
    "MuktiMahalStaffMember",

    # Visit
    "MuktiMahalFamilyVisit",

    # Principles
    "MuktiPrinciples",

    # Service
    "MuktiMahalService",

    # Controller
    "MuktiMahalController",
    "mukti_mahal_controller",

    # Seed
    "MUKTI_MAHAL_ID",
    "PRATAP_GROUP_ID",
    "MUKTI_MAHAL",
    "PRATAP_GROUP",
    "DADA",
    "DADI",
    "PAPA",
    "MAA",
    "BADE_PAPA",
    "BADI_MAA",
    "CHACHA",
    "CHACHI",
    "YOUNG_GENERATION",
    "FAMILY_MEMBERS",
    "CORE_STAFF",
    "ESTATE_AREAS",
    "seed_summary",

    # Bootstrap
    "bootstrap_mukti_mahal",
    "create_default_mukti_mahal_service",
    "bootstrap_summary",
]
