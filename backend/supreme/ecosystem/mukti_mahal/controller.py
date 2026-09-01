"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Controller

Central public control entry point for:

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
- Service status

The controller delegates business rules
to MuktiMahalService.
"""

from __future__ import annotations

from typing import List, Optional

from .model import (
    BusinessCapabilityEvaluation,
    BusinessDivision,
    BusinessExecutiveRole,
    EstateAreaType,
    FamilyGeneration,
    MuktiMahal,
    MuktiMahalEstateArea,
    MuktiMahalFamilyMember,
    MuktiMahalFamilyVisit,
    MuktiMahalStaffMember,
    MuktiPrinciples,
    PratapGroup,
    StaffType,
)

from .service import (
    MuktiMahalService,
)


class MuktiMahalController:
    """Central controller for SUPREME Mukti Mahal."""

    def __init__(
        self,
        service: Optional[
            MuktiMahalService
        ] = None,
    ) -> None:

        self.service = (
            service
            if service is not None
            else MuktiMahalService()
        )

    # =========================================================
    # 🚀 INITIALIZATION
    # =========================================================

    def initialize(self) -> dict:
        """Initialize Mukti Mahal control."""

        return self.service.initialize()

    # =========================================================
    # 🏰 MAHAL
    # =========================================================

    def create_mahal(
        self,
        mahal: MuktiMahal,
    ) -> MuktiMahal:
        """Create a Mukti Mahal estate."""

        return self.service.create_mahal(
            mahal
        )

    def get_mahal(
        self,
        mahal_id: str,
    ) -> Optional[MuktiMahal]:
        """Return a Mukti Mahal estate."""

        return self.service.get_mahal(
            mahal_id
        )

    def list_mahals(
        self,
    ) -> List[MuktiMahal]:
        """Return all Mukti Mahal estates."""

        return self.service.list_mahals()

    # =========================================================
    # 👨‍👩‍👧 FAMILY
    # =========================================================

    def add_family_member(
        self,
        member: MuktiMahalFamilyMember,
        mahal_id: str,
    ) -> MuktiMahalFamilyMember:
        """Add a family member."""

        return self.service.add_family_member(
            member=member,
            mahal_id=mahal_id,
        )

    def get_family_member(
        self,
        character_id: str,
    ) -> Optional[
        MuktiMahalFamilyMember
    ]:
        """Return a family member."""

        return self.service.get_family_member(
            character_id
        )

    def list_family_members(
        self,
        generation: Optional[
            FamilyGeneration
        ] = None,
    ) -> List[
        MuktiMahalFamilyMember
    ]:
        """Return family members."""

        return self.service.list_family_members(
            generation=generation
        )

    # =========================================================
    # 👥 STAFF
    # =========================================================

    def add_staff_member(
        self,
        staff: MuktiMahalStaffMember,
        mahal_id: str,
    ) -> MuktiMahalStaffMember:
        """Add a Mukti Mahal staff member."""

        return self.service.add_staff_member(
            staff=staff,
            mahal_id=mahal_id,
        )

    def get_staff(
        self,
        staff_id: str,
    ) -> Optional[
        MuktiMahalStaffMember
    ]:
        """Return a staff member."""

        return self.service.get_staff(
            staff_id
        )

    def list_staff(
        self,
        staff_type: Optional[
            StaffType
        ] = None,
    ) -> List[
        MuktiMahalStaffMember
    ]:
        """Return staff members."""

        return self.service.list_staff(
            staff_type=staff_type
        )

    # =========================================================
    # 🏠 ESTATE AREAS
    # =========================================================

    def add_estate_area(
        self,
        area: MuktiMahalEstateArea,
        mahal_id: str,
    ) -> MuktiMahalEstateArea:
        """Add an estate area."""

        return self.service.add_estate_area(
            area=area,
            mahal_id=mahal_id,
        )

    def get_estate_area(
        self,
        area_id: str,
    ) -> Optional[
        MuktiMahalEstateArea
    ]:
        """Return an estate area."""

        return self.service.get_estate_area(
            area_id
        )

    def list_estate_areas(
        self,
        area_type: Optional[
            EstateAreaType
        ] = None,
        floor: Optional[int] = None,
    ) -> List[
        MuktiMahalEstateArea
    ]:
        """Return estate areas."""

        return self.service.list_estate_areas(
            area_type=area_type,
            floor=floor,
        )

    # =========================================================
    # 🏢 PRATAP GROUP
    # =========================================================

    def create_group(
        self,
        group: PratapGroup,
    ) -> PratapGroup:
        """Create a Pratap Group business entity."""

        return self.service.create_group(
            group
        )

    def get_group(
        self,
        group_id: str,
    ) -> Optional[PratapGroup]:
        """Return a business group."""

        return self.service.get_group(
            group_id
        )

    def list_groups(
        self,
    ) -> List[PratapGroup]:
        """Return all business groups."""

        return self.service.list_groups()

    def add_business_division(
        self,
        group_id: str,
        division: BusinessDivision,
    ) -> PratapGroup:
        """Add a business division."""

        return self.service.add_business_division(
            group_id=group_id,
            division=division,
        )

    # =========================================================
    # 👔 EXECUTIVE ROLES
    # =========================================================

    def assign_executive_role(
        self,
        character_id: str,
        role: BusinessExecutiveRole,
    ) -> MuktiMahalFamilyMember:
        """Assign a family business role."""

        return self.service.assign_executive_role(
            character_id=character_id,
            role=role,
        )

    # =========================================================
    # 🎓 CAPABILITY EVALUATION
    # =========================================================

    def register_capability_evaluation(
        self,
        evaluation: BusinessCapabilityEvaluation,
    ) -> BusinessCapabilityEvaluation:
        """Register a capability evaluation."""

        return self.service.register_capability_evaluation(
            evaluation
        )

    def get_capability_evaluation(
        self,
        evaluation_id: str,
    ) -> Optional[
        BusinessCapabilityEvaluation
    ]:
        """Return a capability evaluation."""

        return self.service.get_capability_evaluation(
            evaluation_id
        )

    def list_capability_evaluations(
        self,
        character_id: Optional[str] = None,
    ) -> List[
        BusinessCapabilityEvaluation
    ]:
        """Return capability evaluations."""

        return self.service.list_capability_evaluations(
            character_id=character_id
        )

    def qualify_executive_role(
        self,
        character_id: str,
        role: BusinessExecutiveRole,
    ) -> MuktiMahalFamilyMember:
        """
        Qualify a family member for an executive role
        after capability has been proven.
        """

        return self.service.qualify_executive_role(
            character_id=character_id,
            role=role,
        )

    # =========================================================
    # 🤝 FAMILY VISIT
    # =========================================================

    def register_family_visit(
        self,
        visit: MuktiMahalFamilyVisit,
    ) -> MuktiMahalFamilyVisit:
        """Register a one-day family visit."""

        return self.service.register_family_visit(
            visit
        )

    def complete_welcome(
        self,
        visit_id: str,
    ) -> MuktiMahalFamilyVisit:
        """Complete the welcome stage."""

        return self.service.complete_welcome(
            visit_id
        )

    def complete_introductions(
        self,
        visit_id: str,
    ) -> MuktiMahalFamilyVisit:
        """Complete family introductions."""

        return self.service.complete_introductions(
            visit_id
        )

    def complete_dinner(
        self,
        visit_id: str,
    ) -> MuktiMahalFamilyVisit:
        """Complete the family dinner."""

        return self.service.complete_dinner(
            visit_id
        )

    def complete_business_discussion(
        self,
        visit_id: str,
    ) -> MuktiMahalFamilyVisit:
        """Complete the business discussion."""

        return self.service.complete_business_discussion(
            visit_id
        )

    # =========================================================
    # 📜 PRINCIPLES
    # =========================================================

    def principles(
        self,
    ) -> MuktiPrinciples:
        """Return Mukti Mahal principles."""

        return self.service.principles()

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return controller status."""

        return {
            "controller": (
                "SUPREME_MUKTI_MAHAL"
            ),
            "service": self.service.status(),
        }


# =========================================================
# 🌍 DEFAULT CONTROLLER
# =========================================================

mukti_mahal_controller = (
    MuktiMahalController()
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "MuktiMahalController",
    "mukti_mahal_controller",
]
