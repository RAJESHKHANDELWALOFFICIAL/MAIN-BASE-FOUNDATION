"""
Language Engine — Speech Service

MAIN BASE FOUNDATION

Provider-independent speech foundation.

Supports two core operations:

1. SPEECH → TEXT
2. TEXT → SPEECH

Actual speech-recognition and text-to-speech providers
are connected through provider contracts.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .models import (
    LanguageRequest,
    SpeechResult,
)


# =========================================================
# 🎙️ SPEECH-TO-TEXT PROVIDER CONTRACT
# =========================================================

class SpeechToTextProvider(ABC):
    """
    Abstract contract for speech-to-text providers.
    """

    @abstractmethod
    def speech_to_text(
        self,
        request: LanguageRequest,
    ) -> SpeechResult:
        """
        Convert speech/audio into text.
        """
        raise NotImplementedError


# =========================================================
# 🔊 TEXT-TO-SPEECH PROVIDER CONTRACT
# =========================================================

class TextToSpeechProvider(ABC):
    """
    Abstract contract for text-to-speech providers.
    """

    @abstractmethod
    def text_to_speech(
        self,
        request: LanguageRequest,
    ) -> SpeechResult:
        """
        Convert text into speech/audio.
        """
        raise NotImplementedError


# =========================================================
# 🎙️ SPEECH SERVICE
# =========================================================

class SpeechService:
    """
    Central speech service.

    Keeps speech recognition and speech synthesis
    provider-independent.
    """

    def __init__(
        self,
        speech_to_text_provider: Optional[
            SpeechToTextProvider
        ] = None,
        text_to_speech_provider: Optional[
            TextToSpeechProvider
        ] = None,
    ) -> None:

        self.speech_to_text_provider = (
            speech_to_text_provider
        )

        self.text_to_speech_provider = (
            text_to_speech_provider
        )

    # =====================================================
    # ⚙️ PROVIDER CONFIGURATION
    # =====================================================

    def set_speech_to_text_provider(
        self,
        provider: SpeechToTextProvider,
    ) -> None:
        """
        Configure the speech-to-text provider.
        """

        if not hasattr(
            provider,
            "speech_to_text",
        ):
            raise TypeError(
                "Speech-to-text provider must implement "
                "speech_to_text()."
            )

        self.speech_to_text_provider = provider

    def set_text_to_speech_provider(
        self,
        provider: TextToSpeechProvider,
    ) -> None:
        """
        Configure the text-to-speech provider.
        """

        if not hasattr(
            provider,
            "text_to_speech",
        ):
            raise TypeError(
                "Text-to-speech provider must implement "
                "text_to_speech()."
            )

        self.text_to_speech_provider = provider

    # =====================================================
    # 🔌 PROVIDER STATUS
    # =====================================================

    @property
    def speech_to_text_configured(self) -> bool:
        """
        Return whether speech-to-text is configured.
        """

        return (
            self.speech_to_text_provider
            is not None
        )

    @property
    def text_to_speech_configured(self) -> bool:
        """
        Return whether text-to-speech is configured.
        """

        return (
            self.text_to_speech_provider
            is not None
        )

    # =====================================================
    # 📝 SPEECH-TO-TEXT VALIDATION
    # =====================================================

    @staticmethod
    def validate_speech_to_text_request(
        request: LanguageRequest,
    ) -> None:
        """
        Validate a speech-to-text request.
        """

        if not isinstance(
            request,
            LanguageRequest,
        ):
            raise TypeError(
                "Speech-to-text request must be "
                "LanguageRequest."
            )

        audio_reference = (
            request.metadata.get(
                "audio_reference"
            )
        )

        if not audio_reference:
            raise ValueError(
                "Audio reference is required."
            )

        if not audio_reference.strip():
            raise ValueError(
                "Audio reference cannot be empty."
            )

    # =====================================================
    # 📝 TEXT-TO-SPEECH VALIDATION
    # =====================================================

    @staticmethod
    def validate_text_to_speech_request(
        request: LanguageRequest,
    ) -> None:
        """
        Validate a text-to-speech request.
        """

        if not isinstance(
            request,
            LanguageRequest,
        ):
            raise TypeError(
                "Text-to-speech request must be "
                "LanguageRequest."
            )

        if not request.text.strip():
            raise ValueError(
                "Text-to-speech text cannot be empty."
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
    # 🎙️ SPEECH → TEXT
    # =====================================================

    def speech_to_text(
        self,
        audio_reference: str,
        language_code: Optional[str] = None,
        metadata: Optional[
            Dict[str, str]
        ] = None,
    ) -> SpeechResult:
        """
        Convert speech/audio into text.
        """

        request_metadata: Dict[str, str] = (
            dict(metadata)
            if metadata is not None
            else {}
        )

        request_metadata[
            "audio_reference"
        ] = audio_reference

        request = LanguageRequest(
            text="",
            source_language=language_code,
            operation="speech_to_text",
            metadata=request_metadata,
        )

        self.validate_speech_to_text_request(
            request
        )

        if (
            self.speech_to_text_provider
            is None
        ):
            raise RuntimeError(
                "No speech-to-text provider "
                "is configured."
            )

        result = (
            self.speech_to_text_provider
            .speech_to_text(request)
        )

        if not isinstance(
            result,
            SpeechResult,
        ):
            raise TypeError(
                "Speech-to-text provider must return "
                "SpeechResult."
            )

        return result

    # =====================================================
    # 🔊 TEXT → SPEECH
    # =====================================================

    def text_to_speech(
        self,
        text: str,
        language_code: str,
        metadata: Optional[
            Dict[str, str]
        ] = None,
    ) -> SpeechResult:
        """
        Convert text into speech/audio.
        """

        request = LanguageRequest(
            text=text,
            target_language=language_code,
            operation="text_to_speech",
            metadata=(
                dict(metadata)
                if metadata is not None
                else {}
            ),
        )

        self.validate_text_to_speech_request(
            request
        )

        if (
            self.text_to_speech_provider
            is None
        ):
            raise RuntimeError(
                "No text-to-speech provider "
                "is configured."
            )

        result = (
            self.text_to_speech_provider
            .text_to_speech(request)
        )

        if not isinstance(
            result,
            SpeechResult,
        ):
            raise TypeError(
                "Text-to-speech provider must return "
                "SpeechResult."
            )

        return result

    # =====================================================
    # 🌍 LANGUAGE NORMALIZATION
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
        Return current speech-service status.
        """

        return {
            "service": "speech",
            "speech_to_text": (
                self.speech_to_text_configured
            ),
            "text_to_speech": (
                self.text_to_speech_configured
            ),
            "speech_to_text_provider": (
                self.speech_to_text_provider
                .__class__.__name__
                if self.speech_to_text_provider
                is not None
                else None
            ),
            "text_to_speech_provider": (
                self.text_to_speech_provider
                .__class__.__name__
                if self.text_to_speech_provider
                is not None
                else None
            ),
        }


# =========================================================
# 🧪 NULL SPEECH-TO-TEXT PROVIDER
# =========================================================

class NullSpeechToTextProvider(
    SpeechToTextProvider
):
    """
    Explicit placeholder provider.

    It never pretends to perform speech recognition.
    """

    def speech_to_text(
        self,
        request: LanguageRequest,
    ) -> SpeechResult:

        raise RuntimeError(
            "NullSpeechToTextProvider cannot perform "
            "speech recognition. Configure a real "
            "speech-to-text provider."
        )


# =========================================================
# 🧪 NULL TEXT-TO-SPEECH PROVIDER
# =========================================================

class NullTextToSpeechProvider(
    TextToSpeechProvider
):
    """
    Explicit placeholder provider.

    It never pretends to generate speech.
    """

    def text_to_speech(
        self,
        request: LanguageRequest,
    ) -> SpeechResult:

        raise RuntimeError(
            "NullTextToSpeechProvider cannot perform "
            "text-to-speech. Configure a real "
            "text-to-speech provider."
        )


# =========================================================
# 🌍 DEFAULT SPEECH SERVICE
# =========================================================

DEFAULT_SPEECH_SERVICE = SpeechService()


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "SpeechToTextProvider",
    "TextToSpeechProvider",
    "SpeechService",
    "NullSpeechToTextProvider",
    "NullTextToSpeechProvider",
    "DEFAULT_SPEECH_SERVICE",
]
