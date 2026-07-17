"""Capture the real UI surfaces used to review the v1.5.1 background fix.

The output stays in ``dist/verification`` so it is evidence for this change,
not product documentation or a committed release asset.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPoint, QRect
from PySide6.QtWidgets import QApplication, QWidget

from cleantext_studio.app import MainWindow
from cleantext_studio.theme import Theme

OUTPUT = Path("dist/verification/ui-background-fix")
SAMPLE = """# Public sample

**CleanText Studio** removes copied formatting while retaining structure.

| Item | Result |
| --- | --- |
| Table | Preserved |

$E = mc^2$"""


def _capture(window: MainWindow, name: str, rect: QRect | None = None) -> None:
    image = window.grab()
    if rect is not None:
        # QWidget geometry is device-independent; grabbed pixels are DPI-scaled.
        scale_x = image.width() / max(1, window.width())
        scale_y = image.height() / max(1, window.height())
        rect = QRect(
            round(rect.x() * scale_x),
            round(rect.y() * scale_y),
            round(rect.width() * scale_x),
            round(rect.height() * scale_y),
        )
        image = image.copy(rect)
    if not image.save(str(OUTPUT / name), "PNG"):
        raise RuntimeError(f"Could not write {name}")


def _window_rect(window: MainWindow, widget: QWidget, padding: int = 12) -> QRect:
    origin = widget.mapTo(window, QPoint(0, 0))
    return QRect(origin, widget.size()).adjusted(-padding, -padding, padding, padding)


def _populate(window: MainWindow, app: QApplication) -> None:
    window.input.setPlainText(SAMPLE)
    window.start_clean()
    while window.worker is not None and window.worker.isRunning():
        app.processEvents()
    app.processEvents()


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.resize(1440, 900)
    window.show()
    app.processEvents()
    _populate(window, app)
    display_mode_toolbar = window.findChild(QWidget, "displayModeToolbar")
    if display_mode_toolbar is None:
        raise RuntimeError("Display-mode toolbar is missing from the real main window")

    for theme, suffix in ((Theme.LIGHT, "light"), (Theme.DARK, "dark")):
        window.apply_theme(theme)
        window.settings_scroll.verticalScrollBar().setValue(
            window.settings_scroll.verticalScrollBar().maximum()
        )
        app.processEvents()
        _capture(window, f"main-{suffix}.png")
        _capture(window, f"settings-{suffix}.png", _window_rect(window, window.settings_panel))
        _capture(
            window,
            f"display-mode-{suffix}.png",
            _window_rect(window, display_mode_toolbar),
        )
        window.settings_scroll.verticalScrollBar().setValue(0)
        app.processEvents()
        _capture(window, f"checkbox-section-{suffix}.png", _window_rect(window, window.settings_scroll))
        _capture(
            window,
            f"status-area-{suffix}.png",
            QRect(0, max(0, window.height() - 110), window.width(), 110),
        )

    window.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
