"""Report background-affecting properties in the real main-window widget tree."""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget

from cleantext_studio.app import MainWindow


def _stylesheet_summary(widget: QWidget) -> str:
    """Return one readable line without flooding the development audit."""
    stylesheet = " ".join(widget.styleSheet().split())
    if not stylesheet:
        return "-"
    return stylesheet[:117] + "..." if len(stylesheet) > 120 else stylesheet


def main() -> int:
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()
    app.processEvents()
    for widget in [window, *window.findChildren(QWidget)]:
        palette = widget.palette().color(widget.backgroundRole()).name()
        parent = widget.parentWidget()
        if widget.styleSheet() or widget.autoFillBackground() or widget.objectName():
            print(
                f"{type(widget).__name__}\tname={widget.objectName() or '-'}"
                f"\tparent={type(parent).__name__ if parent else '-'}"
                f"\tgeo={widget.geometry().getRect()}\tstylesheet={_stylesheet_summary(widget)}"
                f"\tpalette={palette}\tauto_fill={widget.autoFillBackground()}"
                f"\tstyled={widget.testAttribute(Qt.WidgetAttribute.WA_StyledBackground)}"
            )
    window.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
