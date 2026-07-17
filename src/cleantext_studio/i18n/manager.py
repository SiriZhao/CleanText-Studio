"""Dependency-free localization layer used by the Qt interface."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PySide6.QtCore import QLocale, QObject, QSettings, Qt, Signal


@dataclass(frozen=True, slots=True)
class Language:
    code: str
    native_name: str
    rtl: bool = False


LANGUAGES: tuple[Language, ...] = (
    Language("system", "Follow system"), Language("zh_CN", "简体中文"),
    Language("zh_TW", "繁體中文"), Language("en_US", "English"),
    Language("ja_JP", "日本語"), Language("ko_KR", "한국어"),
    Language("es_ES", "Español"), Language("fr_FR", "Français"),
    Language("de_DE", "Deutsch"), Language("pt_BR", "Português (Brasil)"),
    Language("ru_RU", "Русский"), Language("ar", "العربية", True), Language("hi_IN", "हिन्दी"),
)

# These late-added keys remain in the localization layer rather than in widget
# code.  Catalog contributors can move them into every JSON resource without
# changing the public key names.
RUNTIME_LABELS: dict[str, dict[str, str]] = {
    "en_US": {
        "tip.detect_math": "Detect LaTeX, Unicode, and common equations before text cleaning.",
        "tip.protect_math": "Protect delimiters, subscripts, and commands before Markdown cleaning.",
        "tip.normalize_math": "Fix only clear formula spacing; never calculate or rewrite math.",
        "tip.repair_math": "Repair a formula delimiter only when the correction is unambiguous.",
        "tip.word_omml": "Convert supported formulas to native Word equations; complex formulas use a safe fallback.",
        "tip.math_output": "Choose how formulas are represented in cleaned text and TXT output.",
    },
    "zh_CN": {
        "tip.detect_math": "在文本清洗前识别 LaTeX、Unicode 和常见方程式。",
        "tip.protect_math": "在 Markdown 清理前保护公式定界符、下标和命令。",
        "tip.normalize_math": "仅修复明确的公式空格，不计算或改写数学含义。",
        "tip.repair_math": "仅在修复结果明确时调整公式定界符。",
        "tip.word_omml": "将支持的公式转换为 Word 原生公式；复杂公式使用安全回退。",
        "tip.math_output": "选择清洗结果和 TXT 中的公式表示方式。",
    },
    "es_ES": {
        "tip.detect_math": "Detecta LaTeX, Unicode y ecuaciones comunes antes de limpiar el texto.",
        "tip.protect_math": "Protege delimitadores, subíndices y comandos antes de limpiar Markdown.",
        "tip.normalize_math": "Corrige solo espacios claros; no calcula ni reescribe matemáticas.",
        "tip.repair_math": "Repara un delimitador solo cuando la corrección es inequívoca.",
        "tip.word_omml": "Convierte fórmulas compatibles en ecuaciones nativas de Word.",
        "tip.math_output": "Elige cómo se representan las fórmulas en el texto y TXT.",
    },
}


class LocaleFormatter:
    """Formats UI-only quantities without changing user text."""
    def __init__(self, locale: QLocale) -> None:
        self.locale = locale

    def count(self, value: int) -> str:
        return self.locale.toString(value)

    def milliseconds(self, value: float) -> str:
        return self.locale.toString(value, "f", 1)


class I18nManager(QObject):
    """Loads catalogs, detects system locale and signals live UI updates."""
    language_changed = Signal(str)

    def __init__(self, settings: QSettings | None = None) -> None:
        super().__init__()
        self.settings = settings or QSettings("CleanText Studio", "CleanText Studio")
        self._catalogs = self._load_catalogs()
        self._preference = str(self.settings.value("language", "system"))
        self._active = self.resolve(self._preference)

    @property
    def active(self) -> str:
        return self._active
    @property
    def preference(self) -> str:
        return self._preference
    @property
    def locale(self) -> QLocale:
        return QLocale(self._active)
    @property
    def formatter(self) -> LocaleFormatter:
        return LocaleFormatter(self.locale)

    def languages(self) -> tuple[Language, ...]:
        return LANGUAGES

    def resolve(self, code: str) -> str:
        if code != "system" and code in self._catalogs:
            return code
        system = QLocale.system().name()
        if system in self._catalogs:
            return system
        aliases = {
            "zh_SG": "zh_CN",
            "zh_MY": "zh_CN",
            "zh_HK": "zh_TW",
            "zh_MO": "zh_TW",
            "en_GB": "en_US",
            "en_AU": "en_US",
            "pt_PT": "pt_BR",
        }
        if system in aliases:
            return aliases[system]
        prefix = system.split("_", 1)[0]
        return next((item for item in self._catalogs if item.split("_", 1)[0] == prefix), "en_US")

    def set_language(self, code: str) -> None:
        if code not in {item.code for item in LANGUAGES}:
            code = "system"
        self._preference = code
        self.settings.setValue("language", code)
        active = self.resolve(code)
        if active != self._active or code == "system":
            self._active = active
            self.language_changed.emit(active)

    def tr(self, key: str, /, **values: Any) -> str:  # type: ignore[override]
        fallback = self._catalogs["en_US"]
        catalog = self._catalogs.get(self._active, fallback)
        value = str(catalog.get(key, fallback.get(key, key)))
        if "count" in values:
            plural_key = f"{key}.one" if int(values["count"]) == 1 else f"{key}.other"
            value = str(catalog.get(plural_key, fallback.get(plural_key, value)))
        return value.format(**values)

    def direction(self) -> Qt.LayoutDirection:
        return Qt.LayoutDirection.RightToLeft if self._active == "ar" else Qt.LayoutDirection.LeftToRight

    @staticmethod
    def _resource_directory() -> Path:
        return Path(__file__).with_name("translations")
    def _load_catalogs(self) -> dict[str, dict[str, str]]:
        catalogs = {
            file.stem: json.loads(file.read_text(encoding="utf-8"))
            for file in self._resource_directory().glob("*.json")
        }
        if "en_US" not in catalogs:
            raise RuntimeError("The English translation catalog is required")
        for code, labels in RUNTIME_LABELS.items():
            catalogs.setdefault(code, {}).update(labels)
        baseline = catalogs["en_US"]
        for code, catalog in tuple(catalogs.items()):
            if code == "en_US":
                continue
            catalogs[code] = {**baseline, **catalog}
        return catalogs
