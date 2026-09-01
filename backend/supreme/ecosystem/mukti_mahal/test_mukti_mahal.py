"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Tests

Tests for:

- Models
- Service
- Controller
- Seed data
- Bootstrap
- Family
- Staff
- Estate
- Pratap Group
- Capability evaluation
- Family visit workflow
"""

from __future__ import annotations

import unittest

from .bootstrap import (
    bootstrap_mukti_mahal,
    bootstrap_summary,
)

from .controller import (
    MuktiMahalController,
)

from .model import (
    BusinessExecutiveRole,
    FamilyGeneration,
)

from .seed import (
    MUKTI_MAHAL_ID,
    PRATAP_GROUP_ID,
)


class TestMuktiMahal(unittest.TestCase):
    """Test the complete Mukti Mahal foundation."""

    # =====================================================
    # 🚀 BOOTSTRAP
    # =====================================================

    def setUp(self) -> None:
        self.service = (
            bootstrap_mukti_mahal()
        )

        self.controller = (
            MuktiMahalController(
                service=self.service
            )
        )

    # =====================================================
    # 🏰 MAHAL
    # =====================================================

    def test_mahal_exists(self) -> None:

        mahal = self.service.get_mahal(
            MUKTI_MAHAL_ID
        )

        self.assertIsNotNone(
            mahal
        )

        self.assertEqual(
            mahal.name,
            "MUKTI MAHAL",
        )

        self.assertEqual(
            mahal.country,
            "INDIA",
        )

        self.assertEqual(
            mahal.state,
            "MADHYA PRADESH",
        )

    # =====================================================
    # 🏢 BUSINESS GROUP
    # =====================================================

    def test_pratap_group_exists(self) -> None:

        group = self.service.get_group(
            PRATAP_GROUP_ID
        )

        self.assertIsNotNone(
            group
        )

        self.assertEqual(
            group.name,
            "PRATAP GROUP",
        )

        self.assertTrue(
            group.international_operations
        )

    # =====================================================
    # 👨‍👩‍👧 FAMILY
    # =====================================================

    def test_family_loaded(self) -> None:

        family = (
            self.service.list_family_members()
        )

        self.assertGreaterEqual(
            len(family),
            1,
        )

    def test_founders_loaded(self) -> None:

        founders = (
            self.service.list_family_members(
                generation=FamilyGeneration.FOUNDERS
            )
        )

        self.assertEqual(
            len(founders),
            2,
        )

    def test_young_generation_loaded(self) -> None:

        young_members = (
            self.service.list_family_members(
                generation=(
                    FamilyGeneration.YOUNG_GENERATION
                )
            )
        )

        self.assertGreaterEqual(
            len(young_members),
            1,
        )

        for member in young_members:
            self.assertGreaterEqual(
                member.age,
                20,
            )

    # =====================================================
    # 👥 STAFF
    # =====================================================

    def test_staff_loaded(self) -> None:

        staff = (
            self.service.list_staff()
        )

        self.assertGreaterEqual(
            len(staff),
            1,
        )

    # =====================================================
    # 🏠 ESTATE
    # =====================================================

    def test_estate_areas_loaded(self) -> None:

        areas = (
            self.service.list_estate_areas()
        )

        self.assertGreaterEqual(
            len(areas),
            1,
        )

    # =====================================================
    # 🎓 BOARD LEARNING
    # =====================================================

    def test_young_generation_board_members(
        self,
    ) -> None:

        young_members = (
            self.service.list_family_members(
                generation=(
                    FamilyGeneration.YOUNG_GENERATION
                )
            )
        )

        board_members = [
            member
            for member in young_members
            if member.board_member
        ]

        self.assertGreaterEqual(
            len(board_members),
            1,
        )

        for member in board_members:

            self.assertEqual(
                member.executive_role,
                BusinessExecutiveRole.BOARD_MEMBER,
            )

    # =====================================================
    # 🎛️ CONTROLLER
    # =====================================================

    def test_controller_status(self) -> None:

        status = (
            self.controller.status()
        )

        self.assertEqual(
            status["controller"],
            "SUPREME_MUKTI_MAHAL",
        )

        self.assertIn(
            "service",
            status,
        )

    # =====================================================
    # 📊 BOOTSTRAP SUMMARY
    # =====================================================

    def test_bootstrap_summary(self) -> None:

        summary = (
            bootstrap_summary(
                self.service
            )
        )

        self.assertTrue(
            summary["bootstrapped"]
        )

        self.assertGreaterEqual(
            summary["family_members"],
            1,
        )

        self.assertGreaterEqual(
            summary["staff_members"],
            1,
        )

        self.assertGreaterEqual(
            summary["estate_areas"],
            1,
        )

        self.assertGreaterEqual(
            summary["business_groups"],
            1,
        )


# =========================================================
# ▶️ DIRECT TEST EXECUTION
# =========================================================

if __name__ == "__main__":
    unittest.main()
