"""MAIN BASE FOUNDATION organization unit manager."""

from typing import Dict

from .units import OrganizationUnit


class OrganizationUnitManager:
    """Manage organizational units and facilities."""

    def __init__(self):
        self.units: Dict[str, OrganizationUnit] = {}

    def create(
        self,
        unit_id: str,
        organization_id: str,
        unit_name: str,
        unit_type: str,
        country: str,
        region: str,
        parent_unit_id: str | None = None,
        description: str | None = None,
    ) -> dict:
        """Create an organizational unit."""

        if unit_id in self.units:
            return {
                "success": False,
                "error": "UNIT_ID_ALREADY_EXISTS",
                "unit_id": unit_id,
            }

        if parent_unit_id:
            if parent_unit_id not in self.units:
                return {
                    "success": False,
                    "error": "PARENT_UNIT_NOT_FOUND",
                    "parent_unit_id": parent_unit_id,
                }

        unit = OrganizationUnit(
            unit_id=unit_id,
            organization_id=organization_id,
            parent_unit_id=parent_unit_id,
            unit_name=unit_name,
            unit_type=unit_type,
            country=country,
            region=region,
            description=description,
        )

        self.units[unit_id] = unit

        return {
            "success": True,
            "unit": unit.__dict__,
        }

    def get(
        self,
        unit_id: str,
    ) -> dict:
        """Return one organizational unit."""

        unit = self.units.get(unit_id)

        if unit is None:
            return {
                "success": False,
                "error": "UNIT_NOT_FOUND",
                "unit_id": unit_id,
            }

        return {
            "success": True,
            "unit": unit.__dict__,
        }

    def list(
        self,
        organization_id: str | None = None,
    ) -> dict:
        """Return organizational units."""

        units = list(self.units.values())

        if organization_id:
            units = [
                unit
                for unit in units
                if unit.organization_id == organization_id
            ]

        return {
            "success": True,
            "count": len(units),
            "units": [
                unit.__dict__
                for unit in units
            ],
        }

    def children(
        self,
        parent_unit_id: str,
    ) -> dict:
        """Return direct child units."""

        children = [
            unit
            for unit in self.units.values()
            if unit.parent_unit_id == parent_unit_id
        ]

        return {
            "success": True,
            "count": len(children),
            "units": [
                unit.__dict__
                for unit in children
            ],
        }

    def disable(
        self,
        unit_id: str,
    ) -> dict:
        """Disable an organizational unit."""

        unit = self.units.get(unit_id)

        if unit is None:
            return {
                "success": False,
                "error": "UNIT_NOT_FOUND",
            }

        unit.enabled = False
        unit.status = "DISABLED"

        return {
            "success": True,
            "unit": unit.__dict__,
        }

    def health(self) -> dict:
        """Return organization unit health."""

        active = sum(
            1
            for unit in self.units.values()
            if unit.status == "ACTIVE"
        )

        return {
            "system": "Organization Unit Manager",
            "health": "HEALTHY",
            "registered_units": len(self.units),
            "active_units": active,
        }
