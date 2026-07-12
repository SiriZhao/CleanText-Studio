from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from cleantext_studio.llm.base import RequestEstimate
from cleantext_studio.llm.models import OptimizationMode, ProviderConfig, ProviderType


class ProviderDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("AI 智能优化配置")
        layout = QFormLayout(self)
        self.name = QLineEdit()
        self.provider = QComboBox()
        self.provider.addItems(
            ["OpenAI", "DeepSeek", "Anthropic Claude", "OpenAI 兼容接口", "本地兼容模型"]
        )
        self.base_url = QLineEdit("https://api.openai.com/v1")
        self.model = QLineEdit()
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.remember = QComboBox()
        self.remember.addItems(["保存至 Windows 凭据库", "仅本次会话使用"])
        for label, widget in (
            ("配置名称", self.name),
            ("提供商", self.provider),
            ("Base URL", self.base_url),
            ("Model", self.model),
            ("API Key", self.api_key),
            ("密钥保存方式", self.remember),
        ):
            layout.addRow(label, widget)
        note = QLabel("测试连接可能产生少量 API 用量。配置导出不包含 API Key。")
        note.setWordWrap(True)
        layout.addRow(note)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def config(self) -> ProviderConfig:
        types = [
            ProviderType.OPENAI,
            ProviderType.DEEPSEEK,
            ProviderType.ANTHROPIC,
            ProviderType.OPENAI_COMPATIBLE,
            ProviderType.LOCAL,
        ]
        return ProviderConfig(
            name=self.name.text(),
            provider_type=types[self.provider.currentIndex()],
            base_url=self.base_url.text(),
            model=self.model.text(),
            timeout=60,
            max_output_tokens=4096,
            temperature=0.1,
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
        details = QLabel(
            f"提供商：{config.provider_type.value}\nBase URL：{config.base_url}\n模型：{config.model}\n发送字符数：{estimate.characters:,}\n预计分块：{estimate.estimated_chunks}\n最大请求数：{estimate.maximum_requests}\n敏感信息：{sensitive or '未检测到'}"
        )
        layout.addWidget(details)
        layout.addWidget(self.mode)
        warning = QLabel(
            "启用后，选定文本将发送至你配置的第三方 API。实际 Token 和费用以提供商账单为准。请勿发送不适合交由第三方处理的内容。"
        )
        warning.setWordWrap(True)
        layout.addWidget(warning)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

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
        buttons = QDialogButtonBox()
        accept = buttons.addButton("接受全部", QDialogButtonBox.ButtonRole.AcceptRole)
        reject = buttons.addButton("放弃全部", QDialogButtonBox.ButtonRole.RejectRole)
        accept.setEnabled(not risky)
        accept.clicked.connect(self.accept)
        reject.clicked.connect(self.reject)
        layout.addWidget(buttons)
