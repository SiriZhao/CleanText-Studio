from cleantext_studio.app import MainWindow


def test_ai_button_exists_without_provider(qtbot, monkeypatch) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.output.setPlainText("本地结果")
    monkeypatch.setattr(window.provider_store, "load", lambda: [])
    assert window.ai_button.text() == window.tr("action.ai")
    assert window.output.toPlainText() == "本地结果"


def test_api_key_field_is_hidden(qtbot) -> None:
    from PySide6.QtWidgets import QLineEdit

    from cleantext_studio.ai_dialogs import ProviderDialog

    dialog = ProviderDialog()
    qtbot.addWidget(dialog)
    assert dialog.api_key.echoMode() == QLineEdit.EchoMode.Password
