from cleantext_studio.app import MainWindow


def test_result_mode_switches_between_editor_and_preview(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.result_mode.setCurrentIndex(1)
    assert window.result_stack.currentWidget() is window.preview
    window.result_mode.setCurrentIndex(0)
    assert window.result_stack.currentWidget() is window.output
