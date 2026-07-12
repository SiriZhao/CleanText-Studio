import platform

from PySide6.QtGui import QFont, QFontDatabase


class FontManager:
    def __init__(self, families: set[str] | None = None) -> None:
        self.families = families if families is not None else set(QFontDatabase.families())

    def ui_family(self) -> str:
        candidates = (
            ["PingFang SC", "SF Pro Text", "Helvetica Neue"]
            if platform.system() == "Darwin"
            else [
                "HarmonyOS Sans SC",
                "HarmonyOS Sans",
                "Microsoft YaHei UI",
                "Microsoft YaHei",
                "Segoe UI",
            ]
        )
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
