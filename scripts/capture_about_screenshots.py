"""Capture the real structured About dialog in the required locales."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QApplication

from cleantext_studio.about_dialog import AboutDialog
from cleantext_studio.i18n import I18nService
from cleantext_studio.theme import Theme, stylesheet

OUTPUT = Path("assets/screenshots/v1.5.0")
SHOTS = {"zh_CN": "about-zh-cn.png", "en_US": "about-en.png", "ja_JP": "about-ja.png", "es_ES": "about-es.png"}


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    app.setStyleSheet(stylesheet(Theme.DARK))
    service = I18nService()
    for locale, filename in SHOTS.items():
        service.set_language(locale)
        dialog = AboutDialog(service)
        dialog.show()
        app.processEvents()
        if not dialog.grab().save(str(OUTPUT / filename), "PNG"):
            raise RuntimeError(f"Could not save {filename}")
        dialog.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
