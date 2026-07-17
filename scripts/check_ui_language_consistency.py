"""Exercise live language changes without changing cleaning data or options."""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from cleantext_studio.app import MainWindow


def main() -> int:
    app = QApplication.instance() or QApplication([])
    settings = QSettings("CleanText Studio", "CleanText Studio")
    original = settings.value("language")
    try:
        window = MainWindow()
        original_source = "# Stable input\n\nText"
        original_result = "Stable result"
        window.input.setPlainText(original_source)
        window.output.setPlainText(original_result)
        for code in ("zh_CN", "en_US", "es_ES", "ja_JP", "ar"):
            window.i18n.set_language(code)
            if window.input.toPlainText() != original_source or window.output.toPlainText() != original_result:
                raise SystemExit(f"language switch changed document state for {code}")
            if window.result_mode.currentData() not in {"text", "preview"}:
                raise SystemExit(f"result mode lost stable data for {code}")
        window.close()
    finally:
        settings.setValue("language", original if original is not None else "system")
    app.processEvents()
    print("UI language consistency OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
