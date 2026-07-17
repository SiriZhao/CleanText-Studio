import platform

from PySide6.QtGui import QFont, QFontDatabase


class FontManager:
    def __init__(self, families: set[str] | None = None, locale: str = "en_US") -> None:
        self.families = families if families is not None else set(QFontDatabase.families())
        self.locale = locale

    def ui_family(self) -> str:
        locale_candidates = {
            "zh_CN": ["Noto Sans CJK SC", "Microsoft YaHei UI", "Microsoft YaHei", "Segoe UI"],
            "zh_TW": ["Noto Sans CJK TC", "Microsoft JhengHei UI", "Microsoft JhengHei", "Segoe UI"],
            "ja_JP": ["Noto Sans CJK JP", "Yu Gothic UI", "Meiryo UI", "Segoe UI"],
            "ko_KR": ["Noto Sans CJK KR", "Malgun Gothic", "Segoe UI"],
            "ar": ["Noto Sans Arabic", "Segoe UI", "Arial"],
            "hi_IN": ["Noto Sans Devanagari", "Nirmala UI", "Segoe UI"],
        }
        candidates = locale_candidates.get(self.locale, (
            ["PingFang SC", "SF Pro Text", "Helvetica Neue"]
            if platform.system() == "Darwin"
            else [
                "Noto Sans",
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
