import platform

import PySide6
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from cleantext_studio import __version__

REPOSITORY = "https://github.com/SiriZhao/CleanText-Studio"


def version_information() -> str:
    return "\n".join(
        [
            f"CleanText Studio v{__version__}",
            f"Python {platform.python_version()}",
            f"PySide6 {PySide6.__version__}",
            f"Windows {platform.release()}",
            f"架构 {platform.machine()}",
            f"GitHub {REPOSITORY}",
        ]
    )


class AboutDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("关于净文排版")
        self.resize(620, 520)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        title = QLabel("净文排版 · CleanText Studio")
        title.setStyleSheet("font-size:20px;font-weight:600")
        layout.addWidget(title)
        details = QLabel(
            f"版本：v{__version__}\n开发者：SiriZhao\n\n一款本地优先的文本格式清洗、结构整理与 Word/TXT 排版工具。\n\n项目主页：{REPOSITORY}\n\nCopyright © 2026 SiriZhao. All rights reserved.\n许可证：MIT License\n\n基础清洗完全在本机完成。AI 优化仅在用户主动操作后调用其自行配置的第三方 API。应用不提供公共 API Key，不代理或转售模型服务；第三方数据处理受对应提供商政策约束。\n\n本软件不提供规避 AI 检测、绕过查重或实施学术不端的功能。"
        )
        details.setWordWrap(True)
        details.setTextInteractionFlags(
            details.textInteractionFlags() | Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(details)
        row = QHBoxLayout()
        home = QPushButton("项目主页")
        license_button = QPushButton("查看许可证")
        copy = QPushButton("复制版本信息")
        close = QPushButton("关闭")
        row.addWidget(home)
        row.addWidget(license_button)
        row.addStretch()
        row.addWidget(copy)
        row.addWidget(close)
        layout.addLayout(row)
        home.clicked.connect(self.open_repository)
        license_button.clicked.connect(
            lambda: QMessageBox.information(
                self, "MIT License", "本项目采用 MIT License，完整文本见仓库 LICENSE 文件。"
            )
        )
        copy.clicked.connect(lambda: QApplication.clipboard().setText(version_information()))
        close.clicked.connect(self.accept)

    def open_repository(self) -> None:
        if not QDesktopServices.openUrl(QUrl(REPOSITORY)):
            QMessageBox.warning(self, "无法打开", f"请复制链接：\n{REPOSITORY}")
