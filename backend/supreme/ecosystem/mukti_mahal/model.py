"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Models

Central fictional-world models for:

- Mukti Mahal
- Family members
- Family generations
- Household staff
- Estate areas
- Pratap Group
- Business divisions
- Family business roles
- Young-generation board learning
- Capability-based succession

This module contains world/state models only.

Security principles:
- No passwords.
- No OTPs.
- No authentication secrets.
- No raw identity documents.
- No payment credentials.
- Protected creator functionality must use
  appropriate verification, consent, rights and moderation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional


# =========================================================
# 🕐 TIME
# =========================================================


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(
        timezone.utc
    ).isoformat()


# =========================================================
# 🏰 WORLD
# =========================================================


class MuktiMahalSetting(str, Enum):
    """Primary fictional world setting."""

    INDIA = "INDIA"
    MADHYA_PRADESH = "MADHYA_PRADESH"
    PRESENT_DAY = "PRESENT_DAY"


# =========================================================
# 👨‍👩‍👧 FAMILY GENERATION
# =========================================================


class FamilyGeneration(str, Enum):
    """Family generation classification."""

    FOUNDERS = "FOUNDERS"
    SENIOR_GENERATION = "SENIOR_GENERATION"
    YOUNG_GENERATION = "YOUNG_GENERATION"


# =========================================================
# 👤 GENDER
# =========================================================


class CharacterGender(str, Enum):
    """Character gender classification."""

    MALE = "MALE"
    FEMALE = "FEMALE"


# =========================================================
# 🏠 FAMILY ROLE
# =========================================================


class FamilyRole(str, Enum):
    """Primary family roles."""

    DADA = "DADA"
    DADI = "DADI"

    PAPA = "PAPA"
    MAA = "MAA"

    BADE_PAPA = "BADE_PAPA"
    BADI_MAA = "BADI_MAA"

    CHACHA = "CHACHA"
    CHACHI = "CHACHI"

    SON = "SON"
    DAUGHTER = "DAUGHTER"


# =========================================================
# 💼 BUSINESS EXECUTIVE ROLE
# =========================================================


class BusinessExecutiveRole(str, Enum):
    """Senior executive positions."""

    FOUNDER = "FOUNDER"
    CO_FOUNDER = "CO_FOUNDER"

    CHAIRMAN = "CHAIRMAN"
    MANAGING_DIRECTOR = "MANAGING_DIRECTOR"

    CEO = "CEO"
    CFO = "CFO"
    COO = "COO"
    CHRO = "CHRO"
    CMO = "CMO"
    CTO = "CTO"

    DIRECTOR = "DIRECTOR"
    EXECUTIVE_DIRECTOR = "EXECUTIVE_DIRECTOR"

    BOARD_MEMBER = "BOARD_MEMBER"
    BUSINESS_TRAINEE = "BUSINESS_TRAINEE"


# =========================================================
# 🏢 BUSINESS DIVISION
# =========================================================


class BusinessDivision(str, Enum):
    """Major Pratap Group business divisions."""

    REAL_ESTATE = "REAL_ESTATE"
    CONSTRUCTION = "CONSTRUCTION"

    HOTELS = "HOTELS"
    HOSPITALITY = "HOSPITALITY"
    RESTAURANTS = "RESTAURANTS"
    FOOD = "FOOD"

    TECHNOLOGY = "TECHNOLOGY"
    SOFTWARE = "SOFTWARE"
    AI = "AI"
    DIGITAL = "DIGITAL"

    MEDIA = "MEDIA"
    ENTERTAINMENT = "ENTERTAINMENT"
    PRODUCTION = "PRODUCTION"

    MARKETING = "MARKETING"
    ADVERTISING = "ADVERTISING"

    RETAIL = "RETAIL"
    ECOMMERCE = "ECOMMERCE"

    AUTOMOBILE = "AUTOMOBILE"
    TRANSPORTATION = "TRANSPORTATION"
    LOGISTICS = "LOGISTICS"

    MANUFACTURING = "MANUFACTURING"

    AGRICULTURE = "AGRICULTURE"
    FOOD_PROCESSING = "FOOD_PROCESSING"

    INVESTMENTS = "INVESTMENTS"
    FINANCIAL_SERVICES = "FINANCIAL_SERVICES"

    HEALTHCARE = "HEALTHCARE"
    EDUCATION = "EDUCATION"

    INTERNATIONAL_TRADE = "INTERNATIONAL_TRADE"
    BUSINESS_SERVICES = "BUSINESS_SERVICES"


# =========================================================
# 🏠 ESTATE AREA TYPE
# =========================================================


class EstateAreaType(str, Enum):
    """Types of Mukti Mahal estate areas."""

    MAIN_MANSION = "MAIN_MANSION"

    BEDROOM = "BEDROOM"
    FAMILY_LOUNGE = "FAMILY_LOUNGE"
    DINING_HALL = "DINING_HALL"
    KITCHEN = "KITCHEN"

    TEMPLE = "TEMPLE"
    GARDEN = "GARDEN"
    POOL = "POOL"

    GARAGE = "GARAGE"
    CINEMA = "CINEMA"
    GYM = "GYM"
    GAMING_ROOM = "GAMING_ROOM"
    MUSIC_ROOM = "MUSIC_ROOM"
    LIBRARY = "LIBRARY"

    OFFICE = "OFFICE"
    CONFERENCE_ROOM = "CONFERENCE_ROOM"
    CREATOR_STUDIO = "CREATOR_STUDIO"

    STAFF_QUARTERS = "STAFF_QUARTERS"
    DRIVER_QUARTERS = "DRIVER_QUARTERS"

    SECURITY_ROOM = "SECURITY_ROOM"
    MAINTENANCE_AREA = "MAINTENANCE_AREA"
    STORAGE = "STORAGE"

    TERRACE = "TERRACE"
    ROOFTOP_GARDEN = "ROOFTOP_GARDEN"
    EVENT_LAWN = "EVENT_LAWN"


# =========================================================
# 👥 STAFF TYPE
# =========================================================


class StaffType(str, Enum):
    """Mukti Mahal household and support staff categories."""

    ESTATE_MANAGER = "ESTATE_MANAGER"
    PERSONAL_ASSISTANT = "PERSONAL_ASSISTANT"

    BUSINESS_MANAGER = "BUSINESS_MANAGER"
    ADMINISTRATION = "ADMINISTRATION"

    HR = "HR"
    FINANCE = "FINANCE"
    LEGAL = "LEGAL"
    IT = "IT"
    AI = "AI"

    MEDIA = "MEDIA"
    MARKETING = "MARKETING"
    OPERATIONS = "OPERATIONS"

    CHEF = "CHEF"
    HOUSEKEEPING = "HOUSEKEEPING"
    GARDEN = "GARDEN"
    MAINTENANCE = "MAINTENANCE"

    DRIVER = "DRIVER"
    SECURITY = "SECURITY"
    MEDICAL = "MEDICAL"

    OTHER = "OTHER"


# =========================================================
# 🏢 PRATAP GROUP
# =========================================================


@dataclass
class PratapGroup:
    """Fictional family-owned business group."""

    group_id: str

    name: str = "PRATAP GROUP"

    headquarters_country: str = "INDIA"

    headquarters_state: str = "MADHYA PRADESH"

    international_operations: bool = True

    business_divisions: List[
        BusinessDivision
    ] = field(
        default_factory=list
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

        if not self.name.strip():
            self.name = "PRATAP GROUP"


# =========================================================
# 👤 FAMILY MEMBER
# =========================================================


@dataclass
class MuktiMahalFamilyMember:
    """A fictional Mukti Mahal family member."""

    character_id: str

    name: str

    age: int

    gender: CharacterGender

    generation: FamilyGeneration

    family_role: FamilyRole

    parent_ids: List[str] = field(
        default_factory=list
    )

    spouse_id: Optional[str] = None

    education: str = ""

    interests: List[str] = field(
        default_factory=list
    )

    skills: List[str] = field(
        default_factory=list
    )

    business_interests: List[
        BusinessDivision
    ] = field(
        default_factory=list
    )

    executive_role: Optional[
        BusinessExecutiveRole
    ] = None

    board_member: bool = False

    learning_status: str = ""

    capability_proven: bool = False

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

        if not self.character_id.strip():
            raise ValueError(
                "character_id cannot be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "name cannot be empty."
            )

        if self.age < 0:
            raise ValueError(
                "age cannot be negative."
            )

        if (
            self.generation
            == FamilyGeneration.YOUNG_GENERATION
            and self.age < 20
        ):
            raise ValueError(
                "Young-generation Mukti Mahal characters "
                "must be adults aged 20 or above."
            )


# =========================================================
# 👥 HOUSEHOLD STAFF
# =========================================================


@dataclass
class MuktiMahalStaffMember:
    """A fictional Mukti Mahal staff member."""

    staff_id: str

    name: str

    age: int

    gender: CharacterGender

    staff_type: StaffType

    department: str = ""

    residence_area: str = ""

    responsibilities: List[str] = field(
        default_factory=list
    )

    active: bool = True

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.staff_id.strip():
            raise ValueError(
                "staff_id cannot be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "name cannot be empty."
            )

        if self.age < 18:
            raise ValueError(
                "Staff members must be adults."
            )


# =========================================================
# 🏰 ESTATE AREA
# =========================================================


@dataclass
class MuktiMahalEstateArea:
    """A physical area within the Mukti Mahal estate."""

    area_id: str

    name: str

    area_type: EstateAreaType

    floor: Optional[int] = None

    description: str = ""

    capacity: Optional[int] = None

    private: bool = False

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

        if not self.area_id.strip():
            raise ValueError(
                "area_id cannot be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "name cannot be empty."
            )

        if self.floor is not None:
            if self.floor < -1:
                raise ValueError(
                    "floor cannot be below basement level."
                )

        if self.capacity is not None:
            if self.capacity <= 0:
                raise ValueError(
                    "capacity must be greater than zero."
                )


# =========================================================
# 🏰 MUKTI MAHAL
# =========================================================


@dataclass
class MuktiMahal:
    """Central fictional Mukti Mahal estate."""

    mahal_id: str

    name: str = "MUKTI MAHAL"

    country: str = "INDIA"

    state: str = "MADHYA PRADESH"

    setting: MuktiMahalSetting = (
        MuktiMahalSetting.PRESENT_DAY
    )

    area_acres: float = 10.0

    basement_count: int = 1

    floor_count: int = 5

    family_member_ids: List[str] = field(
        default_factory=list
    )

    staff_member_ids: List[str] = field(
        default_factory=list
    )

    estate_area_ids: List[str] = field(
        default_factory=list
    )

    group_id: Optional[str] = None

    description: str = (
        "Large multi-generation family estate "
        "in Madhya Pradesh, India."
    )

    active: bool = True

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.mahal_id.strip():
            raise ValueError(
                "mahal_id cannot be empty."
            )

        if not self.name.strip():
            self.name = "MUKTI MAHAL"

        if self.area_acres <= 0:
            raise ValueError(
                "area_acres must be greater than zero."
            )

        if self.basement_count < 0:
            raise ValueError(
                "basement_count cannot be negative."
            )

        if self.floor_count <= 0:
            raise ValueError(
                "floor_count must be greater than zero."
            )


# =========================================================
# 🎓 CAPABILITY EVALUATION
# =========================================================


@dataclass
class BusinessCapabilityEvaluation:
    """
    Capability evaluation for young-generation
    business development.

    Family relationship alone does not establish
    executive qualification.
    """

    evaluation_id: str

    character_id: str

    evaluated_by: str

    business_division: BusinessDivision

    knowledge_score: float = 0.0

    leadership_score: float = 0.0

    execution_score: float = 0.0

    problem_solving_score: float = 0.0

    ethics_score: float = 0.0

    overall_score: float = 0.0

    passed: bool = False

    recommendation: str = ""

    created_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.evaluation_id.strip():
            raise ValueError(
                "evaluation_id cannot be empty."
            )

        if not self.character_id.strip():
            raise ValueError(
                "character_id cannot be empty."
            )

        if not self.evaluated_by.strip():
            raise ValueError(
                "evaluated_by cannot be empty."
            )

        for score_name in (
            "knowledge_score",
            "leadership_score",
            "execution_score",
            "problem_solving_score",
            "ethics_score",
            "overall_score",
        ):
            score = getattr(
                self,
                score_name,
            )

            if score < 0 or score > 100:
                raise ValueError(
                    f"{score_name} must be between 0 and 100."
                )


# =========================================================
# 🤝 FAMILY VISIT
# =========================================================


@dataclass
class MuktiMahalFamilyVisit:
    """
    One-day visit by another fictional family.

    Used for story/world events.
    """

    visit_id: str

    host_mahal_id: str

    visiting_family_name: str

    visiting_grandfather_name: str

    visiting_grandmother_name: str

    visiting_son_name: str

    visiting_daughter_in_law_name: str

    visiting_grandchildren: List[str] = field(
        default_factory=list
    )

    visiting_staff_ids: List[str] = field(
        default_factory=list
    )

    duration_days: int = 1

    welcome_completed: bool = False

    introductions_completed: bool = False

    dinner_completed: bool = False

    business_discussion_completed: bool = False

    completed: bool = False

    created_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.visit_id.strip():
            raise ValueError(
                "visit_id cannot be empty."
            )

        if not self.host_mahal_id.strip():
            raise ValueError(
                "host_mahal_id cannot be empty."
            )

        if not self.visiting_family_name.strip():
            raise ValueError(
                "visiting_family_name cannot be empty."
            )

        if self.duration_days <= 0:
            raise ValueError(
                "duration_days must be greater than zero."
            )


# =========================================================
# 📜 MUKTI PRINCIPLES
# =========================================================


@dataclass(frozen=True)
class MuktiPrinciples:
    """
    High-level fictional-world principles.

    Freedom is paired with consent, privacy,
    responsibility, safety and applicable law.
    """

    respect_required: bool = True

    consent_required: bool = True

    privacy_respected: bool = True

    personal_choice_respected: bool = True

    social_pressure_not_required: bool = True

    family_responsibility_required: bool = True

    business_capability_required: bool = True

    applicable_law_required: bool = True

    safety_required: bool = True


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
]
    OPERATIONS = "OPERATIONS"
