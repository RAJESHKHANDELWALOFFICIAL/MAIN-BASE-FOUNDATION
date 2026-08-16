"""
Language Engine — Central Manager

MAIN BASE FOUNDATION

Central orchestration layer for language operations.

The manager coordinates:
- Language detection
- Translation
- Transliteration
- Speech processing
- Multilingual search

Provider-specific implementations remain isolated from
this manager.
"""

from typing import Any, Dict, Optional

from .detection import LanguageDetector
from .models import (
    LanguageDetectionResult,
    LanguageRequest,
    LanguageSearchResult,
    SpeechResult,
    TranslationResult,
    TransliterationResult,
)
from .registry import GlobalLanguageRegistry


# =========================================================
# 🌍 LANGUAGE ENGINE MANAGER
# =========================================================

class LanguageEngineManager:
    """
    Central manager for the Global Language Engine.

    This class provides one consistent interface for
    language-related operations while keeping individual
    providers and services independent.
    """

    def __init__(
        self,
        registry: Optional[
            GlobalLanguageRegistry
        ] = None,
        translator: Optional[Any] = None,
        transliterator: Optional[Any] = None,
        speech_engine: Optional[Any] = None,
        search_engine: Optional[Any] = None,
    ) -> None:

        self.registry = (
            registry
            if registry is not None
            else GlobalLanguageRegistry()
        )

        self.detector = LanguageDetector(
            registry=self.registry
        )

        self.translator = translator
        self.transliterator = transliterator
        self.speech_engine = speech_engine
        self.search_engine = search_engine

    # =====================================================
    # 🔎 LANGUAGE DETECTION
    # =====================================================

    def detect(
        self,
        text: str,
    ) -> LanguageDetectionResult:
        """
        Detect the language and writing script of text.
        """

        return self.detector.detect(text)

    # =====================================================
    # 🔄 TRANSLATION
    # =====================================================

    def translate(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None,
    ) -> TranslationResult:
        """
        Translate text through the configured translator.

        A translator implementation must be supplied before
        translation can be executed.
        """

        if self.translator is None:
            raise RuntimeError(
                "No translation provider is configured."
            )

        request = LanguageRequest(
            text=text,
            source_language=source_language,
            target_language=target_language,
            operation="translate",
        )

        if hasattr(self.translator, "translate"):

            result = self.translator.translate(
                request
            )

        elif callable(self.translator):

            result = self.translator(request)

        else:

            raise TypeError(
                "Configured translator does not provide "
                "a supported translation interface."
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
    # ✍️ TRANSLITERATION
    # =====================================================

    def transliterate(
        self,
        text: str,
        target_script: str,
        source_language: Optional[str] = None,
    ) -> TransliterationResult:
        """
        Transliterate text through the configured service.
        """

        if self.transliterator is None:
            raise RuntimeError(
                "No transliteration provider is configured."
            )

        request = LanguageRequest(
            text=text,
            source_language=source_language,
            operation="transliterate",
            metadata={
                "target_script": target_script
            },
        )

        if hasattr(
            self.transliterator,
            "transliterate",
        ):

            result = self.transliterator.transliterate(
                request
            )

        elif callable(self.transliterator):

            result = self.transliterator(request)

        else:

            raise TypeError(
                "Configured transliterator does not provide "
                "a supported transliteration interface."
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
    # 🎙️ SPEECH-TO-TEXT
    # =====================================================

    def speech_to_text(
        self,
        audio_reference: str,
        language_code: Optional[str] = None,
    ) -> SpeechResult:
        """
        Convert speech/audio into text.

        The actual speech provider is injected separately.
        """

        if self.speech_engine is None:
            raise RuntimeError(
                "No speech provider is configured."
            )

        request = LanguageRequest(
            text="",
            source_language=language_code,
            operation="speech_to_text",
            metadata={
                "audio_reference": audio_reference
            },
        )

        if hasattr(
            self.speech_engine,
            "speech_to_text",
        ):

            result = self.speech_engine.speech_to_text(
                request
            )

        elif callable(self.speech_engine):

            result = self.speech_engine(request)

        else:

            raise TypeError(
                "Configured speech provider does not provide "
                "a supported speech-to-text interface."
            )

        if not isinstance(
            result,
            SpeechResult,
        ):

            raise TypeError(
                "Speech provider must return SpeechResult."
            )

        return result

    # =====================================================
    # 🔊 TEXT-TO-SPEECH
    # =====================================================

    def text_to_speech(
        self,
        text: str,
        language_code: str,
    ) -> SpeechResult:
        """
        Convert text into speech/audio.

        The actual speech provider is injected separately.
        """

        if self.speech_engine is None:
            raise RuntimeError(
                "No speech provider is configured."
            )

        request = LanguageRequest(
            text=text,
            target_language=language_code,
            operation="text_to_speech",
        )

        if hasattr(
            self.speech_engine,
            "text_to_speech",
        ):

            result = self.speech_engine.text_to_speech(
                request
            )

        elif callable(self.speech_engine):

            result = self.speech_engine(request)

        else:

            raise TypeError(
                "Configured speech provider does not provide "
                "a supported text-to-speech interface."
            )

        if not isinstance(
            result,
            SpeechResult,
        ):

            raise TypeError(
                "Speech provider must return SpeechResult."
            )

        return result

    # =====================================================
    # 🔎 MULTILINGUAL SEARCH
    # =====================================================

    def search(
        self,
        query: str,
        language_code: Optional[str] = None,
    ) -> LanguageSearchResult:
        """
        Perform multilingual search through the configured
        search engine.
        """

        if self.search_engine is None:
            raise RuntimeError(
                "No search provider is configured."
            )

        request = LanguageRequest(
            text=query,
            source_language=language_code,
            operation="search",
        )

        if hasattr(
            self.search_engine,
            "search",
        ):

            result = self.search_engine.search(
                request
            )

        elif callable(self.search_engine):

            result = self.search_engine(request)

        else:

            raise TypeError(
                "Configured search provider does not provide "
                "a supported search interface."
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
    # 🌐 REGISTER HUMAN LANGUAGE
    # =====================================================

    def register_human_language(
        self,
        language: Any,
    ) -> None:
        """
        Register a human language in the global registry.
        """

        self.registry.register_human_language(
            language
        )

    # =====================================================
    # 💻 REGISTER PROGRAMMING LANGUAGE
    # =====================================================

    def register_programming_language(
        self,
        language: Any,
    ) -> None:
        """
        Register a programming language in the registry.
        """

        self.registry.register_programming_language(
            language
        )

    # =====================================================
    # 📊 ENGINE STATUS
    # =====================================================

    def status(self) -> Dict[str, Any]:
        """
        Return the current Language Engine status.
        """

        return {
            "engine": "language",
            "human_languages": (
                self.registry.human_language_count()
            ),
            "programming_languages": (
                self.registry.programming_language_count()
            ),
            "detection": True,
            "translation": (
                self.translator is not None
            ),
            "transliteration": (
                self.transliterator is not None
            ),
            "speech": (
                self.speech_engine is not None
            ),
            "search": (
                self.search_engine is not None
            ),
        }


# =========================================================
# 🌍 DEFAULT LANGUAGE ENGINE
# =========================================================

DEFAULT_LANGUAGE_ENGINE = LanguageEngineManager()


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "LanguageEngineManager",
    "DEFAULT_LANGUAGE_ENGINE",
]
