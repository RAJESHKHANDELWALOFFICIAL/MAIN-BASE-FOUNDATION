"""
Language Engine — Language Detection

MAIN BASE FOUNDATION

Provides framework-independent language and script detection.

This module does not depend on a specific external AI or
translation provider. Provider-specific detection can be
connected later through the Language Engine.
"""

from collections import Counter
from typing import Dict, List, Optional, Tuple

from .models import LanguageDetectionResult
from .registry import GlobalLanguageRegistry


# =========================================================
# 🌍 SCRIPT DETECTION
# =========================================================

SCRIPT_RANGES: Dict[str, Tuple[int, int]] = {
    "latin": (0x0041, 0x024F),
    "devanagari": (0x0900, 0x097F),
    "bengali": (0x0980, 0x09FF),
    "gurmukhi": (0x0A00, 0x0A7F),
    "gujarati": (0x0A80, 0x0AFF),
    "oriya": (0x0B00, 0x0B7F),
    "tamil": (0x0B80, 0x0BFF),
    "telugu": (0x0C00, 0x0C7F),
    "kannada": (0x0C80, 0x0CFF),
    "malayalam": (0x0D00, 0x0D7F),
    "thai": (0x0E00, 0x0E7F),
    "georgian": (0x10A0, 0x10FF),
    "hebrew": (0x0590, 0x05FF),
    "arabic": (0x0600, 0x06FF),
    "armenian": (0x0530, 0x058F),
    "cyrillic": (0x0400, 0x04FF),
    "greek": (0x0370, 0x03FF),
    "hiragana": (0x3040, 0x309F),
    "katakana": (0x30A0, 0x30FF),
    "hangul": (0xAC00, 0xD7AF),
}


# =========================================================
# 🔤 LANGUAGE SCRIPT MAP
# =========================================================

SCRIPT_LANGUAGE_MAP: Dict[str, List[str]] = {
    "devanagari": [
        "hi",
        "mr",
        "ne",
        "sa",
    ],
    "bengali": [
        "bn",
    ],
    "gurmukhi": [
        "pa",
    ],
    "gujarati": [
        "gu",
    ],
    "oriya": [
        "or",
    ],
    "tamil": [
        "ta",
    ],
    "telugu": [
        "te",
    ],
    "kannada": [
        "kn",
    ],
    "malayalam": [
        "ml",
    ],
    "thai": [
        "th",
    ],
    "hebrew": [
        "he",
    ],
    "arabic": [
        "ar",
        "fa",
        "ur",
    ],
    "cyrillic": [
        "ru",
        "uk",
        "bg",
        "sr",
    ],
    "greek": [
        "el",
    ],
    "hiragana": [
        "ja",
    ],
    "katakana": [
        "ja",
    ],
    "hangul": [
        "ko",
    ],
}


# =========================================================
# 🧠 COMMON LANGUAGE MARKERS
# =========================================================

LANGUAGE_MARKERS: Dict[str, Tuple[str, ...]] = {
    "en": (
        "the",
        "and",
        "is",
        "are",
        "you",
        "this",
        "that",
        "with",
    ),
    "hi": (
        "है",
        "और",
        "का",
        "की",
        "के",
        "में",
        "से",
        "यह",
    ),
    "es": (
        "el",
        "la",
        "los",
        "las",
        "que",
        "una",
        "con",
    ),
    "fr": (
        "le",
        "la",
        "les",
        "des",
        "une",
        "avec",
        "que",
    ),
    "de": (
        "der",
        "die",
        "das",
        "und",
        "ist",
        "ein",
        "mit",
    ),
    "it": (
        "il",
        "la",
        "gli",
        "le",
        "che",
        "una",
        "con",
    ),
    "pt": (
        "o",
        "a",
        "os",
        "as",
        "que",
        "uma",
        "com",
    ),
    "nl": (
        "de",
        "het",
        "een",
        "en",
        "van",
        "met",
    ),
    "tr": (
        "bir",
        "ve",
        "bu",
        "ile",
        "için",
    ),
}


# =========================================================
# 🔎 SCRIPT DETECTOR
# =========================================================

class ScriptDetector:
    """
    Detects the dominant writing script in text.
    """

    def detect(self, text: str) -> Optional[str]:
        """
        Return the dominant detected script.

        Returns None when no supported script can be
        identified.
        """

        if not text or not text.strip():
            return None

        counts: Counter[str] = Counter()

        for character in text:

            codepoint = ord(character)

            for script, (
                start,
                end,
            ) in SCRIPT_RANGES.items():

                if start <= codepoint <= end:

                    counts[script] += 1

                    break

        if not counts:
            return None

        return counts.most_common(1)[0][0]


# =========================================================
# 🌍 LANGUAGE DETECTOR
# =========================================================

class LanguageDetector:
    """
    Detects a likely language from text.

    Detection is intentionally conservative. Without an
    external language-detection model/provider, the engine
    only returns a result when enough evidence is available.
    """

    def __init__(
        self,
        registry: Optional[GlobalLanguageRegistry] = None,
    ) -> None:

        self.registry = registry

        self.script_detector = ScriptDetector()

    # -----------------------------------------------------
    # DETECT
    # -----------------------------------------------------

    def detect(
        self,
        text: str,
    ) -> LanguageDetectionResult:
        """
        Detect the most likely language.

        Returns a standardized LanguageDetectionResult.
        """

        if not isinstance(text, str):
            raise TypeError(
                "Text must be a string."
            )

        cleaned = text.strip()

        if not cleaned:
            return LanguageDetectionResult(
                language_code=None,
                confidence=0.0,
                script=None,
                candidates=[],
            )

        script = self.script_detector.detect(
            cleaned
        )

        candidates: List[str] = []

        # -------------------------------------------------
        # SCRIPT-BASED CANDIDATES
        # -------------------------------------------------

        if script:

            candidates = list(
                SCRIPT_LANGUAGE_MAP.get(
                    script,
                    [],
                )
            )

        # -------------------------------------------------
        # MARKER-BASED DETECTION
        # -------------------------------------------------

        marker_scores: Dict[str, int] = {}

        words = {
            word.strip(
                ".,!?;:\"'()[]{}"
            ).lower()
            for word in cleaned.split()
        }

        for language_code, markers in (
            LANGUAGE_MARKERS.items()
        ):

            score = sum(
                1
                for marker in markers
                if marker.lower() in words
            )

            if score:
                marker_scores[
                    language_code
                ] = score

        if marker_scores:

            sorted_markers = sorted(
                marker_scores.items(),
                key=lambda item: item[1],
                reverse=True,
            )

            marker_candidates = [
                code
                for code, _ in sorted_markers
            ]

            if not candidates:

                candidates = marker_candidates

            else:

                candidates = list(
                    dict.fromkeys(
                        candidates
                        + marker_candidates
                    )
                )

        # -------------------------------------------------
        # DETERMINE RESULT
        # -------------------------------------------------

        if not candidates:

            return LanguageDetectionResult(
                language_code=None,
                confidence=0.0,
                script=script,
                candidates=[],
            )

        selected = candidates[0]

        # Script alone is weak evidence when several
        # languages share the same script.

        if marker_scores:

            score = marker_scores.get(
                selected,
                0,
            )

            confidence = min(
                0.50 + (score * 0.10),
                0.95,
            )

        else:

            confidence = (
                0.60
                if len(candidates) == 1
                else 0.40
            )

        # -------------------------------------------------
        # REGISTRY VALIDATION
        # -------------------------------------------------

        if self.registry:

            if not self.registry.human.exists(
                selected
            ):

                registered_candidates = [
                    code
                    for code in candidates
                    if self.registry.human.exists(
                        code
                    )
                ]

                if registered_candidates:

                    selected = (
                        registered_candidates[0]
                    )

                else:

                    selected = None
                    confidence = 0.0

        return LanguageDetectionResult(
            language_code=selected,
            confidence=confidence,
            script=script,
            candidates=candidates,
        )


# =========================================================
# ⚡ CONVENIENCE FUNCTION
# =========================================================

def detect_language(
    text: str,
    registry: Optional[GlobalLanguageRegistry] = None,
) -> LanguageDetectionResult:
    """
    Convenience function for language detection.
    """

    detector = LanguageDetector(
        registry=registry
    )

    return detector.detect(text)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "SCRIPT_RANGES",
    "SCRIPT_LANGUAGE_MAP",
    "LANGUAGE_MARKERS",
    "ScriptDetector",
    "LanguageDetector",
    "detect_language",
]
