"""
Language Engine — Core Data Models

MAIN BASE FOUNDATION
Global human-language and programming-language foundation.

This module contains framework-independent data models only.
Provider-specific translation, speech, detection, and search
implementations belong in their respective engine modules.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# =========================================================
# 🌍 HUMAN LANGUAGE DEFINITION
# =========================================================

@dataclass(frozen=True)
class LanguageDefinition:
    """
    Defines a human language and its supported capabilities.
    """

    code: str
    name: str
    native_name: str

    scripts: List[str] = field(default_factory=list)

    direction: str = "ltr"

    speech_to_text: bool = False
    text_to_speech: bool = False
    translation: bool = False
    transliteration: bool = False
    search: bool = True

    locale: Optional[str] = None

    def __post_init__(self) -> None:
        """
        Validate the language definition.
        """

        if not self.code.strip():
            raise ValueError("Language code cannot be empty.")

        if not self.name.strip():
            raise ValueError("Language name cannot be empty.")

        if not self.native_name.strip():
            raise ValueError("Native language name cannot be empty.")

        if self.direction not in {"ltr", "rtl"}:
            raise ValueError(
                "Language direction must be either 'ltr' or 'rtl'."
            )


# =========================================================
# 💻 PROGRAMMING LANGUAGE DEFINITION
# =========================================================

@dataclass(frozen=True)
class ProgrammingLanguageDefinition:
    """
    Defines a programming language for future code-language
    services such as detection, search and syntax tooling.
    """

    key: str
    name: str

    extensions: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)

    syntax_highlighting: bool = False
    code_search: bool = False

    def __post_init__(self) -> None:
        """
        Validate the programming-language definition.
        """

        if not self.key.strip():
            raise ValueError(
                "Programming language key cannot be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "Programming language name cannot be empty."
            )


# =========================================================
# 🔎 LANGUAGE DETECTION RESULT
# =========================================================

@dataclass(frozen=True)
class LanguageDetectionResult:
    """
    Result produced by a language-detection service.
    """

    language_code: Optional[str]

    confidence: float

    script: Optional[str] = None

    candidates: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Validate detection confidence.
        """

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Detection confidence must be between 0.0 and 1.0."
            )


# =========================================================
# 🗣️ LANGUAGE REQUEST
# =========================================================

@dataclass(frozen=True)
class LanguageRequest:
    """
    Normalized request passed through the Language Engine.
    """

    text: str

    source_language: Optional[str] = None
    target_language: Optional[str] = None

    operation: str = "detect"

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        """
        Validate the language request.
        """

        if not isinstance(self.text, str):
            raise TypeError("Language request text must be a string.")

        if not self.operation.strip():
            raise ValueError(
                "Language operation cannot be empty."
            )


# =========================================================
# 🔄 TRANSLATION RESULT
# =========================================================

@dataclass(frozen=True)
class TranslationResult:
    """
    Standard result returned by a translation service.
    """

    source_text: str
    translated_text: str

    source_language: Optional[str] = None
    target_language: Optional[str] = None

    provider: Optional[str] = None

    confidence: Optional[float] = None

    metadata: Dict[str, str] = field(
        default_factory=dict
    )


# =========================================================
# ✍️ TRANSLITERATION RESULT
# =========================================================

@dataclass(frozen=True)
class TransliterationResult:
    """
    Standard result returned by a transliteration service.
    """

    source_text: str
    transliterated_text: str

    source_language: Optional[str] = None
    target_script: Optional[str] = None

    provider: Optional[str] = None

    metadata: Dict[str, str] = field(
        default_factory=dict
    )


# =========================================================
# 🎙️ SPEECH RESULT
# =========================================================

@dataclass(frozen=True)
class SpeechResult:
    """
    Standard result for speech processing.

    Supports both speech-to-text and text-to-speech
    service metadata without binding the model to a
    particular provider.
    """

    text: Optional[str] = None

    language_code: Optional[str] = None

    audio_reference: Optional[str] = None

    provider: Optional[str] = None

    confidence: Optional[float] = None

    metadata: Dict[str, str] = field(
        default_factory=dict
    )


# =========================================================
# 🔎 SEARCH RESULT
# =========================================================

@dataclass(frozen=True)
class LanguageSearchResult:
    """
    Standard multilingual search result.
    """

    query: str

    language_code: Optional[str] = None

    results: List[Dict[str, str]] = field(
        default_factory=list
    )

    total: int = 0

    metadata: Dict[str, str] = field(
        default_factory=dict
    )


# =========================================================
# 🌐 LANGUAGE CAPABILITY
# =========================================================

@dataclass(frozen=True)
class LanguageCapability:
    """
    Represents a specific capability available for a
    language.
    """

    language_code: str

    speech_to_text: bool = False
    text_to_speech: bool = False
    translation: bool = False
    transliteration: bool = False
    search: bool = True

    def __post_init__(self) -> None:

        if not self.language_code.strip():
            raise ValueError(
                "Language capability code cannot be empty."
            )
