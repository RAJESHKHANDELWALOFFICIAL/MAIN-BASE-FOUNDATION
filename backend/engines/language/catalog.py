"""
Language Engine — Global Language Catalog

MAIN BASE FOUNDATION

Global catalog of:

- Human languages
- Programming languages

This module contains language definitions only.
It does not implement translation, speech, detection,
or search providers.

The catalog can be loaded into LanguageRegistry.
"""

from typing import List

from .models import (
    LanguageDefinition,
    ProgrammingLanguageDefinition,
)

from .registry import (
    LanguageRegistry,
)


# =========================================================
# 🌍 HUMAN LANGUAGE CATALOG
# =========================================================

HUMAN_LANGUAGES: List[LanguageDefinition] = [

    LanguageDefinition(
        code="en",
        name="English",
        native_name="English",
        scripts=["Latin"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="en-US",
    ),

    LanguageDefinition(
        code="hi",
        name="Hindi",
        native_name="हिन्दी",
        scripts=["Devanagari"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="hi-IN",
    ),

    LanguageDefinition(
        code="bn",
        name="Bengali",
        native_name="বাংলা",
        scripts=["Bengali"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="bn-IN",
    ),

    LanguageDefinition(
        code="gu",
        name="Gujarati",
        native_name="ગુજરાતી",
        scripts=["Gujarati"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="gu-IN",
    ),

    LanguageDefinition(
        code="mr",
        name="Marathi",
        native_name="मराठी",
        scripts=["Devanagari"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="mr-IN",
    ),

    LanguageDefinition(
        code="pa",
        name="Punjabi",
        native_name="ਪੰਜਾਬੀ",
        scripts=["Gurmukhi"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="pa-IN",
    ),

    LanguageDefinition(
        code="ta",
        name="Tamil",
        native_name="தமிழ்",
        scripts=["Tamil"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="ta-IN",
    ),

    LanguageDefinition(
        code="te",
        name="Telugu",
        native_name="తెలుగు",
        scripts=["Telugu"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="te-IN",
    ),

    LanguageDefinition(
        code="kn",
        name="Kannada",
        native_name="ಕನ್ನಡ",
        scripts=["Kannada"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="kn-IN",
    ),

    LanguageDefinition(
        code="ml",
        name="Malayalam",
        native_name="മലയാളം",
        scripts=["Malayalam"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="ml-IN",
    ),

    LanguageDefinition(
        code="ur",
        name="Urdu",
        native_name="اردو",
        scripts=["Arabic"],
        direction="rtl",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="ur-PK",
    ),

    LanguageDefinition(
        code="sa",
        name="Sanskrit",
        native_name="संस्कृतम्",
        scripts=["Devanagari"],
        direction="ltr",
        speech_to_text=False,
        text_to_speech=False,
        translation=True,
        transliteration=True,
        search=True,
        locale="sa-IN",
    ),

    LanguageDefinition(
        code="ar",
        name="Arabic",
        native_name="العربية",
        scripts=["Arabic"],
        direction="rtl",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="ar-SA",
    ),

    LanguageDefinition(
        code="zh",
        name="Chinese",
        native_name="中文",
        scripts=["Han"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="zh-CN",
    ),

    LanguageDefinition(
        code="ja",
        name="Japanese",
        native_name="日本語",
        scripts=["Hiragana", "Katakana", "Han"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="ja-JP",
    ),

    LanguageDefinition(
        code="ko",
        name="Korean",
        native_name="한국어",
        scripts=["Hangul", "Han"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="ko-KR",
    ),

    LanguageDefinition(
        code="es",
        name="Spanish",
        native_name="Español",
        scripts=["Latin"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="es-ES",
    ),

    LanguageDefinition(
        code="fr",
        name="French",
        native_name="Français",
        scripts=["Latin"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="fr-FR",
    ),

    LanguageDefinition(
        code="de",
        name="German",
        native_name="Deutsch",
        scripts=["Latin"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="de-DE",
    ),

    LanguageDefinition(
        code="pt",
        name="Portuguese",
        native_name="Português",
        scripts=["Latin"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="pt-BR",
    ),

    LanguageDefinition(
        code="ru",
        name="Russian",
        native_name="Русский",
        scripts=["Cyrillic"],
        direction="ltr",
        speech_to_text=True,
        text_to_speech=True,
        translation=True,
        transliteration=True,
        search=True,
        locale="ru-RU",
    ),
]


# =========================================================
# 💻 PROGRAMMING LANGUAGE CATALOG
# =========================================================

PROGRAMMING_LANGUAGES: List[
    ProgrammingLanguageDefinition
] = [

    ProgrammingLanguageDefinition(
        key="python",
        name="Python",
        extensions=[".py", ".pyw"],
        aliases=["py"],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="javascript",
        name="JavaScript",
        extensions=[".js", ".mjs", ".cjs"],
        aliases=["js"],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="typescript",
        name="TypeScript",
        extensions=[".ts", ".mts", ".cts"],
        aliases=["ts"],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="java",
        name="Java",
        extensions=[".java"],
        aliases=[],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="c",
        name="C",
        extensions=[".c", ".h"],
        aliases=[],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="cpp",
        name="C++",
        extensions=[".cpp", ".cc", ".cxx", ".hpp"],
        aliases=["c++"],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="csharp",
        name="C#",
        extensions=[".cs"],
        aliases=["c#", "csharp"],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="go",
        name="Go",
        extensions=[".go"],
        aliases=["golang"],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="rust",
        name="Rust",
        extensions=[".rs"],
        aliases=[],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="php",
        name="PHP",
        extensions=[".php"],
        aliases=[],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="ruby",
        name="Ruby",
        extensions=[".rb"],
        aliases=[],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="swift",
        name="Swift",
        extensions=[".swift"],
        aliases=[],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="kotlin",
        name="Kotlin",
        extensions=[".kt", ".kts"],
        aliases=[],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="dart",
        name="Dart",
        extensions=[".dart"],
        aliases=[],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="r",
        name="R",
        extensions=[".r", ".R"],
        aliases=["r-lang"],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="sql",
        name="SQL",
        extensions=[".sql"],
        aliases=[],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="html",
        name="HTML",
        extensions=[".html", ".htm"],
        aliases=["html5"],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="css",
        name="CSS",
        extensions=[".css"],
        aliases=["css3"],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="shell",
        name="Shell",
        extensions=[".sh", ".bash"],
        aliases=["bash", "shell-script"],
        syntax_highlighting=True,
        code_search=True,
    ),

    ProgrammingLanguageDefinition(
        key="powershell",
        name="PowerShell",
        extensions=[".ps1", ".psm1"],
        aliases=["ps", "pwsh"],
        syntax_highlighting=True,
        code_search=True,
    ),
]


# =========================================================
# 🌍 LOAD HUMAN LANGUAGES
# =========================================================

def load_human_languages(
    registry: LanguageRegistry,
) -> int:
    """
    Load the human-language catalog into a registry.

    Returns the number of newly registered languages.
    """

    count = 0

    for language in HUMAN_LANGUAGES:

        if registry.has_language(
            language.code
        ):
            continue

        registry.register_language(
            language
        )

        count += 1

    return count


# =========================================================
# 💻 LOAD PROGRAMMING LANGUAGES
# =========================================================

def load_programming_languages(
    registry: LanguageRegistry,
) -> int:
    """
    Load the programming-language catalog
    into a registry.

    Returns the number of newly registered languages.
    """

    count = 0

    for language in PROGRAMMING_LANGUAGES:

        if registry.has_programming_language(
            language.key
        ):
            continue

        registry.register_programming_language(
            language
        )

        count += 1

    return count


# =========================================================
# 🌐 LOAD COMPLETE GLOBAL CATALOG
# =========================================================

def load_global_language_catalog(
    registry: LanguageRegistry,
) -> Dict[str, int]:
    """
    Load both human and programming languages
    into the supplied registry.
    """

    human_count = load_human_languages(
        registry
    )

    programming_count = (
        load_programming_languages(
            registry
        )
    )

    return {
        "human_languages": human_count,
        "programming_languages": programming_count,
    }


# =========================================================
# 📊 CATALOG COUNTS
# =========================================================

def catalog_status() -> dict:
    """
    Return static catalog statistics.
    """

    return {
        "human_languages": len(
            HUMAN_LANGUAGES
        ),
        "programming_languages": len(
            PROGRAMMING_LANGUAGES
        ),
    }


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "HUMAN_LANGUAGES",
    "PROGRAMMING_LANGUAGES",
    "load_human_languages",
    "load_programming_languages",
    "load_global_language_catalog",
    "catalog_status",
]
