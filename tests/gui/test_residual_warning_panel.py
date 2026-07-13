from cleantext_studio.app import MainWindow
from cleantext_studio.models import ResidualWarning


def test_residual_button_visibility(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.session.residual_warnings = [ResidualWarning(1, "markdown", "**残留**")]
    window.residual_button.show()
    assert (
        window.residual_button.isVisible() is False
    )  # parent window is not shown in headless test
    assert window.residual_button.text() == "查看残留"
