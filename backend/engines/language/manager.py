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
- Human-language registry
- Programming-language registry

Provider-specific implementations remain isolated from
this manager.
"""

from typing import Any, Dict, Optional

from .detection import (
    LanguageDetectionService,
)

from .models import (
    LanguageDetectionResult,
    LanguageRequest,
    LanguageSearchResult,
    SpeechResult,
    TranslationResult,
    TransliterationResult,
)

from .registry import (
    LanguageRegistry,
)


# =========================================================
# 🌍 LANGUAGE ENGINE MANAGER
# =========================================================

class LanguageEngineManager:
    """
    Central manager for the Global Language Engine.

    Provides one consistent interface for language-related
    operations while keeping providers and services
    independent.
    """

    def __init__(
        self,
        registry: Optional[
            LanguageRegistry
        ] = None,
        detection_service: Optional[
            LanguageDetectionService
        ] = None,
        translator: Optional[Any] = None,
        transliterator: Optional[Any] = None,
        speech_engine: Optional[Any] = None,
        search_engine: Optional[Any] = None,
    ) -> None:

        self.registry = (
            registry
            if registry is not None
            else LanguageRegistry()
        )

        self.detection_service = (
            detection_service
            if detection_service is not None
            else LanguageDetectionService()
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
        Detect language, confidence and script.
        """

        return self.detection_service.detect(
            text
        )

    # =====================================================
    # 🔎 DETECT LANGUAGE CODE
    # =====================================================

    def detect_language(
        self,
        text: str,
    ) -> Optional[str]:
        """
        Return detected language code.
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
        Return language-detection confidence.
        """

        return self.detection_service.detect_confidence(
            text
        )

    # =====================================================
    # 📝 DETECT SCRIPT
    # =====================================================

    def detect_script(
        self,
        text: str,
    ) -> Optional[str]:
        """
        Return detected writing script.
        """

        return self.detection_service.detect_script(
            text
        )

    # =====================================================
    # 🔄 TRANSLATION
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
        Translate text through the configured translator.
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
            metadata=(
                metadata
                if metadata is not None
                else {}
            ),
        )

        if hasattr(
            self.translator,
            "translate_request",
        ):

            result = (
                self.translator.translate_request(
                    request
                )
            )

        elif hasattr(
            self.translator,
            "translate",
        ):

            result = self.translator.translate(
                request
            )

        elif callable(self.translator):

            result = self.translator(
                request
            )

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
                "target_script": target_script,
            },
        )

        if hasattr(
            self.transliterator,
            "transliterate_request",
        ):

            result = (
                self.transliterator
                .transliterate_request(
                    request
                )
            )

        elif hasattr(
            self.transliterator,
            "transliterate",
        ):

            result = (
                self.transliterator.transliterate(
                    request
                )
            )

        elif callable(self.transliterator):

            result = self.transliterator(
                request
            )

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
                "audio_reference": audio_reference,
            },
        )

        if hasattr(
            self.speech_engine,
            "speech_to_text",
        ):

            result = (
                self.speech_engine.speech_to_text(
                    request
                )
            )

        elif callable(self.speech_engine):

            result = self.speech_engine(
                request
            )

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

            result = (
                self.speech_engine.text_to_speech(
                    request
                )
            )

        elif callable(self.speech_engine):

            result = self.speech_engine(
                request
            )

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
        Perform multilingual search.
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
            "search_request",
        ):

            result = (
                self.search_engine.search_request(
                    request
                )
            )

        elif hasattr(
            self.search_engine,
            "search",
        ):

            result = self.search_engine.search(
                request
            )

        elif callable(self.search_engine):

            result = self.search_engine(
                request
            )

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
    # 🌍 REGISTER HUMAN LANGUAGE
    # =====================================================

    def register_human_language(
        self,
        language: Any,
    ) -> None:
        """
        Register a human language.
        """

        self.registry.register_language(
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
        Register a programming language.
        """

        self.registry.register_programming_language(
            language
        )

    # =====================================================
    # 🌍 GET HUMAN LANGUAGE
    # =====================================================

    def get_human_language(
        self,
        language_code: str,
    ) -> Any:
        """
        Retrieve a registered human language.
        """

        return self.registry.get_language(
            language_code
        )

    # =====================================================
    # 💻 GET PROGRAMMING LANGUAGE
    # =====================================================

    def get_programming_language(
        self,
        identifier: str,
    ) -> Any:
        """
        Retrieve a programming language by key,
        alias or extension.
        """

        return (
            self.registry.get_programming_language(
                identifier
            )
        )

    # =====================================================
    # 🌍 LIST HUMAN LANGUAGES
    # =====================================================

    def list_human_languages(
        self,
    ) -> list:
        """
        Return all registered human languages.
        """

        return self.registry.list_languages()

    # =====================================================
    # 💻 LIST PROGRAMMING LANGUAGES
    # =====================================================

    def list_programming_languages(
        self,
    ) -> list:
        """
        Return all registered programming languages.
        """

        return (
            self.registry.list_programming_languages()
        )

    # =====================================================
    # 📊 ENGINE STATUS
    # =====================================================

    def status(
        self,
    ) -> Dict[str, Any]:
        """
        Return complete Language Engine status.
        """

        registry_status = (
            self.registry.status()
        )

        detection_status = (
            self.detection_service.status()
        )

        return {
            "engine": "language",

            "human_languages": (
                registry_status[
                    "human_languages"
                ]
            ),

            "programming_languages": (
                registry_status[
                    "programming_languages"
                ]
            ),

            "detection": detection_status[
                "configured"
            ],

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

DEFAULT_LANGUAGE_ENGINE = (
    LanguageEngineManager()
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "LanguageEngineManager",
    "DEFAULT_LANGUAGE_ENGINE",
]
