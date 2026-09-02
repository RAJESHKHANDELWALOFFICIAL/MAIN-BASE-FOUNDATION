"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Tests

Comprehensive foundation tests for:

- Models
- Service
- Controller
- Seed data
- Bootstrap
- Family
- Staff
- Estate
- Pratap Group
- Business divisions
- Capability evaluation
- Executive governance
- Family visit workflow
- Mukti principles
- Runtime status
- Error handling
- Bootstrap idempotency
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
    BusinessCapabilityEvaluation,
    BusinessDivision,
    BusinessExecutiveRole,
    EstateAreaType,
    FamilyGeneration,
    FamilyRole,
    MuktiMahalFamilyVisit,
    StaffType,
)

from .seed import (
    DADA_ID,
    MUKTI_MAHAL_ID,
    PRATAP_GROUP_ID,
)


class TestMuktiMahal(unittest.TestCase):
    """Test the complete Mukti Mahal foundation."""

    # =========================================================
    # 🚀 BOOTSTRAP
    # =========================================================

    def setUp(self) -> None:
        self.service = bootstrap_mukti_mahal()

        self.controller = MuktiMahalController(
            service=self.service
        )

    # =========================================================
    # 🚀 INITIALIZATION
    # =========================================================

    def test_service_is_initialized(self) -> None:
        status = self.service.status()

        self.assertTrue(
            status["initialized"]
        )

        self.assertEqual(
            status["service"],
            "MUKTI_MAHAL",
        )

    # =========================================================
    # 🏰 MAHAL
    # =========================================================

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

        self.assertTrue(
            mahal.active
        )

    def test_mahal_is_linked_to_pratap_group(self) -> None:
        mahal = self.service.get_mahal(
            MUKTI_MAHAL_ID
        )

        self.assertIsNotNone(
            mahal
        )

        self.assertEqual(
            mahal.group_id,
            PRATAP_GROUP_ID,
        )

    def test_mahal_has_seeded_relationships(self) -> None:
        mahal = self.service.get_mahal(
            MUKTI_MAHAL_ID
        )

        self.assertIsNotNone(
            mahal
        )

        self.assertGreater(
            len(mahal.family_member_ids),
            0,
        )

        self.assertGreater(
            len(mahal.staff_member_ids),
            0,
        )

        self.assertGreater(
            len(mahal.estate_area_ids),
            0,
        )

    # =========================================================
    # 🏢 PRATAP GROUP
    # =========================================================

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

        self.assertEqual(
            group.headquarters_country,
            "INDIA",
        )

        self.assertEqual(
            group.headquarters_state,
            "MADHYA PRADESH",
        )

        self.assertTrue(
            group.international_operations
        )

    def test_pratap_group_has_business_divisions(self) -> None:
        group = self.service.get_group(
            PRATAP_GROUP_ID
        )

        self.assertIsNotNone(
            group
        )

        self.assertGreater(
            len(group.business_divisions),
            0,
        )

        self.assertIn(
            BusinessDivision.REAL_ESTATE,
            group.business_divisions,
        )

        self.assertIn(
            BusinessDivision.TECHNOLOGY,
            group.business_divisions,
        )

        self.assertIn(
            BusinessDivision.AI,
            group.business_divisions,
        )

        self.assertIn(
            BusinessDivision.BUSINESS_SERVICES,
            group.business_divisions,
        )

    # =========================================================
    # 👨‍👩‍👧 FAMILY
    # =========================================================

    def test_family_loaded(self) -> None:
        family = (
            self.service.list_family_members()
        )

        self.assertGreater(
            len(family),
            0,
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

    def test_senior_generation_loaded(self) -> None:
        senior_members = (
            self.service.list_family_members(
                generation=FamilyGeneration.SENIOR_GENERATION
            )
        )

        self.assertGreater(
            len(senior_members),
            0,
        )

    def test_young_generation_loaded(self) -> None:
        young_members = (
            self.service.list_family_members(
                generation=FamilyGeneration.YOUNG_GENERATION
            )
        )

        self.assertGreater(
            len(young_members),
            0,
        )

        for member in young_members:
            self.assertGreaterEqual(
                member.age,
                20,
            )

    def test_young_generation_are_active(self) -> None:
        young_members = (
            self.service.list_family_members(
                generation=FamilyGeneration.YOUNG_GENERATION
            )
        )

        for member in young_members:
            self.assertTrue(
                member.active
            )

    def test_founders_are_founder_roles(self) -> None:
        founders = (
            self.service.list_family_members(
                generation=FamilyGeneration.FOUNDERS
            )
        )

        roles = {
            member.executive_role
            for member in founders
        }

        self.assertIn(
            BusinessExecutiveRole.FOUNDER,
            roles,
        )

        self.assertIn(
            BusinessExecutiveRole.CO_FOUNDER,
            roles,
        )

    def test_family_role_filter(self) -> None:
        dada_members = (
            self.service.list_family_members(
                family_role=FamilyRole.DADA
            )
        )

        self.assertEqual(
            len(dada_members),
            1,
        )

        self.assertEqual(
            dada_members[0].character_id,
            DADA_ID,
        )

    def test_family_member_lookup(self) -> None:
        dada = self.service.get_family_member(
            DADA_ID
        )

        self.assertIsNotNone(
            dada
        )

        self.assertEqual(
            dada.character_id,
            DADA_ID,
        )

    def test_unknown_family_member_returns_none(self) -> None:
        member = self.service.get_family_member(
            "unknown_character"
        )

        self.assertIsNone(
            member
        )

    # =========================================================
    # 👥 STAFF
    # =========================================================

    def test_staff_loaded(self) -> None:
        staff = (
            self.service.list_staff()
        )

        self.assertGreater(
            len(staff),
            0,
        )

    def test_staff_are_adults(self) -> None:
        staff = (
            self.service.list_staff()
        )

        for member in staff:
            self.assertGreaterEqual(
                member.age,
                18,
            )

    def test_staff_type_filter(self) -> None:
        security_staff = (
            self.service.list_staff(
                staff_type=StaffType.SECURITY
            )
        )

        self.assertGreater(
            len(security_staff),
            0,
        )

        for member in security_staff:
            self.assertEqual(
                member.staff_type,
                StaffType.SECURITY,
            )

    # =========================================================
    # 🏠 ESTATE
    # =========================================================

    def test_estate_areas_loaded(self) -> None:
        areas = (
            self.service.list_estate_areas()
        )

        self.assertGreater(
            len(areas),
            0,
        )

    def test_estate_area_lookup(self) -> None:
        area = self.service.get_estate_area(
            "grand_entrance"
        )

        self.assertIsNotNone(
            area
        )

        self.assertEqual(
            area.name,
            "Grand Entrance",
        )

    def test_estate_area_type_filter(self) -> None:
        bedrooms = (
            self.service.list_estate_areas(
                area_type=EstateAreaType.BEDROOM
            )
        )

        self.assertGreater(
            len(bedrooms),
            0,
        )

        for area in bedrooms:
            self.assertEqual(
                area.area_type,
                EstateAreaType.BEDROOM,
            )

    def test_estate_area_floor_filter(self) -> None:
        floor_four = (
            self.service.list_estate_areas(
                floor=4
            )
        )

        self.assertGreater(
            len(floor_four),
            0,
        )

        for area in floor_four:
            self.assertEqual(
                area.floor,
                4,
            )

    # =========================================================
    # 🎓 BOARD / BUSINESS LEARNING
    # =========================================================

    def test_young_generation_board_members(
        self,
    ) -> None:
        young_members = (
            self.service.list_family_members(
                generation=FamilyGeneration.YOUNG_GENERATION
            )
        )

        board_members = [
            member
            for member in young_members
            if member.board_member
        ]

        self.assertGreater(
            len(board_members),
            0,
        )

        for member in board_members:
            self.assertEqual(
                member.executive_role,
                BusinessExecutiveRole.BOARD_MEMBER,
            )

    # =========================================================
    # 🎓 CAPABILITY EVALUATION
    # =========================================================

    def test_capability_evaluation_registration(
        self,
    ) -> None:
        evaluation = BusinessCapabilityEvaluation(
            evaluation_id="test_evaluation_001",
            character_id=DADA_ID,
            evaluated_by=DADA_ID,
            business_division=BusinessDivision.BUSINESS_SERVICES,
            knowledge_score=80,
            leadership_score=85,
            execution_score=90,
            problem_solving_score=88,
            ethics_score=95,
            overall_score=88,
            passed=True,
            recommendation="Continue advanced business development.",
        )

        registered = (
            self.service.register_capability_evaluation(
                evaluation
            )
        )

        self.assertEqual(
            registered.evaluation_id,
            "test_evaluation_001",
        )

        stored = (
            self.service.get_capability_evaluation(
                "test_evaluation_001"
            )
        )

        self.assertIsNotNone(
            stored
        )

        self.assertEqual(
            stored.character_id,
            DADA_ID,
        )

    def test_capability_evaluation_filter(
        self,
    ) -> None:
        evaluation = BusinessCapabilityEvaluation(
            evaluation_id="test_evaluation_002",
            character_id=DADA_ID,
            evaluated_by=DADA_ID,
            business_division=BusinessDivision.REAL_ESTATE,
            knowledge_score=90,
            leadership_score=90,
            execution_score=90,
            problem_solving_score=90,
            ethics_score=90,
            overall_score=90,
            passed=True,
        )

        self.service.register_capability_evaluation(
            evaluation
        )

        evaluations = (
            self.service.list_capability_evaluations(
                character_id=DADA_ID
            )
        )

        self.assertEqual(
            len(evaluations),
            1,
        )

        self.assertEqual(
            evaluations[0].evaluation_id,
            "test_evaluation_002",
        )

    def test_capability_evaluation_rejects_unknown_character(
        self,
    ) -> None:
        evaluation = BusinessCapabilityEvaluation(
            evaluation_id="test_evaluation_003",
            character_id="unknown_character",
            evaluated_by=DADA_ID,
            business_division=BusinessDivision.REAL_ESTATE,
            overall_score=90,
            passed=True,
        )

        with self.assertRaises(
            ValueError
        ):
            self.service.register_capability_evaluation(
                evaluation
            )

    # =========================================================
    # 👔 EXECUTIVE GOVERNANCE
    # =========================================================

    def test_executive_role_requires_capability(
        self,
    ) -> None:
        young_members = (
            self.service.list_family_members(
                generation=FamilyGeneration.YOUNG_GENERATION
            )
        )

        member = young_members[0]

        with self.assertRaises(
            ValueError
        ):
            self.service.assign_executive_role(
                character_id=member.character_id,
                role=BusinessExecutiveRole.CEO,
            )

    # =========================================================
    # 🤝 FAMILY VISIT WORKFLOW
    # =========================================================

    def test_family_visit_workflow(
        self,
    ) -> None:
        visit = MuktiMahalFamilyVisit(
            visit_id="test_visit_001",
            host_mahal_id=MUKTI_MAHAL_ID,
            visiting_family_name="TEST FAMILY",
            visiting_grandfather_name="Test Grandfather",
            visiting_grandmother_name="Test Grandmother",
            visiting_son_name="Test Son",
            visiting_daughter_in_law_name="Test Daughter-in-Law",
            visiting_grandchildren=[
                "Test Grandchild 1",
                "Test Grandchild 2",
            ],
            duration_days=1,
        )

        registered = (
            self.service.register_family_visit(
                visit
            )
        )

        self.assertFalse(
            registered.completed
        )

        self.assertFalse(
            registered.welcome_completed
        )

        # Welcome
        self.service.complete_welcome(
            "test_visit_001"
        )

        stored = (
            self.service.get_family_visit(
                "test_visit_001"
            )
        )

        self.assertTrue(
            stored.welcome_completed
        )

        # Introductions
        self.service.complete_introductions(
            "test_visit_001"
        )

        self.assertTrue(
            stored.introductions_completed
        )

        # Dinner
        self.service.complete_dinner(
            "test_visit_001"
        )

        self.assertTrue(
            stored.dinner_completed
        )

        # Business discussion / completion
        self.service.complete_business_discussion(
            "test_visit_001"
        )

        self.assertTrue(
            stored.business_discussion_completed
        )

        self.assertTrue(
            stored.completed
        )

    def test_family_visit_requires_correct_sequence(
        self,
    ) -> None:
        visit = MuktiMahalFamilyVisit(
            visit_id="test_visit_002",
            host_mahal_id=MUKTI_MAHAL_ID,
            visiting_family_name="SEQUENCE TEST FAMILY",
            visiting_grandfather_name="Grandfather",
            visiting_grandmother_name="Grandmother",
            visiting_son_name="Son",
            visiting_daughter_in_law_name="Daughter-in-Law",
        )

        self.service.register_family_visit(
            visit
        )

        with self.assertRaises(
            ValueError
        ):
            self.service.complete_introductions(
                "test_visit_002"
            )

        self.service.complete_welcome(
            "test_visit_002"
        )

        self.service.complete_introductions(
            "test_visit_002"
        )

        with self.assertRaises(
            ValueError
        ):
            self.service.complete_business_discussion(
                "test_visit_002"
            )

    # =========================================================
    # 📜 MUKTI PRINCIPLES
    # =========================================================

    def test_mukti_principles(self) -> None:
        principles = (
            self.service.principles()
        )

        self.assertTrue(
            principles.respect_required
        )

        self.assertTrue(
            principles.consent_required
        )

        self.assertTrue(
            principles.privacy_respected
        )

        self.assertTrue(
            principles.personal_choice_respected
        )

        self.assertTrue(
            principles.family_responsibility_required
        )

        self.assertTrue(
            principles.business_capability_required
        )

        self.assertTrue(
            principles.applicable_law_required
        )

        self.assertTrue(
            principles.safety_required
        )

    # =========================================================
    # 🎛️ CONTROLLER
    # =========================================================

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

        self.assertTrue(
            status["service"]["initialized"]
        )

    def test_controller_can_get_mahal(self) -> None:
        mahal = (
            self.controller.get_mahal(
                MUKTI_MAHAL_ID
            )
        )

        self.assertIsNotNone(
            mahal
        )

        self.assertEqual(
            mahal.name,
            "MUKTI MAHAL",
        )

    def test_controller_can_get_family_member(
        self,
    ) -> None:
        member = (
            self.controller.get_family_member(
                DADA_ID
            )
        )

        self.assertIsNotNone(
            member
        )

        self.assertEqual(
            member.character_id,
            DADA_ID,
        )

    def test_controller_can_list_staff(
        self,
    ) -> None:
        staff = (
            self.controller.list_staff()
        )

        self.assertGreater(
            len(staff),
            0,
        )

    def test_controller_can_list_estate_areas(
        self,
    ) -> None:
        areas = (
            self.controller.list_estate_areas()
        )

        self.assertGreater(
            len(areas),
            0,
        )

    # =========================================================
    # 📊 BOOTSTRAP SUMMARY
    # =========================================================

    def test_bootstrap_summary(self) -> None:
        summary = (
            bootstrap_summary(
                self.service
            )
        )

        self.assertTrue(
            summary["bootstrapped"]
        )

        self.assertEqual(
            summary["mahal_id"],
            MUKTI_MAHAL_ID,
        )

        self.assertEqual(
            summary["mahal_name"],
            "MUKTI MAHAL",
        )

        self.assertGreater(
            summary["family_members"],
            0,
        )

        self.assertGreater(
            summary["staff_members"],
            0,
        )

        self.assertGreater(
            summary["estate_areas"],
            0,
        )

        self.assertGreater(
            summary["business_groups"],
            0,
        )

    # =========================================================
    # 🔁 BOOTSTRAP IDEMPOTENCY
    # =========================================================

    def test_bootstrap_does_not_duplicate_seed_data(
        self,
    ) -> None:
        before = self.service.status()

        bootstrap_mukti_mahal(
            service=self.service
        )

        after = self.service.status()

        self.assertEqual(
            before["mahals"],
            after["mahals"],
        )

        self.assertEqual(
            before["groups"],
            after["groups"],
        )

        self.assertEqual(
            before["family_members"],
            after["family_members"],
        )

        self.assertEqual(
            before["staff_members"],
            after["staff_members"],
        )

        self.assertEqual(
            before["estate_areas"],
            after["estate_areas"],
        )

    # =========================================================
    # 📈 STATUS CONSISTENCY
    # =========================================================

    def test_status_counts_match_loaded_data(
        self,
    ) -> None:
        status = self.service.status()

        self.assertEqual(
            status["mahals"],
            len(
                self.service.list_mahals()
            ),
        )

        self.assertEqual(
            status["groups"],
            len(
                self.service.list_groups()
            ),
        )

        self.assertEqual(
            status["family_members"],
            len(
                self.service.list_family_members()
            ),
        )

        self.assertEqual(
            status["staff_members"],
            len(
                self.service.list_staff()
            ),
        )

        self.assertEqual(
            status["estate_areas"],
            len(
                self.service.list_estate_areas()
            ),
        )

    # =========================================================
    # ❌ ERROR HANDLING
    # =========================================================

    def test_unknown_estate_area_returns_none(
        self,
    ) -> None:
        area = (
            self.service.get_estate_area(
                "unknown_area"
            )
        )

        self.assertIsNone(
            area
        )

    def test_unknown_group_returns_none(
        self,
    ) -> None:
        group = (
            self.service.get_group(
                "unknown_group"
            )
        )

        self.assertIsNone(
            group
        )

    def test_unknown_visit_raises_clear_error(
        self,
    ) -> None:
        with self.assertRaises(
            ValueError
        ):
            self.service.complete_welcome(
                "unknown_visit"
            )


# =========================================================
# ▶️ DIRECT TEST EXECUTION
# =========================================================

if __name__ == "__main__":
    unittest.main()
