"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Seed Data

Initial fictional world configuration for:

- Mukti Mahal
- Pratap family
- Household staff
- Estate areas
- Pratap Group
- Business divisions
- Senior-generation roles
- Young-generation board learning

This file contains fictional seed data only.
No credentials, passwords, OTPs or secrets are stored here.
"""

from __future__ import annotations

from .model import (
    BusinessDivision,
    BusinessExecutiveRole,
    CharacterGender,
    EstateAreaType,
    FamilyGeneration,
    FamilyRole,
    MuktiMahal,
    MuktiMahalEstateArea,
    MuktiMahalFamilyMember,
    MuktiMahalStaffMember,
    PratapGroup,
    StaffType,
)


# =========================================================
# 🏰 CORE IDENTIFIERS
# =========================================================

MUKTI_MAHAL_ID = "mukti_mahal_mp"
PRATAP_GROUP_ID = "pratap_group"

DADA_ID = "rajendra_pratap"
DADI_ID = "savitri_devi"

PAPA_ID = "arvind_pratap"
MAA_ID = "sunita_pratap"

BADE_PAPA_ID = "mahendra_pratap"
BADI_MAA_ID = "kamla_pratap"

CHACHA_ID = "vikram_pratap"
CHACHI_ID = "neelam_pratap"


# =========================================================
# 🏰 MUKTI MAHAL
# =========================================================

MUKTI_MAHAL = MuktiMahal(
    mahal_id=MUKTI_MAHAL_ID,
    name="MUKTI MAHAL",
    country="INDIA",
    state="MADHYA PRADESH",
    area_acres=10.0,
    basement_count=1,
    floor_count=5,
    group_id=PRATAP_GROUP_ID,
)


# =========================================================
# 👑 FOUNDERS
# =========================================================

DADA = MuktiMahalFamilyMember(
    character_id=DADA_ID,
    name="Rajendra Pratap",
    age=72,
    gender=CharacterGender.MALE,
    generation=FamilyGeneration.FOUNDERS,
    family_role=FamilyRole.DADA,
    education="Traditional business education and lifelong practical experience",
    interests=[
        "Family",
        "Business",
        "Tradition",
        "Gardening",
        "Temple",
    ],
    skills=[
        "Leadership",
        "Business Strategy",
        "Negotiation",
        "Mentorship",
    ],
    business_interests=[
        BusinessDivision.REAL_ESTATE,
        BusinessDivision.INVESTMENTS,
        BusinessDivision.CONSTRUCTION,
    ],
    executive_role=BusinessExecutiveRole.FOUNDER,
)


DADI = MuktiMahalFamilyMember(
    character_id=DADI_ID,
    name="Savitri Devi",
    age=68,
    gender=CharacterGender.FEMALE,
    generation=FamilyGeneration.FOUNDERS,
    family_role=FamilyRole.DADI,
    education="Traditional education and family-business experience",
    interests=[
        "Family",
        "Tradition",
        "Cooking",
        "Garden",
        "Charity",
    ],
    skills=[
        "Family Leadership",
        "People Management",
        "Hospitality",
        "Mentorship",
    ],
    business_interests=[
        BusinessDivision.HOTELS,
        BusinessDivision.HOSPITALITY,
        BusinessDivision.EDUCATION,
    ],
    executive_role=BusinessExecutiveRole.CO_FOUNDER,
)


# =========================================================
# 🏢 SENIOR GENERATION
# =========================================================

PAPA = MuktiMahalFamilyMember(
    character_id=PAPA_ID,
    name="Arvind Pratap",
    age=48,
    gender=CharacterGender.MALE,
    generation=FamilyGeneration.SENIOR_GENERATION,
    family_role=FamilyRole.PAPA,
    parent_ids=[DADA_ID, DADI_ID],
    spouse_id=MAA_ID,
    education="Business Administration",
    interests=[
        "Business",
        "Strategy",
        "Technology",
        "Travel",
    ],
    skills=[
        "Leadership",
        "Operations",
        "Business Strategy",
        "Management",
    ],
    business_interests=[
        BusinessDivision.REAL_ESTATE,
        BusinessDivision.TECHNOLOGY,
        BusinessDivision.AI,
        BusinessDivision.DIGITAL,
    ],
    executive_role=BusinessExecutiveRole.CEO,
)


MAA = MuktiMahalFamilyMember(
    character_id=MAA_ID,
    name="Sunita Pratap",
    age=45,
    gender=CharacterGender.FEMALE,
    generation=FamilyGeneration.SENIOR_GENERATION,
    family_role=FamilyRole.MAA,
    parent_ids=[DADA_ID, DADI_ID],
    spouse_id=PAPA_ID,
    education="Human Resources and Organizational Management",
    interests=[
        "People",
        "Education",
        "Family",
        "Leadership",
    ],
    skills=[
        "Human Resources",
        "Leadership Development",
        "Communication",
        "People Management",
    ],
    business_interests=[
        BusinessDivision.EDUCATION,
        BusinessDivision.BUSINESS_SERVICES,
    ],
    executive_role=BusinessExecutiveRole.CHRO,
)


BADE_PAPA = MuktiMahalFamilyMember(
    character_id=BADE_PAPA_ID,
    name="Mahendra Pratap",
    age=52,
    gender=CharacterGender.MALE,
    generation=FamilyGeneration.SENIOR_GENERATION,
    family_role=FamilyRole.BADE_PAPA,
    parent_ids=[DADA_ID, DADI_ID],
    spouse_id=BADI_MAA_ID,
    education="Business Management",
    interests=[
        "Business",
        "Investments",
        "Construction",
        "Strategy",
    ],
    skills=[
        "Corporate Governance",
        "Strategic Planning",
        "Negotiation",
        "Leadership",
    ],
    business_interests=[
        BusinessDivision.INVESTMENTS,
        BusinessDivision.CONSTRUCTION,
        BusinessDivision.MANUFACTURING,
    ],
    executive_role=BusinessExecutiveRole.CHAIRMAN,
)


BADI_MAA = MuktiMahalFamilyMember(
    character_id=BADI_MAA_ID,
    name="Kamla Pratap",
    age=49,
    gender=CharacterGender.FEMALE,
    generation=FamilyGeneration.SENIOR_GENERATION,
    family_role=FamilyRole.BADI_MAA,
    parent_ids=[DADA_ID, DADI_ID],
    spouse_id=BADE_PAPA_ID,
    education="Finance and Accounting",
    interests=[
        "Finance",
        "Investments",
        "Education",
        "Family",
    ],
    skills=[
        "Financial Planning",
        "Accounting",
        "Risk Management",
        "Investment Analysis",
    ],
    business_interests=[
        BusinessDivision.INVESTMENTS,
        BusinessDivision.FINANCIAL_SERVICES,
    ],
    executive_role=BusinessExecutiveRole.CFO,
)


CHACHA = MuktiMahalFamilyMember(
    character_id=CHACHA_ID,
    name="Vikram Pratap",
    age=42,
    gender=CharacterGender.MALE,
    generation=FamilyGeneration.SENIOR_GENERATION,
    family_role=FamilyRole.CHACHA,
    parent_ids=[DADA_ID, DADI_ID],
    spouse_id=CHACHI_ID,
    education="Operations and Business Management",
    interests=[
        "Operations",
        "Technology",
        "Travel",
        "Business",
    ],
    skills=[
        "Operations",
        "Execution",
        "Team Management",
        "Process Improvement",
    ],
    business_interests=[
        BusinessDivision.LOGISTICS,
        BusinessDivision.MANUFACTURING,
    ],
    executive_role=BusinessExecutiveRole.COO,
)


CHACHI = MuktiMahalFamilyMember(
    character_id=CHACHI_ID,
    name="Neelam Pratap",
    age=39,
    gender=CharacterGender.FEMALE,
    generation=FamilyGeneration.SENIOR_GENERATION,
    family_role=FamilyRole.CHACHI,
    parent_ids=[DADA_ID, DADI_ID],
    spouse_id=CHACHA_ID,
    education="Marketing and Communications",
    interests=[
        "Branding",
        "Marketing",
        "Media",
        "Business",
    ],
    skills=[
        "Marketing",
        "Brand Strategy",
        "Communications",
        "Customer Relations",
    ],
    business_interests=[
        BusinessDivision.MARKETING,
        BusinessDivision.ADVERTISING,
        BusinessDivision.MEDIA,
    ],
    executive_role=BusinessExecutiveRole.CMO,
)


# =========================================================
# 👦👧 YOUNG GENERATION — ALL ADULTS
# =========================================================

YOUNG_GENERATION = [
    MuktiMahalFamilyMember(
        character_id="aarav_pratap",
        name="Aarav Pratap",
        age=26,
        gender=CharacterGender.MALE,
        generation=FamilyGeneration.YOUNG_GENERATION,
        family_role=FamilyRole.SON,
        parent_ids=[PAPA_ID, MAA_ID],
        education="Technology and Business",
        interests=["AI", "Technology", "Entrepreneurship"],
        skills=[
            "Technology",
            "Product Thinking",
            "Problem Solving",
        ],
        business_interests=[
            BusinessDivision.AI,
            BusinessDivision.TECHNOLOGY,
            BusinessDivision.SOFTWARE,
        ],
        executive_role=BusinessExecutiveRole.BOARD_MEMBER,
        board_member=True,
        learning_status="BUSINESS_TRAINING",
    ),

    MuktiMahalFamilyMember(
        character_id="ananya_pratap",
        name="Ananya Pratap",
        age=25,
        gender=CharacterGender.FEMALE,
        generation=FamilyGeneration.YOUNG_GENERATION,
        family_role=FamilyRole.DAUGHTER,
        parent_ids=[PAPA_ID, MAA_ID],
        education="Media and Business",
        interests=[
            "Media",
            "Creative Production",
            "Marketing",
        ],
        skills=[
            "Creative Direction",
            "Communication",
            "Content Strategy",
        ],
        business_interests=[
            BusinessDivision.MEDIA,
            BusinessDivision.ENTERTAINMENT,
            BusinessDivision.MARKETING,
        ],
        executive_role=BusinessExecutiveRole.BOARD_MEMBER,
        board_member=True,
        learning_status="BUSINESS_TRAINING",
    ),

    MuktiMahalFamilyMember(
        character_id="vivaan_pratap",
        name="Vivaan Pratap",
        age=24,
        gender=CharacterGender.MALE,
        generation=FamilyGeneration.YOUNG_GENERATION,
        family_role=FamilyRole.SON,
        parent_ids=[BADE_PAPA_ID, BADI_MAA_ID],
        education="Finance and Economics",
        interests=[
            "Finance",
            "Investments",
            "Business Analysis",
        ],
        skills=[
            "Financial Analysis",
            "Research",
            "Data Analysis",
        ],
        business_interests=[
            BusinessDivision.INVESTMENTS,
            BusinessDivision.FINANCIAL_SERVICES,
        ],
        executive_role=BusinessExecutiveRole.BOARD_MEMBER,
        board_member=True,
        learning_status="BUSINESS_TRAINING",
    ),

    MuktiMahalFamilyMember(
        character_id="aadhya_pratap",
        name="Aadhya Pratap",
        age=24,
        gender=CharacterGender.FEMALE,
        generation=FamilyGeneration.YOUNG_GENERATION,
        family_role=FamilyRole.DAUGHTER,
        parent_ids=[BADE_PAPA_ID, BADI_MAA_ID],
        education="Hospitality and Business",
        interests=[
            "Hotels",
            "Hospitality",
            "Travel",
        ],
        skills=[
            "Hospitality",
            "Customer Experience",
            "Management",
        ],
        business_interests=[
            BusinessDivision.HOTELS,
            BusinessDivision.HOSPITALITY,
            BusinessDivision.RESTAURANTS,
        ],
        executive_role=BusinessExecutiveRole.BOARD_MEMBER,
        board_member=True,
        learning_status="BUSINESS_TRAINING",
    ),

    MuktiMahalFamilyMember(
        character_id="kabir_pratap",
        name="Kabir Pratap",
        age=23,
        gender=CharacterGender.MALE,
        generation=FamilyGeneration.YOUNG_GENERATION,
        family_role=FamilyRole.SON,
        parent_ids=[CHACHA_ID, CHACHI_ID],
        education="Engineering and Operations",
        interests=[
            "Engineering",
            "Manufacturing",
            "Automobile",
        ],
        skills=[
            "Engineering",
            "Operations",
            "Process Design",
        ],
        business_interests=[
            BusinessDivision.MANUFACTURING,
            BusinessDivision.AUTOMOBILE,
        ],
        executive_role=BusinessExecutiveRole.BOARD_MEMBER,
        board_member=True,
        learning_status="BUSINESS_TRAINING",
    ),

    MuktiMahalFamilyMember(
        character_id="kiara_pratap",
        name="Kiara Pratap",
        age=22,
        gender=CharacterGender.FEMALE,
        generation=FamilyGeneration.YOUNG_GENERATION,
        family_role=FamilyRole.DAUGHTER,
        parent_ids=[CHACHA_ID, CHACHI_ID],
        education="Digital Business and Marketing",
        interests=[
            "Digital",
            "Marketing",
            "E-commerce",
        ],
        skills=[
            "Digital Marketing",
            "Branding",
            "E-commerce",
        ],
        business_interests=[
            BusinessDivision.DIGITAL,
            BusinessDivision.ECOMMERCE,
            BusinessDivision.ADVERTISING,
        ],
        executive_role=BusinessExecutiveRole.BOARD_MEMBER,
        board_member=True,
        learning_status="BUSINESS_TRAINING",
    ),

    MuktiMahalFamilyMember(
        character_id="rohan_pratap",
        name="Rohan Pratap",
        age=21,
        gender=CharacterGender.MALE,
        generation=FamilyGeneration.YOUNG_GENERATION,
        family_role=FamilyRole.SON,
        parent_ids=[PAPA_ID, MAA_ID],
        education="Business and Real Estate",
        interests=[
            "Real Estate",
            "Construction",
            "Architecture",
        ],
        skills=[
            "Market Research",
            "Project Planning",
            "Business Development",
        ],
        business_interests=[
            BusinessDivision.REAL_ESTATE,
            BusinessDivision.CONSTRUCTION,
        ],
        executive_role=BusinessExecutiveRole.BOARD_MEMBER,
        board_member=True,
        learning_status="BUSINESS_TRAINING",
    ),

    MuktiMahalFamilyMember(
        character_id="ishita_pratap",
        name="Ishita Pratap",
        age=20,
        gender=CharacterGender.FEMALE,
        generation=FamilyGeneration.YOUNG_GENERATION,
        family_role=FamilyRole.DAUGHTER,
        parent_ids=[BADE_PAPA_ID, BADI_MAA_ID],
        education="Education and Healthcare Management",
        interests=[
            "Education",
            "Healthcare",
            "Social Development",
        ],
        skills=[
            "Research",
            "Communication",
            "Project Coordination",
        ],
        business_interests=[
            BusinessDivision.EDUCATION,
            BusinessDivision.HEALTHCARE,
        ],
        executive_role=BusinessExecutiveRole.BOARD_MEMBER,
        board_member=True,
        learning_status="BUSINESS_TRAINING",
    ),
]


# =========================================================
# 🏢 PRATAP GROUP
# =========================================================

PRATAP_GROUP = PratapGroup(
    group_id=PRATAP_GROUP_ID,
    name="PRATAP GROUP",
    headquarters_country="INDIA",
    headquarters_state="MADHYA PRADESH",
    international_operations=True,
    business_divisions=[
        BusinessDivision.REAL_ESTATE,
        BusinessDivision.CONSTRUCTION,
        BusinessDivision.HOTELS,
        BusinessDivision.HOSPITALITY,
        BusinessDivision.RESTAURANTS,
        BusinessDivision.FOOD,
        BusinessDivision.TECHNOLOGY,
        BusinessDivision.SOFTWARE,
        BusinessDivision.AI,
        BusinessDivision.DIGITAL,
        BusinessDivision.MEDIA,
        BusinessDivision.ENTERTAINMENT,
        BusinessDivision.PRODUCTION,
        BusinessDivision.MARKETING,
        BusinessDivision.ADVERTISING,
        BusinessDivision.RETAIL,
        BusinessDivision.ECOMMERCE,
        BusinessDivision.AUTOMOBILE,
        BusinessDivision.TRANSPORTATION,
        BusinessDivision.LOGISTICS,
        BusinessDivision.MANUFACTURING,
        BusinessDivision.AGRICULTURE,
        BusinessDivision.FOOD_PROCESSING,
        BusinessDivision.INVESTMENTS,
        BusinessDivision.FINANCIAL_SERVICES,
        BusinessDivision.HEALTHCARE,
        BusinessDivision.EDUCATION,
        BusinessDivision.INTERNATIONAL_TRADE,
        BusinessDivision.BUSINESS_SERVICES,
    ],
)


# =========================================================
# 👥 CORE HOUSEHOLD STAFF
# =========================================================

CORE_STAFF = [
    MuktiMahalStaffMember(
        staff_id="estate_manager_01",
        name="Mohan Sharma",
        age=45,
        gender=CharacterGender.MALE,
        staff_type=StaffType.ESTATE_MANAGER,
        department="Estate Management",
        residence_area="Staff Quarters",
        responsibilities=[
            "Estate coordination",
            "Household operations",
            "Staff coordination",
        ],
    ),

    MuktiMahalStaffMember(
        staff_id="personal_assistant_01",
        name="Priya Verma",
        age=32,
        gender=CharacterGender.FEMALE,
        staff_type=StaffType.PERSONAL_ASSISTANT,
        department="Executive Support",
        residence_area="Staff Quarters",
        responsibilities=[
            "Scheduling",
            "Executive coordination",
            "Family support",
        ],
    ),

    MuktiMahalStaffMember(
        staff_id="business_manager_01",
        name="Rahul Mehta",
        age=38,
        gender=CharacterGender.MALE,
        staff_type=StaffType.BUSINESS_MANAGER,
        department="Business Management",
        residence_area="Staff Quarters",
        responsibilities=[
            "Business coordination",
            "Reporting",
            "Operations support",
        ],
    ),

    MuktiMahalStaffMember(
        staff_id="head_chef_01",
        name="Sanjay Khan",
        age=44,
        gender=CharacterGender.MALE,
        staff_type=StaffType.CHEF,
        department="Kitchen",
        residence_area="Staff Quarters",
        responsibilities=[
            "Family meals",
            "Kitchen management",
            "Menu planning",
        ],
    ),

    MuktiMahalStaffMember(
        staff_id="housekeeping_01",
        name="Meena Joshi",
        age=41,
        gender=CharacterGender.FEMALE,
        staff_type=StaffType.HOUSEKEEPING,
        department="Housekeeping",
        residence_area="Staff Quarters",
        responsibilities=[
            "Housekeeping",
            "Room preparation",
            "Household support",
        ],
    ),

    MuktiMahalStaffMember(
        staff_id="garden_01",
        name="Ramesh Patel",
        age=46,
        gender=CharacterGender.MALE,
        staff_type=StaffType.GARDEN,
        department="Garden & Landscaping",
        residence_area="Staff Quarters",
        responsibilities=[
            "Garden maintenance",
            "Landscaping",
            "Poolside greenery",
        ],
    ),

    MuktiMahalStaffMember(
        staff_id="driver_01",
        name="Devendra Singh",
        age=43,
        gender=CharacterGender.MALE,
        staff_type=StaffType.DRIVER,
        department="Transport",
        residence_area="Driver Quarters",
        responsibilities=[
            "Family transportation",
            "Vehicle coordination",
            "Travel support",
        ],
    ),

    MuktiMahalStaffMember(
        staff_id="security_01",
        name="Arjun Yadav",
        age=39,
        gender=CharacterGender.MALE,
        staff_type=StaffType.SECURITY,
        department="Security",
        residence_area="Staff Quarters",
        responsibilities=[
            "Estate security",
            "Gate coordination",
            "Security monitoring",
        ],
    ),
]


# =========================================================
# 🏠 ESTATE AREAS
# =========================================================

ESTATE_AREAS = [
    MuktiMahalEstateArea(
        area_id="basement_garage",
        name="Underground Garage",
        area_type=EstateAreaType.GARAGE,
        floor=-1,
        capacity=20,
    ),

    MuktiMahalEstateArea(
        area_id="basement_storage",
        name="Secure Storage",
        area_type=EstateAreaType.STORAGE,
        floor=-1,
        capacity=20,
        private=True,
    ),

    MuktiMahalEstateArea(
        area_id="basement_maintenance",
        name="Maintenance Workshop",
        area_type=EstateAreaType.MAINTENANCE_AREA,
        floor=-1,
        capacity=15,
    ),

    MuktiMahalEstateArea(
        area_id="grand_entrance",
        name="Grand Entrance",
        area_type=EstateAreaType.MAIN_MANSION,
        floor=0,
        capacity=50,
    ),

    MuktiMahalEstateArea(
        area_id="family_lounge",
        name="Main Family Lounge",
        area_type=EstateAreaType.FAMILY_LOUNGE,
        floor=0,
        capacity=25,
    ),

    MuktiMahalEstateArea(
        area_id="grand_dining",
        name="Grand Dining Hall",
        area_type=EstateAreaType.DINING_HALL,
        floor=0,
        capacity=30,
    ),

    MuktiMahalEstateArea(
        area_id="main_kitchen",
        name="Main Kitchen",
        area_type=EstateAreaType.KITCHEN,
        floor=0,
        capacity=15,
    ),

    MuktiMahalEstateArea(
        area_id="family_temple",
        name="Family Temple",
        area_type=EstateAreaType.TEMPLE,
        floor=0,
        capacity=20,
        private=True,
    ),

    MuktiMahalEstateArea(
        area_id="library",
        name="Family Library",
        area_type=EstateAreaType.LIBRARY,
        floor=0,
        capacity=15,
    ),

    MuktiMahalEstateArea(
        area_id="cinema_room",
        name="Private Cinema",
        area_type=EstateAreaType.CINEMA,
        floor=0,
        capacity=25,
    ),

    MuktiMahalEstateArea(
        area_id="dada_dadi_suite",
        name="Dada Dadi Suite",
        area_type=EstateAreaType.BEDROOM,
        floor=1,
        private=True,
    ),

    MuktiMahalEstateArea(
        area_id="papa_maa_suite",
        name="Papa Maa Suite",
        area_type=EstateAreaType.BEDROOM,
        floor=1,
        private=True,
    ),

    MuktiMahalEstateArea(
        area_id="bade_papa_badi_maa_suite",
        name="Bade Papa Badi Maa Suite",
        area_type=EstateAreaType.BEDROOM,
        floor=1,
        private=True,
    ),

    MuktiMahalEstateArea(
        area_id="chacha_chachi_suite",
        name="Chacha Chachi Suite",
        area_type=EstateAreaType.BEDROOM,
        floor=2,
        private=True,
    ),

    MuktiMahalEstateArea(
        area_id="young_generation_rooms",
        name="Young Generation Rooms",
        area_type=EstateAreaType.BEDROOM,
        floor=2,
        capacity=8,
        private=True,
    ),

    MuktiMahalEstateArea(
        area_id="gym",
        name="Family Gym",
        area_type=EstateAreaType.GYM,
        floor=3,
        capacity=15,
    ),

    MuktiMahalEstateArea(
        area_id="gaming_room",
        name="Gaming Room",
        area_type=EstateAreaType.GAMING_ROOM,
        floor=3,
        capacity=12,
    ),

    MuktiMahalEstateArea(
        area_id="music_room",
        name="Music Room",
        area_type=EstateAreaType.MUSIC_ROOM,
        floor=3,
        capacity=10,
    ),

    MuktiMahalEstateArea(
        area_id="creator_studio",
        name="Creator Studio",
        area_type=EstateAreaType.CREATOR_STUDIO,
        floor=3,
        capacity=10,
    ),

    MuktiMahalEstateArea(
        area_id="chairman_office",
        name="Chairman Office",
        area_type=EstateAreaType.OFFICE,
        floor=4,
        capacity=8,
        private=True,
    ),

    MuktiMahalEstateArea(
        area_id="executive_office",
        name="Executive Office",
        area_type=EstateAreaType.OFFICE,
        floor=4,
        capacity=20,
    ),

    MuktiMahalEstateArea(
        area_id="board_room",
        name="Board Room",
        area_type=EstateAreaType.CONFERENCE_ROOM,
        floor=4,
        capacity=20,
    ),

    MuktiMahalEstateArea(
        area_id="business_studio",
        name="Business Media Studio",
        area_type=EstateAreaType.CREATOR_STUDIO,
        floor=4,
        capacity=15,
    ),

    MuktiMahalEstateArea(
        area_id="rooftop_lounge",
        name="Rooftop Family Lounge",
        area_type=EstateAreaType.TERRACE,
        floor=5,
        capacity=30,
    ),

    MuktiMahalEstateArea(
        area_id="rooftop_garden",
        name="Rooftop Garden",
        area_type=EstateAreaType.ROOFTOP_GARDEN,
        floor=5,
        capacity=30,
    ),

    MuktiMahalEstateArea(
        area_id="event_terrace",
        name="Grand Event Terrace",
        area_type=EstateAreaType.EVENT_LAWN,
        floor=5,
        capacity=50,
    ),

    MuktiMahalEstateArea(
        area_id="main_garden",
        name="Main Family Garden",
        area_type=EstateAreaType.GARDEN,
        capacity=100,
    ),

    MuktiMahalEstateArea(
        area_id="swimming_pool",
        name="Main Swimming Pool",
        area_type=EstateAreaType.POOL,
        capacity=30,
    ),

    MuktiMahalEstateArea(
        area_id="estate_temple",
        name="Estate Temple",
        area_type=EstateAreaType.TEMPLE,
        capacity=30,
    ),

    MuktiMahalEstateArea(
        area_id="staff_quarters",
        name="Staff Quarters",
        area_type=EstateAreaType.STAFF_QUARTERS,
        capacity=50,
    ),

    MuktiMahalEstateArea(
        area_id="driver_quarters",
        name="Driver Quarters",
        area_type=EstateAreaType.DRIVER_QUARTERS,
        capacity=20,
    ),

    MuktiMahalEstateArea(
        area_id="security_control",
        name="Security Control Room",
        area_type=EstateAreaType.SECURITY_ROOM,
        capacity=8,
        private=True,
    ),
]


# =========================================================
# 📦 COLLECTIONS
# =========================================================

FAMILY_MEMBERS = [
    DADA,
    DADI,
    PAPA,
    MAA,
    BADE_PAPA,
    BADI_MAA,
    CHACHA,
    CHACHI,
    *YOUNG_GENERATION,
]


# =========================================================
# 📊 SEED SUMMARY
# =========================================================

def seed_summary() -> dict:
    """Return a safe summary of the fictional seed dataset."""

    return {
        "mahal": MUKTI_MAHAL.name,
        "location": (
            f"{MUKTI_MAHAL.state}, "
            f"{MUKTI_MAHAL.country}"
        ),
        "area_acres": MUKTI_MAHAL.area_acres,
        "basements": MUKTI_MAHAL.basement_count,
        "floors": MUKTI_MAHAL.floor_count,
        "family_members": len(FAMILY_MEMBERS),
        "staff_members": len(CORE_STAFF),
        "estate_areas": len(ESTATE_AREAS),
        "business_group": PRATAP_GROUP.name,
        "business_divisions": len(
            PRATAP_GROUP.business_divisions
        ),
        "young_generation_board_members": len(
            [
                member
                for member in FAMILY_MEMBERS
                if (
                    member.generation
                    == FamilyGeneration.YOUNG_GENERATION
                    and member.board_member
                )
            ]
        ),
    }


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
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
]
