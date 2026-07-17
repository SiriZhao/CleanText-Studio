"""Offline, re-translatable help dialog."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from cleantext_studio.i18n import I18nService

HELP_SECTIONS = ("quick_start", "import", "cleaning", "paragraphs", "headings", "tables", "math", "word", "ai", "privacy", "faq")


class HelpDialog(QDialog):
    """Local help browser that refreshes from the active catalog."""

    def __init__(self, service: I18nService, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.service = service
        self.resize(820, 560)
        root = QVBoxLayout(self)
        body = QHBoxLayout()
        self.navigation = QListWidget()
        self.navigation.setMaximumWidth(220)
        self.content = QTextBrowser()
        self.content.setOpenExternalLinks(True)
        body.addWidget(self.navigation)
        body.addWidget(self.content, 1)
        root.addLayout(body)
        buttons = QHBoxLayout()
        buttons.addStretch()
        self.close_button = QPushButton()
        self.close_button.clicked.connect(self.accept)
        buttons.addWidget(self.close_button)
        root.addLayout(buttons)
        self.navigation.currentRowChanged.connect(self._show_section)
        service.language_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def retranslate_ui(self, _locale: str | None = None) -> None:
        selected = max(self.navigation.currentRow(), 0)
        self.setWindowTitle(self.service.tr("help.title"))
        self.navigation.blockSignals(True)
        self.navigation.clear()
        for section in HELP_SECTIONS:
            self.navigation.addItem(self.service.tr(f"help.{section}.title"))
        self.navigation.setCurrentRow(min(selected, len(HELP_SECTIONS) - 1))
        self.navigation.blockSignals(False)
        self.close_button.setText(self.service.tr("dialog.close"))
        self._show_section(self.navigation.currentRow())

    def _show_section(self, row: int) -> None:
        if row >= 0:
            section = HELP_SECTIONS[row]
            self.content.setHtml(
                f"<h2>{self.service.tr(f'help.{section}.title')}</h2>"
                f"<p>{self.service.tr(f'help.{section}.body')}</p>"
            )
