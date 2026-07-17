"""Localized About dialog for the desktop presentation layer."""

from __future__ import annotations

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
from cleantext_studio.i18n import I18nService

REPOSITORY = "https://github.com/SiriZhao/CleanText-Studio"


def version_information() -> str:
    return "\n".join((
        f"CleanText Studio v{__version__}",
        f"Python {platform.python_version()}",
        f"PySide6 {PySide6.__version__}",
        f"Platform {platform.system()} {platform.release()}",
        f"Architecture {platform.machine()}",
        f"GitHub {REPOSITORY}",
    ))


class AboutDialog(QDialog):
    """Dialog whose complete visible text is refreshed from I18nService."""

    def __init__(self, service: I18nService, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.service = service
        self.resize(620, 520)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        self.title = QLabel()
        self.title.setObjectName("dialogTitle")
        layout.addWidget(self.title)
        self.details = QLabel()
        self.details.setWordWrap(True)
        self.details.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.details)
        row = QHBoxLayout()
        self.home = QPushButton()
        self.license_button = QPushButton()
        self.copy = QPushButton()
        self.close_button = QPushButton()
        row.addWidget(self.home)
        row.addWidget(self.license_button)
        row.addStretch()
        row.addWidget(self.copy)
        row.addWidget(self.close_button)
        layout.addLayout(row)
        self.home.clicked.connect(self.open_repository)
        self.license_button.clicked.connect(self.show_license)
        self.copy.clicked.connect(lambda: QApplication.clipboard().setText(version_information()))
        self.close_button.clicked.connect(self.accept)
        service.language_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def retranslate_ui(self, _locale: str | None = None) -> None:
        tr = self.service.tr
        self.setWindowTitle(tr("about.title"))
        self.title.setText(tr("brand.title"))
        self.details.setText(tr("about.details", version=__version__, repository=REPOSITORY))
        self.home.setText(tr("about.homepage"))
        self.license_button.setText(tr("about.license"))
        self.copy.setText(tr("about.copy_version"))
        self.close_button.setText(tr("dialog.close"))

    def show_license(self) -> None:
        QMessageBox.information(self, self.service.tr("about.license"), self.service.tr("about.license_message"))

    def open_repository(self) -> None:
        if not QDesktopServices.openUrl(QUrl(REPOSITORY)):
            QMessageBox.warning(self, self.service.tr("dialog.error"), self.service.tr("about.open_failed", repository=REPOSITORY))
