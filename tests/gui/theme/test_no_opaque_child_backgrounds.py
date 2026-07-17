"""Keep app background painting limited to top-level surfaces."""

from cleantext_studio.theme import Theme, stylesheet


def test_global_widget_rule_does_not_paint_an_opaque_surface() -> None:
    css = stylesheet(Theme.DARK)
    assert "QWidget { background:" not in css
    assert "QMainWindow, QDialog, QMessageBox { background:" in css
    assert "QFrame#cardPanel { background:" in css
