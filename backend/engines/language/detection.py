"""
Language Engine — Language Detection Service

MAIN BASE FOUNDATION

Provider-independent language detection foundation.

This module defines:

- Detection provider contract
- Text validation
- Language detection
- Candidate languages
- Confidence
- Script information
- Service status

Actual language-detection implementations are connected
through the DetectionProvider contract.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .models import (
    LanguageDetectionResult,
)


# =========================================================
# 🔎 DETECTION PROVIDER CONTRACT
# =========================================================

class DetectionProvider(ABC):
    """
    Abstract contract for language-detection providers.
    """

    @abstractmethod
    def detect(
        self,
        text: str,
    ) -> LanguageDetectionResult:
        """
        Detect the language of supplied text.
        """
        raise NotImplementedError


# =========================================================
# 🧱 DETECTION SERVICE
# =========================================================

class LanguageDetectionService:
    """
    Central language-detection service.

    The service is provider-independent.

    A real detection provider can be connected later
    without changing the Language Engine architecture.
    """

    def __init__(
        self,
        provider: Optional[
            DetectionProvider
        ] = None,
    ) -> None:

        self.provider = provider

    # =====================================================
    # ⚙️ PROVIDER CONFIGURATION
    # =====================================================

    def set_provider(
        self,
        provider: DetectionProvider,
    ) -> None:
        """
        Configure the detection provider.
        """

        if not hasattr(
            provider,
            "detect",
        ):
            raise TypeError(
                "Detection provider must implement "
                "detect()."
            )

        self.provider = provider

    # =====================================================
    # 🔌 PROVIDER STATUS
    # =====================================================

    @property
    def is_configured(self) -> bool:
        """
        Return whether a detection provider is configured.
        """

        return self.provider is not None

    # =====================================================
    # 📝 TEXT VALIDATION
    # =====================================================

    @staticmethod
    def validate_text(
        text: str,
    ) -> None:
        """
        Validate text before detection.
        """

        if not isinstance(
            text,
            str,
        ):
            raise TypeError(
                "Detection text must be a string."
            )

        if not text.strip():
            raise ValueError(
                "Detection text cannot be empty."
            )

    # =====================================================
    # 🔎 DETECT
    # =====================================================

    def detect(
        self,
        text: str,
    ) -> LanguageDetectionResult:
        """
        Detect the language of supplied text.
        """

        self.validate_text(text)

        if self.provider is None:
            raise RuntimeError(
                "No language detection provider "
                "is configured."
            )

        result = self.provider.detect(
            text
        )

        if not isinstance(
            result,
            LanguageDetectionResult,
        ):
            raise TypeError(
                "Detection provider must return "
                "LanguageDetectionResult."
            )

        return result

    # =====================================================
    # 🌍 DETECT LANGUAGE CODE
    # =====================================================

    def detect_language_code(
        self,
        text: str,
    ) -> Optional[str]:
        """
        Return only the detected language code.
        """

        result = self.detect(text)

        return result.language_code

    # =====================================================
    # 📊 DETECT CONFIDENCE
    # =====================================================

    def detect_confidence(
        self,
        text: str,
    ) -> float:
        """
        Return detection confidence.
        """

        result = self.detect(text)

        return result.confidence

    # =====================================================
    # 📝 DETECT SCRIPT
    # =====================================================

    def detect_script(
        self,
        text: str,
    ) -> Optional[str]:
        """
        Return the detected writing script.
        """

        result = self.detect(text)

        return result.script

    # =====================================================
    # 🔎 DETECT CANDIDATES
    # =====================================================

    def detect_candidates(
        self,
        text: str,
    ) -> list[str]:
        """
        Return candidate language codes.
        """

        result = self.detect(text)

        return list(
            result.candidates
        )

    # =====================================================
    # 🎯 CONFIDENCE CHECK
    # =====================================================

    def is_confident(
        self,
        text: str,
        threshold: float = 0.80,
    ) -> bool:
        """
        Determine whether detection confidence meets
        the supplied threshold.
        """

        if not 0.0 <= threshold <= 1.0:
            raise ValueError(
                "Confidence threshold must be between "
                "0.0 and 1.0."
            )

        confidence = (
            self.detect_confidence(text)
        )

        return confidence >= threshold

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

            EN → en
            HI → hi
            en-US → en-us
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
    # 📊 SERVICE STATUS
    # =====================================================

    def status(self) -> Dict[str, Any]:
        """
        Return language detection service status.
        """

        return {
            "service": "language_detection",
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

class NullDetectionProvider(
    DetectionProvider
):
    """
    Explicit provider placeholder.

    It never pretends to detect a language.
    """

    def detect(
        self,
        text: str,
    ) -> LanguageDetectionResult:

        raise RuntimeError(
            "NullDetectionProvider cannot perform "
            "language detection. Configure a real "
            "detection provider."
        )


# =========================================================
# 🌍 DEFAULT DETECTION SERVICE
# =========================================================

DEFAULT_DETECTION_SERVICE = (
    LanguageDetectionService()
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "DetectionProvider",
    "LanguageDetectionService",
    "NullDetectionProvider",
    "DEFAULT_DETECTION_SERVICE",
]
