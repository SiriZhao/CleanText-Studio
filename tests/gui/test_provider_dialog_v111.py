from cleantext_studio.ai_dialogs import ProviderDialog


def test_provider_url_and_model_linkage(qtbot) -> None:
    dialog = ProviderDialog()
    qtbot.addWidget(dialog)
    dialog.provider.setCurrentText("DeepSeek")
    assert dialog.base_url.text() == "https://api.deepseek.com"
    assert dialog.model.count() > 0
    dialog.provider.setCurrentText("Anthropic Claude")
    assert dialog.base_url.text() == "https://api.anthropic.com"
    dialog.provider.setCurrentText("本地 OpenAI 兼容模型")
    assert dialog.base_url.text() == "http://localhost:11434/v1"


def test_custom_url_and_restore_default(qtbot) -> None:
    dialog = ProviderDialog()
    qtbot.addWidget(dialog)
    dialog.base_url.setText("https://custom.example/v1")
    dialog._custom_url = True
    dialog.provider.setCurrentText("DeepSeek")
    assert dialog.base_url.text() == "https://custom.example/v1"
    dialog.restore_default()
    assert dialog.base_url.text() == "https://api.deepseek.com"


def test_dialog_buttons_are_chinese(qtbot) -> None:
    dialog = ProviderDialog()
    qtbot.addWidget(dialog)
    texts = [button.text() for button in dialog.findChildren(type(dialog.test_button))]
    assert "取消" in texts and "保存配置" in texts and "测试连接" in texts
