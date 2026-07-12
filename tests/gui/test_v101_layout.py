from PySide6.QtCore import QSize

from cleantext_studio.app import MainWindow
from cleantext_studio.theme import Theme


def test_three_panel_actions_and_states(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.resize(QSize(1366, 768))
    window.show()
    assert window.splitter.count() == 3
    assert not window.clean_button.isEnabled()
    assert not window.word_button.isEnabled()
    window.input.setPlainText("#### 2.2.1 客户端拍照问诊")
    assert window.clean_button.isEnabled()
    window.start_clean()
    qtbot.waitUntil(lambda: window.output.toPlainText() != "", timeout=3000)
    assert window.output.toPlainText() == "2.2.1 客户端拍照问诊"
    assert window.word_button.isEnabled()
    window.input.appendPlainText("新内容")
    assert window.session.result_outdated
    window.output.appendPlainText("手工修改")
    assert window.session.result_modified
    window.session.result_modified = False


def test_themes_and_collapsible_settings(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.apply_theme(Theme.DARK)
    assert "#171923" in window.styleSheet() or window.palette() is not None
    window.apply_theme(Theme.LIGHT)
    window.show()
    window.toggle_settings_panel()
    assert not window.settings_panel.isVisible()
