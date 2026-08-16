"""
Language Engine — Language Registry

MAIN BASE FOUNDATION

Central registry for:
1. Human languages
2. Programming languages

The registry stores language metadata and capability declarations.
Actual translation, speech, detection, transliteration and search
providers are implemented separately.
"""

from typing import Dict, Iterable, List, Optional

from .models import (
    LanguageDefinition,
    ProgrammingLanguageDefinition,
)


# =========================================================
# 🌍 HUMAN LANGUAGE REGISTRY
# =========================================================

class HumanLanguageRegistry:
    """
    Registry for supported human languages.
    """

    def __init__(
        self,
        languages: Optional[
            Iterable[LanguageDefinition]
        ] = None,
    ) -> None:

        self._languages: Dict[
            str, LanguageDefinition
        ] = {}

        if languages:
            for language in languages:
                self.register(language)

    # -----------------------------------------------------
    # REGISTER
    # -----------------------------------------------------

    def register(
        self,
        language: LanguageDefinition,
    ) -> None:
        """Register or replace a human language."""

        code = language.code.strip().lower()

        if not code:
            raise ValueError(
                "Language code cannot be empty."
            )

        self._languages[code] = language

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    def get(
        self,
        code: str,
    ) -> Optional[LanguageDefinition]:
        """Return a language by code."""

        return self._languages.get(
            code.strip().lower()
        )

    # -----------------------------------------------------
    # EXISTS
    # -----------------------------------------------------

    def exists(
        self,
        code: str,
    ) -> bool:
        """Check whether a language is registered."""

        return (
            code.strip().lower()
            in self._languages
        )

    # -----------------------------------------------------
    # REMOVE
    # -----------------------------------------------------

    def remove(
        self,
        code: str,
    ) -> bool:
        """Remove a registered language."""

        normalized = code.strip().lower()

        if normalized not in self._languages:
            return False

        del self._languages[normalized]

        return True

    # -----------------------------------------------------
    # ALL
    # -----------------------------------------------------

    def all(self) -> List[LanguageDefinition]:
        """Return all registered human languages."""

        return list(self._languages.values())

    # -----------------------------------------------------
    # COUNT
    # -----------------------------------------------------

    def count(self) -> int:
        """Return number of registered human languages."""

        return len(self._languages)

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    def search(
        self,
        query: str,
    ) -> List[LanguageDefinition]:
        """
        Search languages by code, name or native name.
        """

        term = query.strip().lower()

        if not term:
            return self.all()

        return [
            language
            for language in self._languages.values()
            if (
                term in language.code.lower()
                or term in language.name.lower()
                or term in language.native_name.lower()
            )
        ]


# =========================================================
# 💻 PROGRAMMING LANGUAGE REGISTRY
# =========================================================

class ProgrammingLanguageRegistry:
    """
    Registry for programming languages.
    """

    def __init__(
        self,
        languages: Optional[
            Iterable[ProgrammingLanguageDefinition]
        ] = None,
    ) -> None:

        self._languages: Dict[
            str, ProgrammingLanguageDefinition
        ] = {}

        if languages:
            for language in languages:
                self.register(language)

    # -----------------------------------------------------
    # REGISTER
    # -----------------------------------------------------

    def register(
        self,
        language: ProgrammingLanguageDefinition,
    ) -> None:
        """Register or replace a programming language."""

        key = language.key.strip().lower()

        if not key:
            raise ValueError(
                "Programming language key cannot be empty."
            )

        self._languages[key] = language

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    def get(
        self,
        key: str,
    ) -> Optional[ProgrammingLanguageDefinition]:
        """Return a programming language by key."""

        return self._languages.get(
            key.strip().lower()
        )

    # -----------------------------------------------------
    # EXISTS
    # -----------------------------------------------------

    def exists(
        self,
        key: str,
    ) -> bool:
        """Check whether a programming language exists."""

        return (
            key.strip().lower()
            in self._languages
        )

    # -----------------------------------------------------
    # ALL
    # -----------------------------------------------------

    def all(
        self,
    ) -> List[ProgrammingLanguageDefinition]:
        """Return all registered programming languages."""

        return list(self._languages.values())

    # -----------------------------------------------------
    # COUNT
    # -----------------------------------------------------

    def count(self) -> int:
        """Return number of registered programming languages."""

        return len(self._languages)

    # -----------------------------------------------------
    # FIND BY EXTENSION
    # -----------------------------------------------------

    def find_by_extension(
        self,
        extension: str,
    ) -> Optional[ProgrammingLanguageDefinition]:
        """
        Find a programming language by file extension.

        Examples:
            .py
            .js
            .ts
        """

        normalized = extension.strip().lower()

        if not normalized:
            return None

        if not normalized.startswith("."):
            normalized = f".{normalized}"

        for language in self._languages.values():

            extensions = {
                item.strip().lower()
                for item in language.extensions
            }

            if normalized in extensions:
                return language

        return None

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    def search(
        self,
        query: str,
    ) -> List[ProgrammingLanguageDefinition]:
        """Search programming languages."""

        term = query.strip().lower()

        if not term:
            return self.all()

        results: List[
            ProgrammingLanguageDefinition
        ] = []

        for language in self._languages.values():

            searchable_values = [
                language.key,
                language.name,
                *language.aliases,
            ]

            if any(
                term in value.lower()
                for value in searchable_values
            ):
                results.append(language)

        return results


# =========================================================
# 🌐 GLOBAL LANGUAGE REGISTRY
# =========================================================

class GlobalLanguageRegistry:
    """
    Unified registry containing both human-language and
    programming-language registries.
    """

    def __init__(self) -> None:

        self.human = HumanLanguageRegistry()

        self.programming = ProgrammingLanguageRegistry()

    # -----------------------------------------------------
    # HUMAN LANGUAGE
    # -----------------------------------------------------

    def register_human_language(
        self,
        language: LanguageDefinition,
    ) -> None:
        """Register a human language."""

        self.human.register(language)

    # -----------------------------------------------------
    # PROGRAMMING LANGUAGE
    # -----------------------------------------------------

    def register_programming_language(
        self,
        language: ProgrammingLanguageDefinition,
    ) -> None:
        """Register a programming language."""

        self.programming.register(language)

    # -----------------------------------------------------
    # HUMAN LANGUAGE LOOKUP
    # -----------------------------------------------------

    def get_human_language(
        self,
        code: str,
    ) -> Optional[LanguageDefinition]:
        """Get a human language."""

        return self.human.get(code)

    # -----------------------------------------------------
    # PROGRAMMING LANGUAGE LOOKUP
    # -----------------------------------------------------

    def get_programming_language(
        self,
        key: str,
    ) -> Optional[ProgrammingLanguageDefinition]:
        """Get a programming language."""

        return self.programming.get(key)

    # -----------------------------------------------------
    # PROGRAMMING EXTENSION LOOKUP
    # -----------------------------------------------------

    def find_programming_language_by_extension(
        self,
        extension: str,
    ) -> Optional[ProgrammingLanguageDefinition]:
        """Find programming language by file extension."""

        return self.programming.find_by_extension(
            extension
        )

    # -----------------------------------------------------
    # COUNTS
    # -----------------------------------------------------

    def human_language_count(self) -> int:
        """Return registered human-language count."""

        return self.human.count()

    def programming_language_count(self) -> int:
        """Return registered programming-language count."""

        return self.programming.count()


# =========================================================
# 🌍 DEFAULT GLOBAL REGISTRY
# =========================================================

GLOBAL_LANGUAGE_REGISTRY = GlobalLanguageRegistry()


__all__ = [
    "HumanLanguageRegistry",
    "ProgrammingLanguageRegistry",
    "GlobalLanguageRegistry",
    "GLOBAL_LANGUAGE_REGISTRY",
]
