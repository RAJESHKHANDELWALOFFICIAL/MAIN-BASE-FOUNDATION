"""Supreme Ecosystem management engine."""

from datetime import datetime, timezone
from typing import Dict, List, Optional

from .models import EcosystemIdentity
from .registry import EcosystemRegistry


class EcosystemManager:
    """Central manager for the Supreme Ecosystem."""

    def __init__(self):
        self.registry = EcosystemRegistry()

        self.status = "READY"

        self.last_check = (
            datetime.now(timezone.utc).isoformat()
        )

    def list(self) -> List[dict]:
        """Return all registered ecosystems."""

        return [
            ecosystem.to_dict()
            for ecosystem in self.registry.list()
        ]

    def get(
        self,
        ecosystem_id: str,
    ) -> dict:
        """Return one ecosystem."""

        ecosystem = self.registry.get(
            ecosystem_id
        )

        return ecosystem.to_dict()

    def names(self) -> List[str]:
        """Return all registered ecosystem names."""

        return self.registry.names()

    def exists(
        self,
        ecosystem_id: str,
    ) -> bool:
        """Check whether an ecosystem exists."""

        return self.registry.exists(
            ecosystem_id
        )

    def register(
        self,
        ecosystem: EcosystemIdentity,
    ) -> dict:
        """Register a new ecosystem."""

        self.registry.register(
            ecosystem
        )

        self.last_check = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        return ecosystem.to_dict()

    def status(self) -> dict:
        """Return Supreme Ecosystem status."""

        ecosystems = self.registry.list()

        return {
            "ecosystem": "SUPREME ECOSYSTEM",
            "status": self.status,
            "total_ecosystems": len(
                ecosystems
            ),
            "enabled_ecosystems": sum(
                1
                for ecosystem in ecosystems
                if ecosystem.enabled
            ),
            "personal_ecosystems": sum(
                1
                for ecosystem in ecosystems
                if ecosystem.ecosystem_type
                in {
                    "PERSONAL",
                    "PERSONAL_BRAND",
                }
            ),
            "company_ecosystems": sum(
                1
                for ecosystem in ecosystems
                if ecosystem.ecosystem_type
                in {
                    "COMPANY",
                    "COMPANY_GROUP",
                }
            ),
            "last_check": self.last_check,
        }

    def health(self) -> dict:
        """Return ecosystem health information."""

        ecosystems = self.registry.list()

        enabled = [
            ecosystem
            for ecosystem in ecosystems
            if ecosystem.enabled
        ]

        if not ecosystems:
            health = "UNKNOWN"
        elif len(enabled) == len(
            ecosystems
        ):
            health = "HEALTHY"
        elif enabled:
            health = "DEGRADED"
        else:
            health = "OFFLINE"

        return {
            "health": health,
            "total_ecosystems": len(
                ecosystems
            ),
            "enabled_ecosystems": len(
                enabled
            ),
            "disabled_ecosystems": (
                len(ecosystems)
                - len(enabled)
            ),
            "last_check": self.last_check,
        }

    def start(self) -> dict:
        """Start Supreme Ecosystem management."""

        self.status = "RUNNING"

        self.last_check = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        return self.status()

    def stop(self) -> dict:
        """Stop Supreme Ecosystem management."""

        self.status = "STOPPED"

        self.last_check = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        return self.status()

    def restart(self) -> dict:
        """Restart Supreme Ecosystem management."""

        self.stop()

        return self.start()    
