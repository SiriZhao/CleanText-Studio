from cleantext_studio.app import MainWindow
from cleantext_studio.models import MathOutputMode


def test_math_settings_are_enabled_and_bound(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.detect_math.isChecked()
    assert window.protect_math.isChecked()
    assert window.normalize_math.isChecked()
    assert window._options().detect_math is True
    window.math_output_mode.setCurrentIndex(2)
    assert window._options().math_output_mode == MathOutputMode.UNICODE


def test_math_preview_is_structured(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.input.setPlainText("$$\nx^2\n$$")
    window.start_clean()
    window.result_mode.setCurrentIndex(1)
    qtbot.waitUntil(
        lambda: any(
            label.objectName() == "mathPreview"
            for label in window.preview_container.findChildren(type(window.result_notice))
        ),
        timeout=5000,
    )
