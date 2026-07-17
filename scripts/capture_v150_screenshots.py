"""Capture privacy-safe product screenshots from the real v1.5.1 Qt UI."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from cleantext_studio.about_dialog import AboutDialog
from cleantext_studio.app import MainWindow
from cleantext_studio.help_dialog import HelpDialog
from cleantext_studio.theme import Theme

OUTPUT = Path("assets/screenshots/v1.5.0")
SAMPLE = """# Project background

CleanText Studio keeps basic text processing on this device.

| Module | Function |
| --- | --- |
| Structure | Preserve headings and tables |
| Export | Create DOCX and TXT files |

The equation is $E = mc^2$."""


def capture(widget: object, path: Path, app: QApplication) -> None:
    window = widget
    window.show()  # type: ignore[attr-defined]
    app.processEvents()
    if not window.grab().save(str(path), "PNG"):  # type: ignore[attr-defined]
        raise RuntimeError(f"could not write {path}")


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.resize(1440, 900)
    window.input.setPlainText(SAMPLE)
    window.start_clean()
    while window.worker and window.worker.isRunning():
        app.processEvents()
    app.processEvents()
    shots = {
        "en_US": "hero-main-en.png", "zh_CN": "hero-main-zh-cn.png",
        "zh_TW": "main-zh-tw.png", "ja_JP": "main-ja.png", "ko_KR": "main-ko.png",
        "es_ES": "main-es.png", "fr_FR": "main-fr.png", "de_DE": "main-de.png",
        "pt_BR": "main-pt-br.png", "ru_RU": "main-ru.png", "ar": "main-ar-rtl.png",
        "hi_IN": "main-hi.png",
    }
    for locale, name in shots.items():
        window.i18n.set_language(locale)
        capture(window, OUTPUT / name, app)
    window.i18n.set_language("en_US")
    window.apply_theme(Theme.DARK)
    capture(window, OUTPUT / "main-dark-en.png", app)
    window.apply_theme(Theme.LIGHT)
    capture(HelpDialog(window.i18n, window), OUTPUT / "help-en.png", app)
    window.i18n.set_language("zh_CN")
    capture(HelpDialog(window.i18n, window), OUTPUT / "help-zh-cn.png", app)
    capture(AboutDialog(window.i18n, window), OUTPUT / "about-zh-cn.png", app)
    window.i18n.set_language("en_US")
    capture(AboutDialog(window.i18n, window), OUTPUT / "about-en.png", app)
    window.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
