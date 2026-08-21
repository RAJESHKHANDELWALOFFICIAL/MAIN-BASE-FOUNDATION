"""Supreme Ecosystem registry."""

from typing import Dict, List

from .models import EcosystemIdentity


class EcosystemRegistry:
    """Central registry for Supreme Ecosystem identities."""

    def __init__(self):
        self.ecosystems: Dict[
            str,
            EcosystemIdentity,
        ] = {}

        self.register(
            EcosystemIdentity(
                ecosystem_id="PERSONAL-RAJESHKHANDELWAL",
                name="RAJESHKHANDELWAL",
                ecosystem_type="PERSONAL",
                repository_ref=(
                    "RAJESHKHANDELWALOFFICIAL/"
                    "RAJESHKHANDELWAL"
                ),
                status="REGISTERED",
                capabilities=[
                    "IDENTITY",
                    "PROFILE",
                    "WEBSITE",
                    "DOMAIN",
                    "PROJECTS",
                ],
            )
        )

        self.register(
            EcosystemIdentity(
                ecosystem_id="PERSONAL-RAJESHKHANDELWALOFFICIAL",
                name="RAJESHKHANDELWALOFFICIAL",
                ecosystem_type="PERSONAL",
                repository_ref=(
                    "RAJESHKHANDELWALOFFICIAL/"
                    "MAIN-BASE-FOUNDATION"
                ),
                status="REGISTERED",
                capabilities=[
                    "IDENTITY",
                    "PROFILE",
                    "BUSINESS",
                    "WEBSITE",
                    "DOMAIN",
                    "PROJECTS",
                ],
            )
        )

        self.register(
            EcosystemIdentity(
                ecosystem_id="PERSONAL-DRRAJESHKANDELWALIBC",
                name="DRRAJESHKANDELWALIBC",
                ecosystem_type="PERSONAL_BRAND",
                status="REGISTERED",
                capabilities=[
                    "IDENTITY",
                    "BRAND",
                    "BUSINESS",
                    "WEBSITE",
                    "DOMAIN",
                ],
            )
        )

        self.register(
            EcosystemIdentity(
                ecosystem_id=(
                    "PERSONAL-DRRAJESHKANDELWALIBCOFFICIAL"
                ),
                name="DRRAJESHKANDELWALIBCOFFICIAL",
                ecosystem_type="PERSONAL_BRAND",
                status="REGISTERED",
                capabilities=[
                    "IDENTITY",
                    "BRAND",
                    "BUSINESS",
                    "WEBSITE",
                    "DOMAIN",
                ],
            )
        )

        self.register(
            EcosystemIdentity(
                ecosystem_id=(
                    "COMPANY-KHANDELWALGROUPANDCOMPANY"
                ),
                name="KHANDELWALGROUPANDCOMPANY",
                ecosystem_type="COMPANY",
                status="REGISTERED",
                capabilities=[
                    "ORGANIZATION",
                    "BUSINESS",
                    "TEAM",
                    "PROJECTS",
                    "WEBSITE",
                    "DOMAIN",
                ],
            )
        )

        self.register(
            EcosystemIdentity(
                ecosystem_id=(
                    "COMPANY-KHANDELWALGROUPANDCOMPANYOFFICIAL"
                ),
                name="KHANDELWALGROUPANDCOMPANYOFFICIAL",
                ecosystem_type="COMPANY",
                status="REGISTERED",
                capabilities=[
                    "ORGANIZATION",
                    "BUSINESS",
                    "TEAM",
                    "PROJECTS",
                    "WEBSITE",
                    "DOMAIN",
                ],
            )
        )

        self.register(
            EcosystemIdentity(
                ecosystem_id=(
                    "COMPANY-KHANDELWALGROUPANDCOMPANIES"
                ),
                name="KHANDELWALGROUPANDCOMPANIES",
                ecosystem_type="COMPANY_GROUP",
                status="REGISTERED",
                capabilities=[
                    "ORGANIZATION",
                    "BUSINESS",
                    "TEAM",
                    "PROJECTS",
                    "WEBSITE",
                    "DOMAIN",
                ],
            )
        )

        self.register(
            EcosystemIdentity(
                ecosystem_id=(
                    "COMPANY-KHANDELWALGROUPANDCOMPANIESOFFICIAL"
                ),
                name="KHANDELWALGROUPANDCOMPANIESOFFICIAL",
                ecosystem_type="COMPANY_GROUP",
                status="REGISTERED",
                capabilities=[
                    "ORGANIZATION",
                    "BUSINESS",
                    "TEAM",
                    "PROJECTS",
                    "WEBSITE",
                    "DOMAIN",
                ],
            )
        )

    def register(
        self,
        ecosystem: EcosystemIdentity,
    ) -> None:
        """Register an ecosystem."""

        self.ecosystems[
            ecosystem.ecosystem_id
        ] = ecosystem

    def get(
        self,
        ecosystem_id: str,
    ) -> EcosystemIdentity:
        """Return one registered ecosystem."""

        key = ecosystem_id.strip()

        if key not in self.ecosystems:
            raise KeyError(
                f"Unknown ecosystem: {ecosystem_id}"
            )

        return self.ecosystems[key]

    def list(self) -> List[EcosystemIdentity]:
        """Return all registered ecosystems."""

        return list(
            self.ecosystems.values()
        )

    def names(self) -> List[str]:
        """Return all ecosystem names."""

        return [
            ecosystem.name
            for ecosystem in self.ecosystems.values()
        ]

    def statuses(self) -> List[dict]:
        """Return all ecosystem status records."""

        return [
            ecosystem.to_dict()
            for ecosystem in self.ecosystems.values()
        ]

    def exists(
        self,
        ecosystem_id: str,
    ) -> bool:
        """Check whether an ecosystem is registered."""

        return (
            ecosystem_id.strip()
            in self.ecosystems
        )
