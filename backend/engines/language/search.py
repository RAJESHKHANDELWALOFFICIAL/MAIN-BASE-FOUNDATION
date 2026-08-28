"""
Language Engine — Multilingual Search Service

MAIN BASE FOUNDATION

Provider-independent multilingual search foundation.

This module defines the search provider contract,
request validation, language-aware query normalization,
search execution, and service status.

Actual search providers are connected through the
SearchProvider contract.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    LanguageRequest,
    LanguageSearchResult,
)


# =========================================================
# 🔎 SEARCH PROVIDER CONTRACT
# =========================================================

class SearchProvider(ABC):
    """
    Abstract contract for multilingual search providers.
    """

    @abstractmethod
    def search(
        self,
        request: LanguageRequest,
    ) -> LanguageSearchResult:
        """
        Execute a multilingual search request.
        """
        raise NotImplementedError


# =========================================================
# 🧱 SEARCH SERVICE
# =========================================================

class SearchService:
    """
    Central multilingual search service.

    The service remains provider-independent and allows
    different search providers to be connected later.
    """

    def __init__(
        self,
        provider: Optional[SearchProvider] = None,
    ) -> None:

        self.provider = provider

    # =====================================================
    # ⚙️ PROVIDER CONFIGURATION
    # =====================================================

    def set_provider(
        self,
        provider: SearchProvider,
    ) -> None:
        """
        Configure the search provider.
        """

        if not hasattr(
            provider,
            "search",
        ):
            raise TypeError(
                "Search provider must implement search()."
            )

        self.provider = provider

    # =====================================================
    # 🔌 PROVIDER STATUS
    # =====================================================

    @property
    def is_configured(self) -> bool:
        """
        Return whether a search provider is configured.
        """

        return self.provider is not None

    # =====================================================
    # 📝 REQUEST VALIDATION
    # =====================================================

    @staticmethod
    def validate_request(
        request: LanguageRequest,
    ) -> None:
        """
        Validate a multilingual search request.
        """

        if not isinstance(
            request,
            LanguageRequest,
        ):
            raise TypeError(
                "Search request must be LanguageRequest."
            )

        if not request.text.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

    # =====================================================
    # 🔎 SEARCH REQUEST
    # =====================================================

    def search_request(
        self,
        request: LanguageRequest,
    ) -> LanguageSearchResult:
        """
        Execute a normalized multilingual search request.
        """

        self.validate_request(request)

        if self.provider is None:
            raise RuntimeError(
                "No search provider is configured."
            )

        result = self.provider.search(
            request
        )

        if not isinstance(
            result,
            LanguageSearchResult,
        ):
            raise TypeError(
                "Search provider must return "
                "LanguageSearchResult."
            )

        return result

    # =====================================================
    # 🌍 SIMPLE MULTILINGUAL SEARCH API
    # =====================================================

    def search(
        self,
        query: str,
        language_code: Optional[str] = None,
        metadata: Optional[
            Dict[str, str]
        ] = None,
    ) -> LanguageSearchResult:
        """
        Search using the configured provider.

        language_code is optional so providers can perform
        automatic language detection when supported.
        """

        request = LanguageRequest(
            text=query,
            source_language=language_code,
            operation="search",
            metadata=(
                dict(metadata)
                if metadata is not None
                else {}
            ),
        )

        return self.search_request(
            request
        )

    # =====================================================
    # 🌐 LANGUAGE NORMALIZATION
    # =====================================================

    @staticmethod
    def normalize_language_code(
        language_code: str,
    ) -> str:
        """
        Normalize a language code.

        Examples:

            EN      → en
            HI      → hi
            en-US   → en-us
        """

        if not isinstance(
            language_code,
            str,
        ):
            raise TypeError(
                "Language code must be a string."
            )

        normalized = (
            language_code.strip().lower()
        )

        if not normalized:
            raise ValueError(
                "Language code cannot be empty."
            )

        return normalized

    # =====================================================
    # 🔎 QUERY NORMALIZATION
    # =====================================================

    @staticmethod
    def normalize_query(
        query: str,
    ) -> str:
        """
        Normalize a search query without changing
        its linguistic meaning.
        """

        if not isinstance(
            query,
            str,
        ):
            raise TypeError(
                "Search query must be a string."
            )

        normalized = " ".join(
            query.strip().split()
        )

        if not normalized:
            raise ValueError(
                "Search query cannot be empty."
            )

        return normalized

    # =====================================================
    # 🌍 LANGUAGE-AWARE SEARCH
    # =====================================================

    def search_in_language(
        self,
        query: str,
        language_code: str,
        metadata: Optional[
            Dict[str, str]
        ] = None,
    ) -> LanguageSearchResult:
        """
        Execute a search explicitly associated with
        a language.
        """

        normalized_query = (
            self.normalize_query(query)
        )

        normalized_language = (
            self.normalize_language_code(
                language_code
            )
        )

        return self.search(
            query=normalized_query,
            language_code=normalized_language,
            metadata=metadata,
        )

    # =====================================================
    # 🔎 SEARCH RESULT NORMALIZATION
    # =====================================================

    @staticmethod
    def normalize_results(
        results: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        """
        Normalize provider search results into a safe
        list structure.
        """

        if not isinstance(
            results,
            list,
        ):
            raise TypeError(
                "Search results must be a list."
            )

        normalized_results: List[
            Dict[str, str]
        ] = []

        for result in results:

            if not isinstance(
                result,
                dict,
            ):
                continue

            normalized_result: Dict[str, str] = {}

            for key, value in result.items():

                if not isinstance(
                    key,
                    str,
                ):
                    continue

                normalized_result[key] = str(
                    value
                )

            normalized_results.append(
                normalized_result
            )

        return normalized_results

    # =====================================================
    # 📊 SERVICE STATUS
    # =====================================================

    def status(self) -> Dict[str, Any]:
        """
        Return multilingual search service status.
        """

        return {
            "service": "search",
            "configured": self.is_configured,
            "provider": (
                self.provider.__class__.__name__
                if self.provider is not None
                else None
            ),
        }


# =========================================================
# 🧪 NULL / PLACEHOLDER SEARCH PROVIDER
# =========================================================

class NullSearchProvider(
    SearchProvider
):
    """
    Explicit provider placeholder.

    It never pretends to perform a real search.
    """

    def search(
        self,
        request: LanguageRequest,
    ) -> LanguageSearchResult:

        raise RuntimeError(
            "NullSearchProvider cannot perform "
            "search. Configure a real search provider."
        )


# =========================================================
# 🌍 DEFAULT SEARCH SERVICE
# =========================================================

DEFAULT_SEARCH_SERVICE = (
    SearchService()
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "SearchProvider",
    "SearchService",
    "NullSearchProvider",
    "DEFAULT_SEARCH_SERVICE",
]
