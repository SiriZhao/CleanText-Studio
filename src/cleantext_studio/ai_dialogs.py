from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from cleantext_studio.llm.base import LLMProvider, RequestEstimate
from cleantext_studio.llm.models import OptimizationMode, ProviderConfig
from cleantext_studio.llm.presets import ProviderPreset, all_presets


class ConnectionWorker(QThread):
    succeeded = Signal()
    failed = Signal(str)

    def __init__(self, provider: LLMProvider) -> None:
        super().__init__()
        self.provider = provider

    def run(self) -> None:
        try:
            self.provider.test_connection()
            self.succeeded.emit()
        except Exception as exc:
            self.failed.emit(str(exc))


class ModelWorker(QThread):
    succeeded = Signal(list)
    failed = Signal(str)

    def __init__(self, provider: LLMProvider) -> None:
        super().__init__()
        self.provider = provider

    def run(self) -> None:
        try:
            self.succeeded.emit(self.provider.list_models())
        except Exception as exc:
            self.failed.emit(str(exc))


class ProviderDialog(QDialog):
    def __init__(
        self, parent: QWidget | None = None, existing: ProviderConfig | None = None
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("AI 智能优化配置")
        self.resize(590, 610)
        self.presets = all_presets()
        self._last_preset = self.presets[0]
        self._custom_url = False
        self._worker: ConnectionWorker | None = None
        self._model_worker: ModelWorker | None = None
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)
        title = QLabel("AI 智能优化配置")
        title.setStyleSheet("font-size:18px;font-weight:600")
        root.addWidget(title)
        form = QFormLayout()
        form.setSpacing(12)
        self.name = QLineEdit()
        self.provider = QComboBox()
        self.provider.addItems([p.display_name for p in self.presets])
        self.model = QComboBox()
        self.model.setEditable(True)
        self.fetch_models = QPushButton("获取模型")
        model_row = QHBoxLayout()
        model_row.addWidget(self.model)
        model_row.addWidget(self.fetch_models)
        self.base_url = QLineEdit()
        restore = QPushButton("恢复默认")
        url_row = QHBoxLayout()
        url_row.addWidget(self.base_url)
        url_row.addWidget(restore)
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        show = QCheckBox("显示密钥")
        key_row = QHBoxLayout()
        key_row.addWidget(self.api_key)
        key_row.addWidget(show)
        self.remember = QComboBox()
        self.remember.addItems(["保存至 Windows 凭据管理器", "仅本次会话使用"])
        self.timeout = QSpinBox()
        self.timeout.setRange(5, 600)
        self.timeout.setValue(60)
        self.tokens = QSpinBox()
        self.tokens.setRange(128, 100000)
        self.tokens.setValue(4096)
        self.temperature = QDoubleSpinBox()
        self.temperature.setRange(0, 2)
        self.temperature.setSingleStep(0.1)
        self.temperature.setValue(0.1)
        self.advanced = QCheckBox("显示高级设置")
        self.advanced_box = QWidget()
        advanced_form = QFormLayout(self.advanced_box)
        advanced_form.addRow("请求超时", self.timeout)
        advanced_form.addRow("最大输出 Token", self.tokens)
        advanced_form.addRow("Temperature", self.temperature)
        self.advanced_box.hide()
        form.addRow("配置名称", self.name)
        form.addRow("提供商", self.provider)
        form.addRow("模型", model_row)
        form.addRow("Base URL", url_row)
        form.addRow("API Key", key_row)
        form.addRow("密钥保存方式", self.remember)
        root.addLayout(form)
        root.addWidget(self.advanced)
        root.addWidget(self.advanced_box)
        self.help = QLabel()
        self.help.setWordWrap(True)
        root.addWidget(self.help)
        self.test_button = QPushButton("测试连接")
        root.addWidget(self.test_button)
        buttons = QHBoxLayout()
        buttons.addStretch()
        cancel = QPushButton("取消")
        save = QPushButton("保存配置")
        save.setObjectName("primary")
        buttons.addWidget(cancel)
        buttons.addWidget(save)
        root.addLayout(buttons)
        self.provider.currentIndexChanged.connect(self._provider_changed)
        self.base_url.textEdited.connect(lambda: setattr(self, "_custom_url", True))
        restore.clicked.connect(self.restore_default)
        show.toggled.connect(
            lambda checked: self.api_key.setEchoMode(
                QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
            )
        )
        self.advanced.toggled.connect(self.advanced_box.setVisible)
        cancel.clicked.connect(self.reject)
        save.clicked.connect(self.accept)
        if existing:
            self._load(existing)
        else:
            self._apply_preset(self.presets[0], True)

    def start_connection_test(self, provider: LLMProvider) -> None:
        self.test_button.setText("正在测试……")
        self.test_button.setEnabled(False)
        self._worker = ConnectionWorker(provider)
        self._worker.succeeded.connect(lambda: self._connection_finished("连接成功"))
        self._worker.failed.connect(
            lambda message: self._connection_finished(f"连接失败：{message}")
        )
        self._worker.start()

    def _connection_finished(self, text: str) -> None:
        self.test_button.setText(text)
        self.test_button.setEnabled(True)

    def start_model_fetch(self, provider: LLMProvider) -> None:
        self.fetch_models.setText("正在获取……")
        self.fetch_models.setEnabled(False)
        self._model_worker = ModelWorker(provider)
        self._model_worker.succeeded.connect(self._models_loaded)
        self._model_worker.failed.connect(lambda _: self._models_loaded([]))
        self._model_worker.start()

    def _models_loaded(self, models: list[str]) -> None:
        current = self.model.currentText()
        if models:
            self.model.clear()
            self.model.addItems(models)
            self.model.setEditText(current or models[0])
        self.fetch_models.setText("获取模型")
        self.fetch_models.setEnabled(True)

    def preset(self) -> ProviderPreset:
        return self.presets[self.provider.currentIndex()]

    def _apply_preset(self, preset: ProviderPreset, update_url: bool) -> None:
        if update_url:
            self.base_url.setText(preset.default_base_url)
            self._custom_url = False
        current = self.model.currentText()
        self.model.clear()
        self.model.addItems(preset.default_models)
        self.model.setEditText(
            current
            if current and not update_url
            else (preset.default_models[0] if preset.default_models else "")
        )
        self.api_key.setPlaceholderText("必填" if preset.api_key_required else "可选")
        self.help.setText(f"API 风格：{preset.api_style} · {preset.help_url or '模型名可手动输入'}")
        if not self.name.text() or self.name.text() == f"{self._last_preset.display_name} 默认配置":
            self.name.setText(f"{preset.display_name} 默认配置")
        self._last_preset = preset

    def _provider_changed(self, _: int) -> None:
        self._apply_preset(self.preset(), not self._custom_url)

    def restore_default(self) -> None:
        self._apply_preset(self.preset(), True)

    def _load(self, config: ProviderConfig) -> None:
        index = next(
            (i for i, p in enumerate(self.presets) if p.provider_type == config.provider_type), 0
        )
        self.provider.setCurrentIndex(index)
        self._apply_preset(self.presets[index], True)
        self.name.setText(config.name)
        self.base_url.setText(config.base_url)
        self._custom_url = config.base_url != self.presets[index].default_base_url
        self.model.setEditText(config.model)
        self.timeout.setValue(int(config.timeout))
        self.tokens.setValue(config.max_output_tokens)
        self.temperature.setValue(config.temperature)

    def config(self) -> ProviderConfig:
        preset = self.preset()
        if preset.api_key_required and not self.api_key.text():
            raise ValueError("该提供商需要 API Key")
        return ProviderConfig(
            name=self.name.text() or f"{preset.display_name} 默认配置",
            provider_type=preset.provider_type,
            base_url=self.base_url.text(),
            model=self.model.currentText(),
            timeout=self.timeout.value(),
            max_output_tokens=self.tokens.value(),
            temperature=self.temperature.value(),
        )


class SendConfirmationDialog(QDialog):
    def __init__(
        self,
        config: ProviderConfig,
        estimate: RequestEstimate,
        sensitive: dict[str, int],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("确认 AI 智能优化")
        layout = QVBoxLayout(self)
        self.mode = QComboBox()
        self.mode.addItems(["结构识别", "换行优化", "轻度整理", "列表自然化", "学术和报告结构"])
        layout.addWidget(
            QLabel(
                f"提供商：{config.provider_type.value}\nBase URL：{config.base_url}\n模型：{config.model}\n发送字符数：{estimate.characters:,}\n预计分块：{estimate.estimated_chunks}\n最大请求数：{estimate.maximum_requests}\n敏感信息：{sensitive or '未检测到'}"
            )
        )
        layout.addWidget(self.mode)
        warning = QLabel("启用后，选定文本将发送至你配置的第三方 API。实际费用以提供商账单为准。")
        warning.setWordWrap(True)
        layout.addWidget(warning)
        row = QHBoxLayout()
        cancel = QPushButton("取消")
        confirm = QPushButton("确认发送")
        row.addStretch()
        row.addWidget(cancel)
        row.addWidget(confirm)
        layout.addLayout(row)
        cancel.clicked.connect(self.reject)
        confirm.clicked.connect(self.accept)

    def selected_mode(self) -> OptimizationMode:
        return list(OptimizationMode)[:5][self.mode.currentIndex()]


class AIDiffDialog(QDialog):
    def __init__(
        self, local: str, suggested: str, risky: bool, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("AI 建议差异确认")
        self.resize(1100, 700)
        layout = QVBoxLayout(self)
        if risky:
            layout.addWidget(QLabel("警告：模型报告事实、信息或参考文献变化，请逐段核对。"))
        row = QHBoxLayout()
        left = QPlainTextEdit(local)
        right = QPlainTextEdit(suggested)
        left.setReadOnly(True)
        right.setReadOnly(True)
        row.addWidget(left)
        row.addWidget(right)
        layout.addLayout(row)
        buttons = QHBoxLayout()
        reject = QPushButton("放弃全部")
        accept = QPushButton("接受全部")
        accept.setEnabled(not risky)
        buttons.addStretch()
        buttons.addWidget(reject)
        buttons.addWidget(accept)
        layout.addLayout(buttons)
        accept.clicked.connect(self.accept)
        reject.clicked.connect(self.reject)
