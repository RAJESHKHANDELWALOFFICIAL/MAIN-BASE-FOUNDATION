"""
Language Engine — Transliteration Service

MAIN BASE FOUNDATION

Provider-independent transliteration foundation.

Transliteration converts text from one writing script
to another while preserving the underlying linguistic
representation as closely as the configured provider allows.

Example:

    हिंदी → hindi
    नमस्ते → namaste

Translation and transliteration are intentionally kept
as separate services.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .models import (
    LanguageRequest,
    TransliterationResult,
)


# =========================================================
# ✍️ TRANSLITERATION PROVIDER CONTRACT
# =========================================================

class TransliterationProvider(ABC):
    """
    Abstract contract for transliteration providers.
    """

    @abstractmethod
    def transliterate(
        self,
        request: LanguageRequest,
    ) -> TransliterationResult:
        """
        Transliterate a normalized language request.
        """
        raise NotImplementedError


# =========================================================
# 🧱 TRANSLITERATION SERVICE
# =========================================================

class TransliterationService:
    """
    Central transliteration service.

    Provider-specific implementations are injected through
    the TransliterationProvider contract.
    """

    def __init__(
        self,
        provider: Optional[
            TransliterationProvider
        ] = None,
    ) -> None:

        self.provider = provider

    # =====================================================
    # ⚙️ PROVIDER CONFIGURATION
    # =====================================================

    def set_provider(
        self,
        provider: TransliterationProvider,
    ) -> None:
        """
        Configure the transliteration provider.
        """

        if not hasattr(
            provider,
            "transliterate",
        ):

            raise TypeError(
                "Transliteration provider must implement "
                "transliterate()."
            )

        self.provider = provider

    # =====================================================
    # 🔌 PROVIDER STATUS
    # =====================================================

    @property
    def is_configured(self) -> bool:
        """
        Return whether a transliteration provider is
        configured.
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
        Validate a transliteration request.
        """

        if not isinstance(
            request,
            LanguageRequest,
        ):

            raise TypeError(
                "Transliteration request must be "
                "LanguageRequest."
            )

        if not request.text.strip():

            raise ValueError(
                "Transliteration text cannot be empty."
            )

        target_script = request.metadata.get(
            "target_script"
        )

        if not target_script:

            raise ValueError(
                "Target script is required."
            )

        if not target_script.strip():

            raise ValueError(
                "Target script cannot be empty."
            )

    # =====================================================
    # ✍️ TRANSLITERATE REQUEST
    # =====================================================

    def transliterate_request(
        self,
        request: LanguageRequest,
    ) -> TransliterationResult:
        """
        Execute a normalized transliteration request.
        """

        self.validate_request(request)

        if self.provider is None:

            raise RuntimeError(
                "No transliteration provider is configured."
            )

        result = self.provider.transliterate(
            request
        )

        if not isinstance(
            result,
            TransliterationResult,
        ):

            raise TypeError(
                "Transliteration provider must return "
                "TransliterationResult."
            )

        return result

    # =====================================================
    # ✍️ SIMPLE TRANSLITERATION API
    # =====================================================

    def transliterate(
        self,
        text: str,
        target_script: str,
        source_language: Optional[str] = None,
        metadata: Optional[
            Dict[str, str]
        ] = None,
    ) -> TransliterationResult:
        """
        Transliterate text using the configured provider.
        """

        request_metadata: Dict[str, str] = (
            dict(metadata)
            if metadata is not None
            else {}
        )

        request_metadata[
            "target_script"
        ] = target_script.strip().lower()

        request = LanguageRequest(
            text=text,
            source_language=source_language,
            operation="transliterate",
            metadata=request_metadata,
        )

        return self.transliterate_request(
            request
        )

    # =====================================================
    # 🌍 NORMALIZE SCRIPT
    # =====================================================

    @staticmethod
    def normalize_script(
        script: str,
    ) -> str:
        """
        Normalize a writing-script identifier.

        Example:

            Devanagari → devanagari
            Latin      → latin
        """

        if not isinstance(
            script,
            str,
        ):

            raise TypeError(
                "Script identifier must be a string."
            )

        normalized = script.strip().lower()

        if not normalized:

            raise ValueError(
                "Script identifier cannot be empty."
            )

        return normalized

    # =====================================================
    # 🔎 SOURCE LANGUAGE / SCRIPT RESOLUTION
    # =====================================================

    def resolve_source_language(
        self,
        text: str,
        source_language: Optional[str] = None,
        detector: Optional[Any] = None,
    ) -> Optional[str]:
        """
        Resolve the source language.

        Explicit source language takes priority.
        Otherwise an optional detector may be used.
        """

        if source_language:

            return source_language.strip().lower()

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
    # 🧠 AUTO-SOURCE TRANSLITERATION
    # =====================================================

    def transliterate_auto(
        self,
        text: str,
        target_script: str,
        detector: Optional[Any] = None,
        source_language: Optional[str] = None,
        metadata: Optional[
            Dict[str, str]
        ] = None,
    ) -> TransliterationResult:
        """
        Transliterate while optionally resolving the source
        language automatically.
        """

        resolved_source = (
            self.resolve_source_language(
                text=text,
                source_language=source_language,
                detector=detector,
            )
        )

        return self.transliterate(
            text=text,
            target_script=target_script,
            source_language=resolved_source,
            metadata=metadata,
        )

    # =====================================================
    # 📊 SERVICE STATUS
    # =====================================================

    def status(self) -> Dict[str, Any]:
        """
        Return transliteration service status.
        """

        return {
            "service": "transliteration",
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

class NullTransliterationProvider(
    TransliterationProvider
):
    """
    Explicit provider placeholder.

    It never pretends to perform transliteration.
    """

    def transliterate(
        self,
        request: LanguageRequest,
    ) -> TransliterationResult:

        raise RuntimeError(
            "NullTransliterationProvider cannot perform "
            "transliteration. Configure a real "
            "transliteration provider."
        )


# =========================================================
# 🌍 DEFAULT TRANSLITERATION SERVICE
# =========================================================

DEFAULT_TRANSLITERATION_SERVICE = (
    TransliterationService()
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "TransliterationProvider",
    "TransliterationService",
    "NullTransliterationProvider",
    "DEFAULT_TRANSLITERATION_SERVICE",
]
