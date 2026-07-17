"""Structured About dialog with immutable project facts."""

from __future__ import annotations

import platform
import sys
from pathlib import Path

import PySide6
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from cleantext_studio import __version__
from cleantext_studio.about_view_model import HOMEPAGE_URL, AboutViewModel
from cleantext_studio.i18n import I18nService

REPOSITORY = HOMEPAGE_URL


def version_information(service: I18nService | None = None) -> str:
    if service is None:
        version = f"v{__version__}"
        developer = "SiriZhao"
        license_name = "MIT License"
        version_label, developer_label, license_label, homepage_label = (
            "Version", "Developer", "License", "Project homepage",
        )
    else:
        model = AboutViewModel.from_service(service)
        version, developer, license_name = model.version, model.developer, model.license_name
        version_label = service.tr("about.version")
        developer_label = service.tr("about.developer")
        license_label = service.tr("about.license")
        homepage_label = service.tr("about.homepage")
    return "\n".join((
        "CleanText Studio",
        f"{version_label}: {version}",
        f"{developer_label}: {developer}",
        f"{license_label}: {license_name}",
        f"{homepage_label}: {REPOSITORY}",
        f"Python {platform.python_version()} · PySide6 {PySide6.__version__}",
    ))


class AboutDialog(QDialog):
    """Render immutable facts separately from localized explanatory copy."""

    def __init__(self, service: I18nService, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.service = service
        self.resize(660, 580)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        self.title = QLabel()
        self.title.setObjectName("dialogTitle")
        layout.addWidget(self.title)
        self.subtitle = QLabel()
        layout.addWidget(self.subtitle)
        self.facts = QLabel()
        self.facts.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.facts)
        self.explanation = QLabel()
        self.explanation.setWordWrap(True)
        self.explanation.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.explanation)
        self.notice = QLabel()
        self.notice.setObjectName("muted")
        layout.addWidget(self.notice)
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
        self.copy.clicked.connect(self.copy_version_information)
        self.close_button.clicked.connect(self.accept)
        service.language_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def retranslate_ui(self, _locale: str | None = None) -> None:
        model = AboutViewModel.from_service(self.service)
        tr = self.service.tr
        self.setWindowTitle(tr("about.title"))
        self.title.setText(tr("about.title"))
        self.subtitle.setText(model.localized_product_subtitle)
        self.facts.setText("\n".join((
            model.product_name,
            f"{tr('about.version')}: {model.version}",
            f"{tr('about.developer')}: {model.developer}",
            f"{tr('about.homepage')}: {model.homepage_url}",
            model.copyright_text,
            f"{tr('about.license')}: {model.license_name}",
        )))
        self.explanation.setText("\n\n".join((
            model.description, model.local_processing, model.ai_processing,
            model.privacy, model.disclaimer,
        )))
        self.home.setText(tr("about.homepage"))
        self.license_button.setText(model.license_name)
        self.copy.setText(tr("about.copy_version"))
        self.close_button.setText(tr("dialog.close"))
        self.notice.clear()

    def copy_version_information(self) -> None:
        QApplication.clipboard().setText(version_information(self.service))
        self.notice.setText(self.service.tr("about.copy_version"))

    def show_license(self) -> None:
        path = Path(getattr(sys, "_MEIPASS", Path(__file__).parents[2])) / "LICENSE"
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            QMessageBox.warning(self, "MIT License", self.service.tr("about.license_message"))
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("MIT License")
        dialog.resize(720, 560)
        layout = QVBoxLayout(dialog)
        viewer = QPlainTextEdit(text)
        viewer.setReadOnly(True)
        layout.addWidget(viewer)
        close = QPushButton(self.service.tr("dialog.close"))
        close.clicked.connect(dialog.accept)
        layout.addWidget(close)
        dialog.exec()

    def open_repository(self) -> None:
        if not QDesktopServices.openUrl(QUrl(REPOSITORY)):
            QMessageBox.warning(
                self, self.service.tr("dialog.error"),
                self.service.tr("about.open_failed", repository=REPOSITORY),
            )
