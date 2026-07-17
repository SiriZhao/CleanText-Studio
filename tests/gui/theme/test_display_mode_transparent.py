"""Display-mode labels must not get their own rectangular panel."""

from cleantext_studio.theme import Theme, stylesheet


def test_display_mode_toolbar_is_a_transparent_layout_surface() -> None:
    css = stylesheet(Theme.DARK)
    assert "QWidget#displayModeToolbar" in css
    assert "QLabel, QCheckBox { background:transparent; }" in css
