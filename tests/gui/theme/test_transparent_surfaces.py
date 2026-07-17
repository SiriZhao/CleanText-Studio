"""Regression checks for transparent internal presentation containers."""

from __future__ import annotations

from PySide6.QtCore import Qt

from cleantext_studio.app import MainWindow
from cleantext_studio.theme import Theme, stylesheet


def test_settings_scroll_view_has_no_horizontal_scrollbar(qtbot: object) -> None:
    window = MainWindow()
    qtbot.addWidget(window)  # type: ignore[attr-defined]
    scroll = window.findChild(type(window.preview), "settingsScrollView")
    assert scroll is not None
    assert scroll.horizontalScrollBarPolicy() == Qt.ScrollBarPolicy.ScrollBarAlwaysOff


def test_display_mode_and_settings_content_are_transparent(qtbot: object) -> None:
    window = MainWindow()
    qtbot.addWidget(window)  # type: ignore[attr-defined]
    assert window.findChild(type(window.preview_container), "displayModeToolbar") is not None
    assert window.findChild(type(window.preview_container), "settingsContent") is not None


def test_theme_reserves_opaque_surfaces_for_cards_and_controls() -> None:
    css = stylesheet(Theme.DARK)

    assert "QMainWindow, QDialog, QMessageBox { background:" in css
    assert "QWidget { color:" in css
    assert "QWidget { background:" not in css
    assert "QScrollArea#settingsScrollView, QScrollArea#settingsScrollView::viewport" in css
    assert "QScrollArea::viewport, QAbstractScrollArea::viewport" in css
    assert "QLabel, QCheckBox { background:transparent; }" in css
