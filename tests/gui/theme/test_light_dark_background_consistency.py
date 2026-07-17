"""Both palettes must keep the same transparent internal-surface contract."""

from cleantext_studio.theme import Theme, stylesheet


def test_light_and_dark_keep_internal_containers_consistent() -> None:
    for theme in (Theme.LIGHT, Theme.DARK):
        css = stylesheet(theme)
        assert "QScrollArea#settingsScrollView, QScrollArea#settingsScrollView::viewport" in css
        assert "QWidget#displayModeToolbar" in css
        assert "QLabel, QCheckBox { background:transparent; }" in css
