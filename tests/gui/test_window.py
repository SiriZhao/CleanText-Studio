from cleantext_studio.app import MainWindow


def test_window_clean(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.input.setPlainText("## 标题\n✅ 正文")
    window.start_clean()
    qtbot.waitUntil(lambda: bool(window.output.toPlainText()), timeout=3000)
    assert window.output.toPlainText() == "标题\n\n正文"
