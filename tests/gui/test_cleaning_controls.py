from cleantext_studio.app import MainWindow


def test_deep_preset_enables_instructional_cleaning(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.preset.setCurrentText("深度清洗")
    assert window.clean_instructional.isChecked()
    assert window.url_mode.currentText() == "保留独立 URL"
