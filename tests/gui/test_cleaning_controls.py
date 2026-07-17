from cleantext_studio.app import MainWindow


def test_deep_preset_enables_instructional_cleaning(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.preset.setCurrentIndex(window.preset.findData("deep"))
    assert window.clean_instructional.isChecked()
    assert window.url_mode.currentData() == "preserve"
