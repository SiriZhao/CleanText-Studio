from PySide6.QtWidgets import QTableWidget

from cleantext_studio.app import MainWindow


def test_table_automatically_opens_preview(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.input.setPlainText("|模块|功能|\n|-|-|\n|AI识别|病害识别|")
    window.start_clean()
    qtbot.waitUntil(lambda: bool(window.output.toPlainText()), timeout=3000)
    assert window.result_mode.currentText() == "预览模式"
    tables = window.preview.findChildren(QTableWidget)
    assert len(tables) == 1
    assert tables[0].horizontalHeaderItem(0).text() == "模块"
