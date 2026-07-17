"""Only the real rule-count InfoBar is allowed to paint a status surface."""

from cleantext_studio.theme import Theme, stylesheet


def test_status_labels_are_transparent_but_rule_count_is_rounded_infobar() -> None:
    css = stylesheet(Theme.LIGHT)
    assert "QToolBar, QStatusBar, QSplitter#mainSplitter { background:" in css
    assert "QStatusBar::item { border:0; }" in css
    assert "QLabel#muted { color:" in css
    assert "QLabel#ruleCount { background:" in css
    assert "border-radius:" in css
