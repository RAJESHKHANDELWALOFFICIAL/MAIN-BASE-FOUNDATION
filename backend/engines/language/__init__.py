"""
Language Engine

MAIN BASE FOUNDATION

Global human-language and programming-language
foundation.

Public interface for the Language Engine package.
"""

# =========================================================
# 🌍 DATA MODELS
# =========================================================

from .models import (
    LanguageDefinition,
    ProgrammingLanguageDefinition,
    LanguageDetectionResult,
    LanguageRequest,
    TranslationResult,
    TransliterationResult,
    SpeechResult,
    LanguageSearchResult,
    LanguageCapability,
)


# =========================================================
# 🔎 LANGUAGE DETECTION
# =========================================================

from .detection import (
    DetectionProvider,
    LanguageDetectionService,
    NullDetectionProvider,
    DEFAULT_DETECTION_SERVICE,
)


# =========================================================
# 🔄 TRANSLATION
# =========================================================

from .translation import (
    TranslationProvider,
    TranslationService,
    NullTranslationProvider,
    DEFAULT_TRANSLATION_SERVICE,
)


# =========================================================
# ✍️ TRANSLITERATION
# =========================================================

from .transliteration import (
    TransliterationProvider,
    TransliterationService,
    NullTransliterationProvider,
    DEFAULT_TRANSLITERATION_SERVICE,
)


# =========================================================
# 🎙️ SPEECH
# =========================================================

from .speech import (
    SpeechToTextProvider,
    TextToSpeechProvider,
    SpeechService,
    NullSpeechToTextProvider,
    NullTextToSpeechProvider,
    DEFAULT_SPEECH_SERVICE,
)


# =========================================================
# 🔎 SEARCH
# =========================================================

from .search import (
    SearchProvider,
    SearchService,
    NullSearchProvider,
    DEFAULT_SEARCH_SERVICE,
)


# =========================================================
# 🌍 REGISTRY
# =========================================================

from .registry import (
    LanguageRegistry,
    DEFAULT_LANGUAGE_REGISTRY,
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [

    # Models
    "LanguageDefinition",
    "ProgrammingLanguageDefinition",
    "LanguageDetectionResult",
    "LanguageRequest",
    "TranslationResult",
    "TransliterationResult",
    "SpeechResult",
    "LanguageSearchResult",
    "LanguageCapability",

    # Detection
    "DetectionProvider",
    "LanguageDetectionService",
    "NullDetectionProvider",
    "DEFAULT_DETECTION_SERVICE",

    # Translation
    "TranslationProvider",
    "TranslationService",
    "NullTranslationProvider",
    "DEFAULT_TRANSLATION_SERVICE",

    # Transliteration
    "TransliterationProvider",
    "TransliterationService",
    "NullTransliterationProvider",
    "DEFAULT_TRANSLITERATION_SERVICE",

    # Speech
    "SpeechToTextProvider",
    "TextToSpeechProvider",
    "SpeechService",
    "NullSpeechToTextProvider",
    "NullTextToSpeechProvider",
    "DEFAULT_SPEECH_SERVICE",

    # Search
    "SearchProvider",
    "SearchService",
    "NullSearchProvider",
    "DEFAULT_SEARCH_SERVICE",

    # Registry
    "LanguageRegistry",
    "DEFAULT_LANGUAGE_REGISTRY",
]
