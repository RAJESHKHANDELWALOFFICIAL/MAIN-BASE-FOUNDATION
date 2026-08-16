"""
Language Engine — Language Registry

MAIN BASE FOUNDATION

Central registry for:

1. Human languages
2. Programming languages

This module stores language definitions and provides
registration, lookup, listing, alias, extension and
capability access.

The registry is provider-independent.
"""

from typing import Dict, List, Optional

from .models import (
    LanguageDefinition,
    ProgrammingLanguageDefinition,
)


# =========================================================
# 🌍 LANGUAGE REGISTRY
# =========================================================

class LanguageRegistry:
    """
    Central registry for human and programming languages.
    """

    def __init__(self) -> None:

        self._languages: Dict[
            str,
            LanguageDefinition,
        ] = {}

        self._programming_languages: Dict[
            str,
            ProgrammingLanguageDefinition,
        ] = {}

        self._programming_aliases: Dict[
            str,
            str,
        ] = {}

        self._programming_extensions: Dict[
            str,
            str,
        ] = {}

    # =====================================================
    # 🌍 HUMAN LANGUAGE REGISTRATION
    # =====================================================

    def register_language(
        self,
        language: LanguageDefinition,
    ) -> None:
        """
        Register a human language.
        """

        if not isinstance(
            language,
            LanguageDefinition,
        ):
            raise TypeError(
                "Language must be LanguageDefinition."
            )

        code = language.code.strip().lower()

        if code in self._languages:
            raise ValueError(
                f"Language already registered: {code}"
            )

        self._languages[code] = language

    # =====================================================
    # 🌍 HUMAN LANGUAGE LOOKUP
    # =====================================================

    def get_language(
        self,
        language_code: str,
    ) -> Optional[LanguageDefinition]:
        """
        Retrieve a human language by language code.
        """

        code = self._normalize_code(
            language_code
        )

        return self._languages.get(code)

    # =====================================================
    # 🌍 HUMAN LANGUAGE REQUIRE
    # =====================================================

    def require_language(
        self,
        language_code: str,
    ) -> LanguageDefinition:
        """
        Retrieve a language or raise an error.
        """

        language = self.get_language(
            language_code
        )

        if language is None:
            raise KeyError(
                f"Language not registered: "
                f"{language_code}"
            )

        return language

    # =====================================================
    # 🌍 HUMAN LANGUAGE EXISTS
    # =====================================================

    def has_language(
        self,
        language_code: str,
    ) -> bool:
        """
        Check whether a human language is registered.
        """

        return (
            self.get_language(language_code)
            is not None
        )

    # =====================================================
    # 🌍 HUMAN LANGUAGE LIST
    # =====================================================

    def list_languages(
        self,
    ) -> List[LanguageDefinition]:
        """
        Return all registered human languages.
        """

        return list(
            self._languages.values()
        )

    # =====================================================
    # 🌍 HUMAN LANGUAGE COUNT
    # =====================================================

    @property
    def language_count(self) -> int:
        """
        Return number of registered human languages.
        """

        return len(self._languages)

    # =====================================================
    # 💻 PROGRAMMING LANGUAGE REGISTRATION
    # =====================================================

    def register_programming_language(
        self,
        language: ProgrammingLanguageDefinition,
    ) -> None:
        """
        Register a programming language.
        """

        if not isinstance(
            language,
            ProgrammingLanguageDefinition,
        ):
            raise TypeError(
                "Programming language must be "
                "ProgrammingLanguageDefinition."
            )

        key = language.key.strip().lower()

        if key in self._programming_languages:
            raise ValueError(
                "Programming language already "
                f"registered: {key}"
            )

        self._programming_languages[
            key
        ] = language

        for alias in language.aliases:

            normalized_alias = (
                alias.strip().lower()
            )

            if normalized_alias:
                self._programming_aliases[
                    normalized_alias
                ] = key

        for extension in language.extensions:

            normalized_extension = (
                extension.strip().lower()
            )

            if not normalized_extension:
                continue

            if not normalized_extension.startswith(
                "."
            ):
                normalized_extension = (
                    "." + normalized_extension
                )

            self._programming_extensions[
                normalized_extension
            ] = key

    # =====================================================
    # 💻 PROGRAMMING LANGUAGE LOOKUP
    # =====================================================

    def get_programming_language(
        self,
        identifier: str,
    ) -> Optional[
        ProgrammingLanguageDefinition
    ]:
        """
        Retrieve a programming language by:

        - key
        - alias
        - file extension
        """

        normalized = (
            identifier.strip().lower()
        )

        if not normalized:
            return None

        language = (
            self._programming_languages.get(
                normalized
            )
        )

        if language is not None:
            return language

        key = self._programming_aliases.get(
            normalized
        )

        if key is not None:
            return self._programming_languages.get(
                key
            )

        extension = normalized

        if not extension.startswith("."):
            extension = "." + extension

        key = self._programming_extensions.get(
            extension
        )

        if key is not None:
            return self._programming_languages.get(
                key
            )

        return None

    # =====================================================
    # 💻 PROGRAMMING LANGUAGE REQUIRE
    # =====================================================

    def require_programming_language(
        self,
        identifier: str,
    ) -> ProgrammingLanguageDefinition:
        """
        Retrieve a programming language or raise an error.
        """

        language = (
            self.get_programming_language(
                identifier
            )
        )

        if language is None:
            raise KeyError(
                "Programming language not registered: "
                f"{identifier}"
            )

        return language

    # =====================================================
    # 💻 PROGRAMMING LANGUAGE EXISTS
    # =====================================================

    def has_programming_language(
        self,
        identifier: str,
    ) -> bool:
        """
        Check whether a programming language exists.
        """

        return (
            self.get_programming_language(
                identifier
            )
            is not None
        )

    # =====================================================
    # 💻 PROGRAMMING LANGUAGE LIST
    # =====================================================

    def list_programming_languages(
        self,
    ) -> List[
        ProgrammingLanguageDefinition
    ]:
        """
        Return all registered programming languages.
        """

        return list(
            self._programming_languages.values()
        )

    # =====================================================
    # 💻 PROGRAMMING LANGUAGE COUNT
    # =====================================================

    @property
    def programming_language_count(
        self,
    ) -> int:
        """
        Return number of registered programming
        languages.
        """

        return len(
            self._programming_languages
        )

    # =====================================================
    # 🔎 LANGUAGE CAPABILITY
    # =====================================================

    def get_language_capabilities(
        self,
        language_code: str,
    ) -> Dict[str, bool]:
        """
        Return supported capabilities of a human language.
        """

        language = self.require_language(
            language_code
        )

        return {
            "speech_to_text":
                language.speech_to_text,

            "text_to_speech":
                language.text_to_speech,

            "translation":
                language.translation,

            "transliteration":
                language.transliteration,

            "search":
                language.search,
        }

    # =====================================================
    # 📝 SCRIPT INFORMATION
    # =====================================================

    def get_language_scripts(
        self,
        language_code: str,
    ) -> List[str]:
        """
        Return scripts supported by a human language.
        """

        language = self.require_language(
            language_code
        )

        return list(
            language.scripts
        )

    # =====================================================
    # 🌐 LOCALE INFORMATION
    # =====================================================

    def get_language_locale(
        self,
        language_code: str,
    ) -> Optional[str]:
        """
        Return the locale associated with a language.
        """

        language = self.require_language(
            language_code
        )

        return language.locale

    # =====================================================
    # ↔️ TEXT DIRECTION
    # =====================================================

    def get_language_direction(
        self,
        language_code: str,
    ) -> str:
        """
        Return text direction:

        ltr = left-to-right
        rtl = right-to-left
        """

        language = self.require_language(
            language_code
        )

        return language.direction

    # =====================================================
    # 🧹 REGISTRY CLEAR
    # =====================================================

    def clear(self) -> None:
        """
        Clear all registered languages.
        """

        self._languages.clear()

        self._programming_languages.clear()

        self._programming_aliases.clear()

        self._programming_extensions.clear()

    # =====================================================
    # 📊 REGISTRY STATUS
    # =====================================================

    def status(self) -> Dict[str, int]:
        """
        Return registry statistics.
        """

        return {
            "human_languages":
                self.language_count,

            "programming_languages":
                self.programming_language_count,

            "programming_aliases":
                len(self._programming_aliases),

            "programming_extensions":
                len(self._programming_extensions),
        }

    # =====================================================
    # 🔧 INTERNAL NORMALIZATION
    # =====================================================

    @staticmethod
    def _normalize_code(
        language_code: str,
    ) -> str:
        """
        Normalize a human-language code.
        """

        if not isinstance(
            language_code,
            str,
        ):
            raise TypeError(
                "Language code must be a string."
            )

        code = (
            language_code.strip().lower()
        )

        if not code:
            raise ValueError(
                "Language code cannot be empty."
            )

        return code


# =========================================================
# 🌍 DEFAULT REGISTRY
# =========================================================

DEFAULT_LANGUAGE_REGISTRY = (
    LanguageRegistry()
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "LanguageRegistry",
    "DEFAULT_LANGUAGE_REGISTRY",
]
