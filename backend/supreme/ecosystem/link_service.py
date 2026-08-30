"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Link Service

Central service for managing reusable ecosystem links.

Supports:
- Multiple links per ecosystem entity
- Create
- Get
- List
- Update
- Reorder
- Activate / deactivate
- Delete

The service is intentionally independent from:
- Posts
- Profiles
- Pages
- Channels
- Groups
- Communities
- Businesses
- Organizations

Those entities can reference this service later.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from backend.supreme.ecosystem.link import (
    EcosystemLink,
)


class EcosystemLinkService:
    """Central service for reusable SUPREME ecosystem links."""

    def __init__(self) -> None:

        self._links: Dict[
            str,
            EcosystemLink,
        ] = {}

        self._initialized = False

        self._next_link_number = 1

    # =========================================================
    # 🚀 INITIALIZE
    # =========================================================

    def initialize(self) -> dict:
        """Initialize the ecosystem link service."""

        self._initialized = True

        return {
            "service": "SUPREME_ECOSYSTEM_LINK",
            "status": "READY",
            "initialized": True,
        }

    # =========================================================
    # 🔑 INTERNAL LINK KEY
    # =========================================================

    def _generate_link_key(self) -> str:
        """
        Generate an internal service key.

        This is NOT a public/global ecosystem ID.
        """

        key = f"LINK-{self._next_link_number}"

        self._next_link_number += 1

        return key

    # =========================================================
    # ➕ CREATE
    # =========================================================

    def create_link(
        self,
        owner_type: str,
        owner_id: str,
        title: str,
        url: str,
        icon: str = "",
        display_order: int = 0,
        metadata: Optional[dict] = None,
    ) -> EcosystemLink:
        """Create a reusable ecosystem link."""

        link = EcosystemLink(
            owner_type=owner_type,
            owner_id=owner_id,
            title=title,
            url=url,
            icon=icon,
            display_order=display_order,
            active=True,
            metadata=(
                metadata
                if isinstance(metadata, dict)
                else {}
            ),
        )

        key = self._generate_link_key()

        self._links[key] = link

        return link

    # =========================================================
    # 🔎 GET
    # =========================================================

    def get_link(
        self,
        link_key: str,
    ) -> Optional[EcosystemLink]:
        """Return a stored ecosystem link."""

        return self._links.get(
            link_key
        )

    # =========================================================
    # 📋 LIST BY OWNER
    # =========================================================

    def list_links(
        self,
        owner_type: str,
        owner_id: str,
        active_only: bool = False,
    ) -> List[EcosystemLink]:
        """
        Return links belonging to one ecosystem entity.
        """

        links = [
            link
            for link in self._links.values()
            if link.owner_type == owner_type
            and link.owner_id == owner_id
        ]

        if active_only:
            links = [
                link
                for link in links
                if link.active
            ]

        return sorted(
            links,
            key=lambda link: link.display_order,
        )

    # =========================================================
    # ✏️ UPDATE
    # =========================================================

    def update_link(
        self,
        link_key: str,
        title: Optional[str] = None,
        url: Optional[str] = None,
        icon: Optional[str] = None,
        display_order: Optional[int] = None,
        active: Optional[bool] = None,
        metadata: Optional[dict] = None,
    ) -> Optional[EcosystemLink]:
        """Update an existing ecosystem link."""

        link = self._links.get(
            link_key
        )

        if link is None:
            return None

        if title is not None:

            if not title.strip():
                raise ValueError(
                    "title cannot be empty."
                )

            link.title = title

        if url is not None:

            if not url.strip():
                raise ValueError(
                    "url cannot be empty."
                )

            link.url = url

        if icon is not None:
            link.icon = icon

        if display_order is not None:

            if display_order < 0:
                raise ValueError(
                    "display_order cannot be negative."
                )

            link.display_order = display_order

        if active is not None:
            link.active = active

        if metadata is not None:

            if not isinstance(
                metadata,
                dict,
            ):
                raise TypeError(
                    "metadata must be a dictionary."
                )

            link.metadata = metadata

        return link

    # =========================================================
    # 🔄 REORDER
    # =========================================================

    def reorder_link(
        self,
        link_key: str,
        display_order: int,
    ) -> Optional[EcosystemLink]:
        """Change the display order of a link."""

        if display_order < 0:
            raise ValueError(
                "display_order cannot be negative."
            )

        link = self._links.get(
            link_key
        )

        if link is None:
            return None

        link.display_order = display_order

        return link

    # =========================================================
    # ⛔ ACTIVATE / DEACTIVATE
    # =========================================================

    def set_active(
        self,
        link_key: str,
        active: bool,
    ) -> Optional[EcosystemLink]:
        """Activate or deactivate a link."""

        link = self._links.get(
            link_key
        )

        if link is None:
            return None

        link.active = active

        return link

    # =========================================================
    # ❌ DELETE
    # =========================================================

    def delete_link(
        self,
        link_key: str,
    ) -> bool:
        """Delete an ecosystem link."""

        return (
            self._links.pop(
                link_key,
                None,
            )
            is not None
        )

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return ecosystem link service status."""

        return {
            "service": "SUPREME_ECOSYSTEM_LINK",
            "initialized": self._initialized,
            "total_links": len(
                self._links
            ),
        }


__all__ = [
    "EcosystemLinkService",
]
