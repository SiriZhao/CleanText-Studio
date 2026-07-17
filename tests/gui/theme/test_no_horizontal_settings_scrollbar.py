"""The settings surface must not create a bottom rectangular scrollbar."""

from PySide6.QtCore import Qt

from cleantext_studio.app import MainWindow


def test_settings_scrollbar_is_vertically_only(qtbot: object) -> None:
    window = MainWindow()
    qtbot.addWidget(window)  # type: ignore[attr-defined]
    assert window.settings_scroll.horizontalScrollBarPolicy() == Qt.ScrollBarPolicy.ScrollBarAlwaysOff
