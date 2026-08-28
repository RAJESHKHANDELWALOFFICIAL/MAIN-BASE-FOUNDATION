"""
Language Engine — Translation Service

MAIN BASE FOUNDATION

Provider-independent translation foundation.

This module defines the translation service contract,
validation, request normalization, and a safe provider
adapter.

Actual translation providers can be connected later
without changing the Language Engine manager.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .models import (
    LanguageRequest,
    TranslationResult,
)


# =========================================================
# 🔄 TRANSLATION PROVIDER CONTRACT
# =========================================================

class TranslationProvider(ABC):
    """
    Abstract contract for any translation provider.
    """

    @abstractmethod
    def translate(
        self,
        request: LanguageRequest,
    ) -> TranslationResult:
        """
        Translate a normalized language request.
        """
        raise NotImplementedError


# =========================================================
# 🧱 TRANSLATION SERVICE
# =========================================================

class TranslationService:
    """
    Central translation service.

    The service does not implement a proprietary or
    provider-specific translation algorithm.

    A provider is injected when actual translation
    capability is required.
    """

    def __init__(
        self,
        provider: Optional[TranslationProvider] = None,
    ) -> None:

        self.provider = provider

    # =====================================================
    # ⚙️ PROVIDER CONFIGURATION
    # =====================================================

    def set_provider(
        self,
        provider: TranslationProvider,
    ) -> None:
        """
        Configure the translation provider.
        """

        if not hasattr(provider, "translate"):

            raise TypeError(
                "Translation provider must implement "
                "translate()."
            )

        self.provider = provider

    # =====================================================
    # 🔌 PROVIDER STATUS
    # =====================================================

    @property
    def is_configured(self) -> bool:
        """
        Return whether a translation provider is configured.
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
        Validate a translation request.
        """

        if not isinstance(
            request,
            LanguageRequest,
        ):

            raise TypeError(
                "Translation request must be "
                "LanguageRequest."
            )

        if not request.text.strip():

            raise ValueError(
                "Translation text cannot be empty."
            )

        if not request.target_language:

            raise ValueError(
                "Target language is required."
            )

        if not request.target_language.strip():

            raise ValueError(
                "Target language cannot be empty."
            )

    # =====================================================
    # 🔄 TRANSLATE REQUEST
    # =====================================================

    def translate_request(
        self,
        request: LanguageRequest,
    ) -> TranslationResult:
        """
        Execute a normalized translation request.
        """

        self.validate_request(request)

        if self.provider is None:

            raise RuntimeError(
                "No translation provider is configured."
            )

        result = self.provider.translate(
            request
        )

        if not isinstance(
            result,
            TranslationResult,
        ):

            raise TypeError(
                "Translation provider must return "
                "TranslationResult."
            )

        return result

    # =====================================================
    # 🔄 SIMPLE TRANSLATE API
    # =====================================================

    def translate(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None,
        metadata: Optional[
            Dict[str, str]
        ] = None,
    ) -> TranslationResult:
        """
        Translate text using the configured provider.
        """

        request = LanguageRequest(
            text=text,
            source_language=source_language,
            target_language=target_language,
            operation="translate",
            metadata=(
                metadata
                if metadata is not None
                else {}
            ),
        )

        return self.translate_request(
            request
        )

    # =====================================================
    # 🌍 LANGUAGE PAIR
    # =====================================================

    @staticmethod
    def normalize_language_code(
        language_code: str,
    ) -> str:
        """
        Normalize a language code.

        Example:
            EN-us -> en-us
            HI -> hi
        """

        if not isinstance(
            language_code,
            str,
        ):

            raise TypeError(
                "Language code must be a string."
            )

        normalized = language_code.strip().lower()

        if not normalized:

            raise ValueError(
                "Language code cannot be empty."
            )

        return normalized

    # =====================================================
    # 🔎 SOURCE LANGUAGE RESOLUTION
    # =====================================================

    def resolve_source_language(
        self,
        text: str,
        source_language: Optional[str] = None,
        detector: Optional[Any] = None,
    ) -> Optional[str]:
        """
        Resolve the source language.

        If a source language is explicitly supplied,
        it is normalized and returned.

        Otherwise an optional detector may be used.
        """

        if source_language:

            return self.normalize_language_code(
                source_language
            )

        if detector is None:

            return None

        if not hasattr(
            detector,
            "detect",
        ):

            raise TypeError(
                "Language detector must provide "
                "detect()."
            )

        detection = detector.detect(
            text
        )

        return getattr(
            detection,
            "language_code",
            None,
        )

    # =====================================================
    # 🧠 AUTO-SOURCE TRANSLATION
    # =====================================================

    def translate_auto(
        self,
        text: str,
        target_language: str,
        detector: Optional[Any] = None,
        metadata: Optional[
            Dict[str, str]
        ] = None,
    ) -> TranslationResult:
        """
        Translate text while optionally detecting the
        source language automatically.
        """

        source_language = (
            self.resolve_source_language(
                text=text,
                detector=detector,
            )
        )

        return self.translate(
            text=text,
            source_language=source_language,
            target_language=target_language,
            metadata=metadata,
        )

    # =====================================================
    # 📊 SERVICE STATUS
    # =====================================================

    def status(self) -> Dict[str, Any]:
        """
        Return translation service status.
        """

        return {
            "service": "translation",
            "configured": self.is_configured,
            "provider": (
                self.provider.__class__.__name__
                if self.provider is not None
                else None
            ),
        }


# =========================================================
# 🧪 NULL / PLACEHOLDER PROVIDER
# =========================================================

class NullTranslationProvider(
    TranslationProvider
):
    """
    Explicit provider placeholder.

    It never pretends to perform translation.
    It exists only to make the absence of a real provider
    explicit and testable.
    """

    def translate(
        self,
        request: LanguageRequest,
    ) -> TranslationResult:

        raise RuntimeError(
            "NullTranslationProvider cannot perform "
            "translation. Configure a real translation "
            "provider."
        )


# =========================================================
# 🌍 DEFAULT TRANSLATION SERVICE
# =========================================================

DEFAULT_TRANSLATION_SERVICE = (
    TranslationService()
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "TranslationProvider",
    "TranslationService",
    "NullTranslationProvider",
    "DEFAULT_TRANSLATION_SERVICE",
]
