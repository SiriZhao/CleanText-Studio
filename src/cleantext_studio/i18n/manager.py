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

 # Backwards-compatible source for v1.4 catalogs.  v1.5 writes these keys to
 # every static catalog and no longer uses per-key runtime inheritance.
RUNTIME_LABELS: dict[str, dict[str, str]] = {
    "en_US": {
        "about.title": "About CleanText Studio",
        "about.copy_version": "Copy version information",
        "about.details": "Version: v{version}\nDeveloper: SiriZhao\n\nA local-first text cleanup, document-structure, and Word/TXT formatting tool.\n\nProject homepage: {repository}\n\nCopyright © 2026 SiriZhao. All rights reserved.\nLicense: MIT License\n\nBasic cleanup is performed locally. AI optimization only calls a third-party API that you configure yourself. The app provides no public API key and does not proxy or resell model services.\n\nThis software is for text cleanup, structure recovery, and document layout. It does not provide AI-detection evasion, plagiarism evasion, or academic-misconduct features.",
        "about.license_message": "CleanText Studio is distributed under the MIT License. See the repository LICENSE file for the complete text.",
        "about.open_failed": "Copy this project address: {repository}",
        "tip.detect_math": "Detect LaTeX, Unicode, and common equations before text cleaning.",
        "tip.protect_math": "Protect delimiters, subscripts, and commands before Markdown cleaning.",
        "tip.normalize_math": "Fix only clear formula spacing; never calculate or rewrite math.",
        "tip.repair_math": "Repair a formula delimiter only when the correction is unambiguous.",
        "tip.word_omml": "Convert supported formulas to native Word equations; complex formulas use a safe fallback.",
        "tip.math_output": "Choose how formulas are represented in cleaned text and TXT output.",
    },
    "zh_CN": {
        "about.title": "关于净文排版",
        "about.copy_version": "复制版本信息",
        "about.details": "版本：v{version}\n开发者：SiriZhao\n\n一款本地优先的文本格式清洗、结构整理与 Word/TXT 排版工具。\n\n项目主页：{repository}\n\nCopyright © 2026 SiriZhao. All rights reserved.\n许可证：MIT License\n\n基础清洗完全在本机完成。AI 优化仅在用户主动操作后调用其自行配置的第三方 API。应用不提供公共 API Key，也不代理或转售模型服务。\n\n本软件用于文本格式清理、结构整理和文档排版，不提供规避 AI 检测、绕过查重或实施学术不端的功能。",
        "about.license_message": "净文排版采用 MIT License 发布，完整文本见仓库中的 LICENSE 文件。",
        "about.open_failed": "请复制项目地址：{repository}",
        "tip.detect_math": "在文本清洗前识别 LaTeX、Unicode 和常见方程式。",
        "tip.protect_math": "在 Markdown 清理前保护公式定界符、下标和命令。",
        "tip.normalize_math": "仅修复明确的公式空格，不计算或改写数学含义。",
        "tip.repair_math": "仅在修复结果明确时调整公式定界符。",
        "tip.word_omml": "将支持的公式转换为 Word 原生公式；复杂公式使用安全回退。",
        "tip.math_output": "选择清洗结果和 TXT 中的公式表示方式。",
    },
    "es_ES": {
        "about.title": "Acerca de CleanText Studio",
        "about.copy_version": "Copiar información de versión",
        "about.details": "Versión: v{version}\nDesarrollador: SiriZhao\n\nUna herramienta local para limpiar texto, recuperar estructura y exportar Word/TXT.\n\nProyecto: {repository}\n\nCopyright © 2026 SiriZhao. Todos los derechos reservados.\nLicencia: MIT License\n\nLa limpieza básica se realiza localmente. La optimización con IA usa solo una API de terceros que usted configure.",
        "about.license_message": "CleanText Studio se distribuye bajo la licencia MIT. Consulte LICENSE para el texto completo.",
        "about.open_failed": "Copie esta dirección del proyecto: {repository}",
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
        return catalogs
