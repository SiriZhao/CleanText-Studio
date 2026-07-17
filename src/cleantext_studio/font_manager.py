import platform

from PySide6.QtGui import QFont, QFontDatabase


class FontManager:
    def __init__(self, families: set[str] | None = None, locale: str = "en_US") -> None:
        self.families = families if families is not None else set(QFontDatabase.families())
        self.locale = locale

    def ui_family(self) -> str:
        locale_candidates = {
            "zh_CN": ["HarmonyOS Sans SC", "Microsoft YaHei UI", "Microsoft YaHei", "Noto Sans CJK SC"],
            "zh_TW": ["Microsoft JhengHei UI", "Microsoft JhengHei", "Noto Sans CJK TC"],
            "ja_JP": ["Yu Gothic UI", "Meiryo UI", "Noto Sans CJK JP"],
            "ko_KR": ["Malgun Gothic", "Noto Sans CJK KR"],
            "ar": ["Segoe UI", "Noto Sans Arabic", "Arial"],
            "hi_IN": ["Nirmala UI", "Noto Sans Devanagari"],
        }
        candidates = locale_candidates.get(self.locale, (
            ["PingFang SC", "SF Pro Text", "Helvetica Neue"]
            if platform.system() == "Darwin"
            else [
                "HarmonyOS Sans SC",
                "HarmonyOS Sans",
                "Microsoft YaHei UI",
                "Microsoft YaHei",
                "Segoe UI",
            ]
        ))
        return next(
            (name for name in candidates if name in self.families),
            QFont().defaultFamily() or "Sans Serif",
        )

    def editor_family(self) -> str:
        return self.ui_family()

    def code_family(self) -> str:
        return next(
            (name for name in ["Cascadia Mono", "Consolas", "Menlo"] if name in self.families),
            QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont).family(),
        )

    def application_font(self) -> QFont:
        font = QFont(self.ui_family())
        font.setPixelSize(14)
        return font
