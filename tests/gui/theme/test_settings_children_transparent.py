"""Regression coverage for transparent settings containers."""

from cleantext_studio.theme import Theme, stylesheet


def test_settings_content_matches_its_card_and_hides_the_viewport_edge() -> None:
    css = stylesheet(Theme.LIGHT)
    assert "QScrollArea#settingsScrollView, QScrollArea#settingsScrollView::viewport" in css
    assert "QScrollArea#settingsScrollView::viewport" in css
    assert "QScrollArea::viewport, QAbstractScrollArea::viewport" in css
    assert "background:transparent; border:0;" in css
