"""Capture privacy-safe v1.4.2 shell screenshots from the real Qt application."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from cleantext_studio.app import MainWindow
from cleantext_studio.theme import Theme

OUTPUT = Path("assets/screenshots/v1.4.2")
SAMPLE = "# Project background\n\nCleanText Studio keeps text processing on this device."


def capture(window: MainWindow, name: str, app: QApplication) -> None:
    window.show()
    app.processEvents()
    if not window.grab().save(str(OUTPUT / name), "PNG"):
        raise RuntimeError(f"could not write {name}")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.resize(1440, 900)
    window.input.setPlainText(SAMPLE)
    for code, name in (("zh_CN", "main-zh-cn.png"), ("en_US", "main-en.png"), ("es_ES", "main-es.png"), ("ja_JP", "main-ja.png"), ("ar", "main-ar-rtl.png")):
        window.i18n.set_language(code)
        capture(window, name, app)
    window.apply_theme(Theme.DARK)
    capture(window, "main-dark.png", app)
    window.close()


if __name__ == "__main__":
    main()
