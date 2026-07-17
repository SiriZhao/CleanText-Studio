"""Capture the small, stable v1.5.2 showcase set from the real Qt app.

This deliberately avoids multilingual sample text and complex LaTeX.  Those
cases belong in regression fixtures, not public product screenshots.  The
script uses native Qt rendering so the committed images are real application
captures rather than mockups.
"""

from __future__ import annotations

import time
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QEvent, QRect
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from cleantext_studio.about_dialog import AboutDialog
from cleantext_studio.app import MainWindow
from cleantext_studio.cleaners import clean_text
from cleantext_studio.font_manager import FontManager
from cleantext_studio.models import CleanOptions
from cleantext_studio.theme import Theme

ROOT = Path(__file__).parents[1]
OUTPUT = ROOT / "assets" / "screenshots" / "v1.5.2"
WINDOW_SIZE = (1600, 960)

DEMO_TEXT = """# Project research notes

---

**Goal:** turn copied material into an editable document. ✨

- Keep meaningful headings and lists
- Remove decorative formatting residue

| Area | Export result |
| --- | --- |
| Tables | Native Word table |
| Formula | Editable equation |

https://example.com/reference
"""


def pump(app: QApplication, milliseconds: int = 400) -> None:
    deadline = time.monotonic() + milliseconds / 1_000
    while time.monotonic() < deadline:
        app.processEvents()


def save(window: MainWindow, name: str, app: QApplication) -> None:
    pump(app)
    image = window.grab()
    path = OUTPUT / name
    if not image.save(str(path), "PNG"):
        raise RuntimeError(f"Could not save {path}")


def save_settings_crop(window: MainWindow, app: QApplication) -> None:
    pump(app)
    rect: QRect = window.settings_panel.geometry()
    ratio = window.devicePixelRatioF()
    crop = window.grab().copy(
        int(rect.x() * ratio), int(rect.y() * ratio),
        int(rect.width() * ratio), int(rect.height() * ratio),
    )
    if not crop.save(str(OUTPUT / "07-settings.png"), "PNG"):
        raise RuntimeError("Could not save settings crop")


def clean_demo(window: MainWindow, app: QApplication) -> None:
    window.input.setPlainText(DEMO_TEXT)
    window._cleaned(clean_text(DEMO_TEXT, CleanOptions()))
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    window.result_mode.setCurrentIndex(0)
    pump(app)


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    app.setApplicationName("CleanText Studio")
    app.setFont(FontManager(locale="en_US").application_font())

    window = MainWindow()
    window.resize(*WINDOW_SIZE)
    window.i18n.set_language("en_US")
    window.show()
    clean_demo(window, app)

    window.apply_theme(Theme.LIGHT)
    clean_demo(window, app)
    save(window, "01-main-light.png", app)
    save(window, "03-before-after-light.png", app)
    save_settings_crop(window, app)

    window.result_mode.setCurrentIndex(1)
    pump(app)
    save(window, "05-table-export.png", app)
    window.result_mode.setCurrentIndex(0)
    pump(app)
    save(window, "06-word-export.png", app)

    window.apply_theme(Theme.DARK)
    clean_demo(window, app)
    save(window, "02-main-dark.png", app)
    save(window, "04-before-after-dark.png", app)

    # About is a real dialog invoked from the running application.
    about = AboutDialog(window.i18n, window)
    about.show()
    pump(app)
    dialog: QPixmap = about.grab()
    if not dialog.save(str(OUTPUT / "08-about.png"), "PNG"):
        raise RuntimeError("Could not save About dialog")
    about.hide()
    window.close()
    print(f"Captured 8 v1.5.2 showcase images in {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
