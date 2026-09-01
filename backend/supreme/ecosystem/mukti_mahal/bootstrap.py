"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Bootstrap

Loads the initial fictional Mukti Mahal world into
MuktiMahalService.

Loads:

- Mukti Mahal
- Pratap Group
- Family members
- Household staff
- Estate areas

No credentials, passwords, OTPs or secrets are loaded.
"""

from __future__ import annotations

from .model import MuktiMahal
from .service import MuktiMahalService
from .seed import (
    MUKTI_MAHAL,
    PRATAP_GROUP,
    FAMILY_MEMBERS,
    CORE_STAFF,
    ESTATE_AREAS,
)


def bootstrap_mukti_mahal(
    service: MuktiMahalService | None = None,
) -> MuktiMahalService:
    """
    Load the complete initial Mukti Mahal dataset
    into a service instance.
    """

    if service is None:
        service = MuktiMahalService()

    service.initialize()

    # =====================================================
    # 🏢 PRATAP GROUP
    # =====================================================

    if service.get_group(
        PRATAP_GROUP.group_id
    ) is None:
        service.create_group(
            PRATAP_GROUP
        )

    # =====================================================
    # 🏰 MUKTI MAHAL
    # =====================================================

    if service.get_mahal(
        MUKTI_MAHAL.mahal_id
    ) is None:
        service.create_mahal(
            MUKTI_MAHAL
        )

    # =====================================================
    # 👨‍👩‍👧 FAMILY
    # =====================================================

    for member in FAMILY_MEMBERS:

        if service.get_family_member(
            member.character_id
        ) is None:

            service.add_family_member(
                member=member,
                mahal_id=MUKTI_MAHAL.mahal_id,
            )

    # =====================================================
    # 👥 STAFF
    # =====================================================

    for staff in CORE_STAFF:

        if service.get_staff(
            staff.staff_id
        ) is None:

            service.add_staff_member(
                staff=staff,
                mahal_id=MUKTI_MAHAL.mahal_id,
            )

    # =====================================================
    # 🏠 ESTATE AREAS
    # =====================================================

    for area in ESTATE_AREAS:

        if service.get_estate_area(
            area.area_id
        ) is None:

            service.add_estate_area(
                area=area,
                mahal_id=MUKTI_MAHAL.mahal_id,
            )

    return service


def create_default_mukti_mahal_service(
) -> MuktiMahalService:
    """
    Create and fully bootstrap a fresh
    Mukti Mahal service instance.
    """

    return bootstrap_mukti_mahal()


def bootstrap_summary(
    service: MuktiMahalService,
) -> dict:
    """Return a safe bootstrap summary."""

    mahal = service.get_mahal(
        MUKTI_MAHAL.mahal_id
    )

    return {
        "bootstrapped": mahal is not None,
        "mahal_id": (
            mahal.mahal_id
            if mahal is not None
            else None
        ),
        "mahal_name": (
            mahal.name
            if mahal is not None
            else None
        ),
        "family_members": len(
            service.list_family_members()
        ),
        "staff_members": len(
            service.list_staff()
        ),
        "estate_areas": len(
            service.list_estate_areas()
        ),
        "business_groups": len(
            service.list_groups()
        ),
    }


__all__ = [
    "bootstrap_mukti_mahal",
    "create_default_mukti_mahal_service",
    "bootstrap_summary",
]
