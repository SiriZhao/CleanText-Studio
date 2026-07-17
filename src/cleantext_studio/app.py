from __future__ import annotations

import html
import sys
from contextlib import suppress
from pathlib import Path
from typing import cast

from PySide6.QtCore import QSettings, Qt, QThread, QUrl, Signal
from PySide6.QtGui import QAction, QCloseEvent, QDesktopServices, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from cleantext_studio.about_dialog import AboutDialog
from cleantext_studio.ai_dialogs import AIDiffDialog, ProviderDialog, SendConfirmationDialog
from cleantext_studio.cleaners import clean_text
from cleantext_studio.cleaners.tables import TableWidthPlanner
from cleantext_studio.exporters import export_docx_blocks, export_txt
from cleantext_studio.font_manager import FontManager
from cleantext_studio.help_dialog import HelpDialog
from cleantext_studio.i18n import I18nService
from cleantext_studio.importers import import_file
from cleantext_studio.llm.base import LLMProvider
from cleantext_studio.llm.config_store import ProviderConfigStore
from cleantext_studio.llm.credentials import CredentialStore
from cleantext_studio.llm.models import OptimizationMode
from cleantext_studio.llm.registry import create_provider
from cleantext_studio.llm.retry import with_retry
from cleantext_studio.llm.schemas import OptimizationResponse
from cleantext_studio.llm.sensitive import redact_sensitive
from cleantext_studio.math import FormulaParser, MathDetector, PreviewFormulaRenderer
from cleantext_studio.math.ast import FormulaNode
from cleantext_studio.models import (
    CleanOptions,
    CleanResult,
    DocumentSession,
    IndependentURLMode,
    LinkMode,
    ListMode,
    MathBlockData,
    MathExportMode,
    MathOutputMode,
    MergeLevel,
    ParagraphBreakMode,
    TextBlock,
)
from cleantext_studio.system_theme import SystemThemeWatcher
from cleantext_studio.theme import Theme, stylesheet
from cleantext_studio.ui.card_panel import CardPanel

SAMPLE = """## 一、项目背景

---

✅ 人工智能正在快速发展，
并逐渐应用于教育、
医疗和农业等领域。

- 提高效率
- 降低成本
- 改善体验"""


class CleanWorker(QThread):
    completed = Signal(object)
    failed = Signal(str)

    def __init__(self, text: str, options: CleanOptions) -> None:
        super().__init__()
        self.text = text
        self.options = options

    def run(self) -> None:
        try:
            if not self.isInterruptionRequested():
                self.completed.emit(clean_text(self.text, self.options))
        except Exception as exc:
            self.failed.emit(str(exc))


class AIWorker(QThread):
    completed = Signal(object)
    failed = Signal(str)

    def __init__(self, provider: LLMProvider, text: str, mode: OptimizationMode) -> None:
        super().__init__()
        self.provider = provider
        self.text = text
        self.mode = mode

    def run(self) -> None:
        try:
            if not self.isInterruptionRequested():
                self.completed.emit(
                    with_retry(
                        lambda: self.provider.optimize_document(self.text, self.mode),
                        self.isInterruptionRequested,
                    )
                )
        except Exception as exc:
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.session = DocumentSession()
        self.provider_store = ProviderConfigStore()
        self.credential_store = CredentialStore()
        self.worker: CleanWorker | None = None
        self.ai_worker: AIWorker | None = None
        self.settings_store = QSettings("CleanText Studio", "CleanText Studio")
        self.i18n = I18nService(self.settings_store)
        self.i18n.language_changed.connect(self._language_changed)
        self.theme_preference = Theme(str(self.settings_store.value("theme", Theme.SYSTEM.value)))
        self.theme_watcher = SystemThemeWatcher()
        self.theme_watcher.changed.connect(self._system_theme_changed)
        self.theme_watcher.start()
        self.setWindowTitle(self.tr("app.title"))
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)
        root = Path(getattr(sys, "_MEIPASS", Path(__file__).parents[3]))
        icon = root / "assets" / "icon.png"
        if icon.exists():
            self.setWindowIcon(QIcon(str(icon)))
        self._global_toolbar()
        self._build_ui()
        self._shortcuts()
        QApplication.instance().setLayoutDirection(self.i18n.direction())  # type: ignore[union-attr]
        QApplication.instance().setFont(FontManager(locale=self.i18n.active).application_font())  # type: ignore[union-attr]
        self.apply_theme(self.theme_preference)
        saved = self.settings_store.value("splitter_sizes")
        self.splitter.setSizes(
            [int(x) for x in saved] if isinstance(saved, list) else [520, 290, 520]
        )
        self.statusBar().showMessage(self.tr("status.ready"))

    def tr(self, key: str, /, **values: object) -> str:  # type: ignore[override]
        return self.i18n.tr(key, **values)

    def _global_toolbar(self) -> None:
        bar = QToolBar("global")
        bar.setMovable(False)
        self.addToolBar(bar)
        self.brand_label = QLabel("  " + self.tr("brand.title") + "  ")
        self.brand_label.setStyleSheet("font-size:16px;font-weight:600")
        self.file_label = QLabel(self.tr("file.untitled"))
        self.file_label.setObjectName("muted")
        self.dirty_label = QLabel("")
        bar.addWidget(self.brand_label)
        bar.addSeparator()
        bar.addWidget(self.file_label)
        bar.addWidget(self.dirty_label)
        spacer = QWidget()
        spacer.setSizePolicy(
            spacer.sizePolicy().Policy.Expanding, spacer.sizePolicy().Policy.Preferred
        )
        bar.addWidget(spacer)
        self.theme_button = QToolButton()
        self.theme_button.setText(self.tr("toolbar.theme"))
        self.theme_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        menu = QMenu(self.theme_button)
        self.theme_actions = {}
        for theme, key in (
            (Theme.SYSTEM, "theme.system"),
            (Theme.LIGHT, "theme.light"),
            (Theme.DARK, "theme.dark"),
        ):
            action = menu.addAction(self.tr(key))
            action.setData(key)
            action.setCheckable(True)
            action.triggered.connect(
                lambda checked=False, selected=theme: self.set_theme_preference(selected)
            )
            self.theme_actions[theme] = action
        self.theme_button.setMenu(menu)
        bar.addWidget(self.theme_button)
        self.collapse_action = bar.addAction(self.tr("toolbar.collapse_settings"), self.toggle_settings_panel)
        self.settings_action = bar.addAction(self.tr("toolbar.settings"), self.show_settings)
        self.help_action = bar.addAction(self.tr("toolbar.help"), self.show_help)
        self.about_action = bar.addAction(self.tr("toolbar.about"), self.about)

    def _panel(self, title: str) -> tuple[QFrame, QVBoxLayout, QLabel]:
        panel = CardPanel()
        layout = panel.content_layout
        heading = QLabel(title)
        heading.setObjectName("panelTitle")
        heading.setStyleSheet("font-size:16px;font-weight:600")
        layout.addWidget(heading)
        return panel, layout, heading

    def _buttons(
        self, layout: QVBoxLayout, items: list[tuple[str, object, str]]
    ) -> list[QPushButton]:
        row = QHBoxLayout()
        buttons = []
        for text, callback, tip in items:
            button = QPushButton(text)
            button.clicked.connect(callback)
            button.setToolTip(tip)
            row.addWidget(button)
            buttons.append(button)
        layout.addLayout(row)
        return buttons

    def _build_ui(self) -> None:
        left, lv, self.source_heading = self._panel(self.tr("panel.source"))
        self.source_buttons = self._buttons(
            lv,
            [
                (self.tr("action.new"), self.new, self.tr("tip.new")),
                (self.tr("action.open"), self.open, self.tr("tip.open")),
                (self.tr("action.paste"), self.paste_source, self.tr("tip.paste")),
                (self.tr("action.sample"), self.load_sample, self.tr("tip.sample")),
                (self.tr("action.clear"), self.clear_source, self.tr("tip.clear")),
            ],
        )
        self.source_buttons[-1].setObjectName("danger")
        self.input = QPlainTextEdit()
        self.input.setPlaceholderText(self.tr("placeholder.source"))
        lv.addWidget(self.input)
        self.source_meta = QLabel(self.tr("status.source_meta", count=0, paragraphs=0, encoding="UTF-8"))
        self.source_meta.setObjectName("muted")
        lv.addWidget(self.source_meta)
        middle, mv, self.settings_heading = self._panel(self.tr("panel.settings"))
        self.settings_panel = middle
        self.preset = QComboBox()
        for key, value in (("preset.light", "light"), ("preset.standard", "standard"), ("preset.deep", "deep"), ("preset.markdown", "markdown"), ("preset.linebreak", "linebreak"), ("preset.custom", "custom")):
            self.preset.addItem(self.tr(key), value)
        self.preset.setCurrentIndex(1)
        self.preset_label = QLabel(self.tr("preset.label"))
        mv.addWidget(self.preset_label)
        mv.addWidget(self.preset)
        rules = QWidget()
        rules.setObjectName("settingsContent")
        rv = QVBoxLayout(rules)
        self.remove_markdown = QCheckBox(self.tr("option.remove_markdown"))
        self.remove_markdown.setChecked(True)
        self.remove_emoji = QCheckBox(self.tr("option.remove_emoji"))
        self.remove_emoji.setChecked(True)
        self.clean_instructional = QCheckBox(self.tr("option.instructional"))
        self.clean_instructional.setChecked(False)
        self.link_mode = QComboBox()
        for key, value in (("link.text", LinkMode.TEXT_ONLY), ("link.url", LinkMode.TEXT_AND_URL), ("link.markdown", LinkMode.KEEP_MARKDOWN)):
            self.link_mode.addItem(self.tr(key), value)
        self.url_mode = QComboBox()
        for key, value in (("url.keep", IndependentURLMode.PRESERVE), ("url.merge", IndependentURLMode.MERGE_PREVIOUS), ("url.delete", IndependentURLMode.DELETE_TUTORIAL)):
            self.url_mode.addItem(self.tr(key), value)
        self.paragraph_mode = QComboBox()
        for key, value in (("paragraph.compact", ParagraphBreakMode.COMPACT), ("paragraph.smart", ParagraphBreakMode.SMART_SECTIONS), ("paragraph.preserve", ParagraphBreakMode.PRESERVE_ALL)):
            self.paragraph_mode.addItem(self.tr(key), value)
        self.paragraph_mode.setCurrentIndex(1)
        self.list_mode = QComboBox()
        for key, value in (("list.keep", ListMode.KEEP), ("list.remove", ListMode.REMOVE_MARKERS), ("list.natural", ListMode.NATURAL_PARAGRAPH)):
            self.list_mode.addItem(self.tr(key), value)
        self.detect_math = QCheckBox(self.tr("option.detect_math"))
        self.detect_math.setChecked(True)
        self.detect_math.setToolTip(self.tr("tip.detect_math"))
        self.protect_math = QCheckBox(self.tr("option.protect_math"))
        self.protect_math.setChecked(True)
        self.protect_math.setToolTip(self.tr("tip.protect_math"))
        self.normalize_math = QCheckBox(self.tr("option.normalize_math"))
        self.normalize_math.setChecked(True)
        self.normalize_math.setToolTip(self.tr("tip.normalize_math"))
        self.repair_math = QCheckBox(self.tr("option.repair_math"))
        self.repair_math.setChecked(True)
        self.repair_math.setToolTip(self.tr("tip.repair_math"))
        self.preserve_equation_numbers = QCheckBox(self.tr("option.equation_numbers"))
        self.preserve_equation_numbers.setChecked(True)
        self.word_math_omml = QCheckBox(self.tr("option.word_omml"))
        self.word_math_omml.setChecked(True)
        self.word_math_omml.setToolTip(self.tr("tip.word_omml"))
        self.math_output_mode = QComboBox()
        for key, value in (("math.preserve", MathOutputMode.PRESERVE), ("math.latex", MathOutputMode.LATEX), ("math.unicode", MathOutputMode.UNICODE)):
            self.math_output_mode.addItem(self.tr(key), value)
        self.math_output_mode.setToolTip(self.tr("tip.math_output"))
        self.group_basic = QLabel(self.tr("group.basic"))
        self.group_links = QLabel(self.tr("group.links"))
        self.group_url = QLabel(self.tr("group.url"))
        self.group_paragraph = QLabel(self.tr("group.paragraph"))
        self.group_list = QLabel(self.tr("group.list"))
        self.group_math = QLabel(self.tr("group.math"))
        self.group_math_output = QLabel(self.tr("group.math_output"))
        settings_widgets = (
            self.group_basic,
            self.remove_markdown,
            self.remove_emoji,
            self.clean_instructional,
            self.group_links,
            self.link_mode,
            self.group_url,
            self.url_mode,
            self.group_paragraph,
            self.paragraph_mode,
            self.group_list,
            self.list_mode,
            self.group_math,
            self.detect_math,
            self.protect_math,
            self.normalize_math,
            self.repair_math,
            self.preserve_equation_numbers,
            self.word_math_omml,
            self.group_math_output,
            self.math_output_mode,
        )
        rules.setMinimumWidth(0)
        for widget in settings_widgets:
            widget.setMinimumWidth(0)
            if isinstance(widget, QCheckBox):
                widget.setSizePolicy(
                    QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred
                )
            elif isinstance(widget, QComboBox):
                widget.setSizePolicy(
                    QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
                )
            rv.addWidget(widget)
        rv.addStretch()
        scroll = QScrollArea()
        scroll.setObjectName("settingsScrollView")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.settings_scroll = scroll
        scroll.setWidget(rules)
        mv.addWidget(scroll)
        self.rule_count = QLabel(self.tr("status.rules", count=8))
        self.rule_count.setObjectName("ruleCount")
        self.rule_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mv.addWidget(self.rule_count)
        self.clean_button = QPushButton(self.tr("action.clean"))
        self.clean_button.setObjectName("primary")
        self.clean_button.setEnabled(False)
        self.clean_button.clicked.connect(self.start_clean)
        mv.addWidget(self.clean_button)
        right, ov, self.result_heading = self._panel(self.tr("panel.result"))
        mode_row = QHBoxLayout()
        mode_container = QWidget()
        mode_container.setObjectName("displayModeToolbar")
        mode_container.setLayout(mode_row)
        self.result_mode_label = QLabel(self.tr("result.mode"))
        mode_row.addWidget(self.result_mode_label)
        self.result_mode = QComboBox()
        self.result_mode.addItem(self.tr("result.text"), "text")
        self.result_mode.addItem(self.tr("result.preview"), "preview")
        mode_row.addWidget(self.result_mode)
        mode_row.addStretch()
        ov.addWidget(mode_container)
        result_buttons = self._buttons(
            ov,
            [
                (self.tr("action.export_word"), self.save_word, self.tr("tip.export_word")),
                (self.tr("action.copy"), self.copy_result, self.tr("tip.copy")),
                (self.tr("action.export_txt"), self.save_txt, "Ctrl+Shift+T"),
                (self.tr("action.undo"), self.undo_result, "Ctrl+Z"),
                (self.tr("action.restore"), self.restore_result, self.tr("action.restore")),
                (self.tr("action.clear"), self.clear_result, self.tr("tip.clear")),
            ],
        )
        (
            self.word_button,
            self.copy_button,
            self.txt_button,
            self.undo_button,
            self.restore_button,
            self.clear_result_button,
        ) = result_buttons
        self.word_tip = QLabel(self.tr("result.word_tip"))
        self.word_tip.setObjectName("muted")
        ov.addWidget(self.word_tip)
        self.ai_button = QPushButton(self.tr("action.ai"))
        self.ai_button.setToolTip(self.tr("tip.ai"))
        self.ai_button.clicked.connect(self.start_ai_optimization)
        ov.addWidget(self.ai_button)
        self.output = QPlainTextEdit()
        self.output.setPlaceholderText(self.tr("placeholder.result"))
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_container)
        self.preview_layout.addStretch()
        self.preview = QScrollArea()
        self.preview.setWidgetResizable(True)
        self.preview.setWidget(self.preview_container)
        self.result_stack = QStackedWidget()
        self.result_stack.addWidget(self.output)
        self.result_stack.addWidget(self.preview)
        ov.addWidget(self.result_stack)
        self.result_notice = QLabel(self.tr("status.not_cleaned"))
        self.result_notice.setObjectName("muted")
        self.result_notice.setWordWrap(True)
        ov.addWidget(self.result_notice)
        self.residual_button = QPushButton(self.tr("action.view_residuals"))
        self.residual_button.clicked.connect(self.show_residuals)
        self.residual_button.hide()
        ov.addWidget(self.residual_button)
        self.open_folder_button = QPushButton(self.tr("action.open_folder"))
        self.open_folder_button.hide()
        ov.addWidget(self.open_folder_button)
        self.result_meta = QLabel(self.tr("status.result_meta", count=0))
        self.result_meta.setObjectName("muted")
        ov.addWidget(self.result_meta)
        self.splitter = QSplitter()
        self.splitter.setObjectName("mainSplitter")
        self.splitter.addWidget(left)
        self.splitter.addWidget(middle)
        self.splitter.addWidget(right)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setStretchFactor(0, 4)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.setStretchFactor(2, 4)
        left.setMinimumWidth(360)
        middle.setMinimumWidth(270)
        right.setMinimumWidth(360)
        self.setCentralWidget(self.splitter)
        self.input.textChanged.connect(self._source_changed)
        self.output.textChanged.connect(self._result_changed)
        self.result_mode.currentIndexChanged.connect(self.result_stack.setCurrentIndex)
        self.preset.currentIndexChanged.connect(lambda _index: self._preset_changed())
        for control in (
            self.remove_markdown,
            self.remove_emoji,
            self.clean_instructional,
            self.detect_math,
            self.protect_math,
            self.normalize_math,
            self.repair_math,
            self.preserve_equation_numbers,
            self.word_math_omml,
        ):
            control.toggled.connect(self._customized)
        self.paragraph_mode.currentIndexChanged.connect(self._customized)
        self.list_mode.currentIndexChanged.connect(self._customized)
        self.link_mode.currentIndexChanged.connect(self._customized)
        self.url_mode.currentIndexChanged.connect(self._customized)
        self.math_output_mode.currentIndexChanged.connect(self._customized)
        self._set_result_actions(False)

    def _shortcuts(self) -> None:
        for sequence, callback in [
            ("Ctrl+N", self.new),
            ("Ctrl+O", self.open),
            ("Ctrl+Return", self.start_clean),
            ("Ctrl+Shift+C", self.copy_result),
            ("Ctrl+Shift+T", self.save_txt),
            ("Ctrl+Shift+W", self.save_word),
            ("Ctrl+,", self.show_settings),
            ("F1", self.show_help),
        ]:
            action = QAction(self)
            action.setShortcut(QKeySequence(sequence))
            action.triggered.connect(callback)
            self.addAction(action)

    def _options(self) -> CleanOptions:
        return CleanOptions(
            remove_markdown=self.remove_markdown.isChecked(),
            remove_emoji=self.remove_emoji.isChecked(),
            merge_level=MergeLevel.STANDARD,
            paragraph_break_mode=cast(ParagraphBreakMode, self.paragraph_mode.currentData()),
            list_mode=cast(ListMode, self.list_mode.currentData()),
            clean_instructional_labels=self.clean_instructional.isChecked(),
            link_mode=cast(LinkMode, self.link_mode.currentData()),
            independent_url_mode=cast(IndependentURLMode, self.url_mode.currentData()),
            detect_math=self.detect_math.isChecked(),
            protect_math=self.protect_math.isChecked(),
            normalize_math_spacing=self.normalize_math.isChecked(),
            repair_math_delimiters=self.repair_math.isChecked(),
            preserve_equation_numbers=self.preserve_equation_numbers.isChecked(),
            math_export_mode=(
                MathExportMode.WORD_OMML
                if self.word_math_omml.isChecked()
                else MathExportMode.LATEX_TEXT
            ),
            math_output_mode=cast(MathOutputMode, self.math_output_mode.currentData()),
        )

    def _source_changed(self) -> None:
        text = self.input.toPlainText()
        self.session.source_text = text
        self.session.source_modified = True
        self.clean_button.setEnabled(
            bool(text.strip()) and not (self.worker and self.worker.isRunning())
        )
        self.source_meta.setText(
            self.tr(
                "status.source_meta",
                count=len(text),
                paragraphs=len([line for line in text.splitlines() if line.strip()]),
                encoding=self.session.encoding,
            )
        )
        if self.session.local_result_text:
            self.session.result_outdated = True
            self.result_notice.setText(self.tr("status.outdated"))

    def _result_changed(self) -> None:
        text = self.output.toPlainText()
        self.session.edited_result_text = text
        if self.session.local_result_text and text != self.session.local_result_text:
            self.session.result_modified = True
            self.result_notice.setText(self.tr("status.modified"))
        self.result_meta.setText(self.tr("status.result_meta", count=len(text)))
        self._set_result_actions(bool(text))

    def _set_result_actions(self, enabled: bool) -> None:
        for button in (self.word_button, self.copy_button, self.txt_button):
            button.setEnabled(enabled)

    def _customized(self, *_: object) -> None:
        if self.preset.currentData() != "custom":
            self.preset.blockSignals(True)
            self.preset.setCurrentIndex(self.preset.findData("custom"))
            self.preset.blockSignals(False)

    def _preset_changed(self) -> None:
        name = cast(str, self.preset.currentData())
        if name == "custom":
            return
        self.remove_markdown.setChecked(name != "linebreak")
        self.remove_emoji.setChecked(name not in {"markdown", "linebreak"})
        self.clean_instructional.setChecked(name == "deep")
        self.paragraph_mode.setCurrentIndex(
            2 if name == "light" else 0 if name == "deep" else 1
        )

    def start_clean(self) -> None:
        if not self.input.toPlainText().strip():
            return
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.clean_button.setText(self.tr("action.cancelling"))
            return
        self.session.processing_state = "processing"
        self.clean_button.setText(self.tr("action.cancel_clean"))
        self.clean_button.setEnabled(True)
        self.session.cleaning_options = self._options()
        self.worker = CleanWorker(self.input.toPlainText(), self.session.cleaning_options)
        self.worker.completed.connect(self._cleaned)
        self.worker.failed.connect(self._failed)
        self.worker.start()

    def _cleaned(self, result: CleanResult) -> None:
        self.session.local_result_text = result.text
        self.session.edited_result_text = result.text
        self.session.result_blocks = result.blocks
        self.session.cleaning_stats = result.stats
        self.session.residual_warnings = result.residuals
        self.session.result_modified = False
        self.session.result_outdated = False
        self.session.processing_state = "idle"
        self.output.blockSignals(True)
        self.output.setPlainText(result.text)
        self.output.blockSignals(False)
        self._render_preview(result.blocks)
        if any(block.table for block in result.blocks):
            self.result_mode.setCurrentIndex(1)
        self.clean_button.setText(self.tr("action.clean"))
        self.clean_button.setEnabled(True)
        self._set_result_actions(bool(result.text))
        warning = self.tr("status.residual_count", count=len(result.residuals)) if result.residuals else ""
        self.residual_button.setVisible(bool(result.residuals))
        self.result_notice.setText(
            self.tr("status.cleaned", count=result.stats.removed_chars,
                    merged=result.stats.merged_linebreaks) + warning
        )
        self.result_meta.setText(
            self.tr("statistics.summary", markdown=result.stats.removed_markdown,
                    ai=result.stats.removed_ai_patterns, blank=result.stats.removed_blank_lines,
                    emoji=result.stats.removed_emoji, headings=result.stats.headings_detected,
                    columns=result.stats.empty_table_columns_removed,
                    elapsed=result.stats.elapsed_ms)
        )

    def show_residuals(self) -> None:
        if not self.session.residual_warnings:
            return
        details = "\n".join(
            f"第 {item.line_number} 行 · {item.warning_type} · {item.snippet}"
            for item in self.session.residual_warnings[:50]
        )
        QMessageBox.warning(self, "可能的格式残留", details)

    def _render_preview(self, blocks: list[TextBlock]) -> None:
        while self.preview_layout.count() > 1:
            item = self.preview_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        for block in blocks:
            if block.table is not None:
                data = block.table
                assert data is not None
                table = QTableWidget(len(data.rows), len(data.headers))
                table.setHorizontalHeaderLabels(data.headers)
                table.setWordWrap(True)
                table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
                for column, ratio in enumerate(TableWidthPlanner().proportions(data)):
                    table.setColumnWidth(column, max(120, int(430 * ratio)))
                table.verticalHeader().hide()
                for row, values in enumerate(data.rows):
                    for column, value in enumerate(values):
                        if MathDetector().detect_inline(value):
                            cell = QLabel(self._formula_rich_text(value))
                            cell.setTextFormat(Qt.TextFormat.RichText)
                            cell.setWordWrap(True)
                            cell.setMargin(6)
                            table.setCellWidget(row, column, cell)
                        else:
                            table.setItem(row, column, QTableWidgetItem(value))
                table.resizeRowsToContents()
                table.setMinimumHeight(
                    min(420, 70 + sum(table.rowHeight(i) for i in range(table.rowCount())))
                )
                self.preview_layout.insertWidget(self.preview_layout.count() - 1, table)
            elif getattr(block, "text", ""):
                label = QLabel(block.text)
                label.setWordWrap(True)
                if block.math is not None:
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    label.setObjectName("mathPreview")
                    label.setTextFormat(Qt.TextFormat.RichText)
                    label.setText(self._math_block_html(block.math))
                    label.setToolTip(self.tr("tip.word_omml"))
                else:
                    formulas = cast(list[MathBlockData], block.metadata.get("inline_math", []))
                    if formulas:
                        label.setTextFormat(Qt.TextFormat.RichText)
                        label.setText(self._formula_rich_text(block.text))
                self.preview_layout.insertWidget(self.preview_layout.count() - 1, label)

    @staticmethod
    def _math_block_html(data: MathBlockData) -> str:
        ast = data.metadata.get("ast")
        if ast is None:
            try:
                ast = FormulaParser().parse(data.expression_source or data.normalized_text)
            except ValueError:
                return html.escape(data.expression_source or data.normalized_text)
        rendered = PreviewFormulaRenderer().render(cast(FormulaNode, ast))
        number = f"&nbsp;&nbsp;&nbsp;{html.escape(data.equation_number)}" if data.equation_number else ""
        return rendered + number

    @staticmethod
    def _formula_rich_text(text: str) -> str:
        regions = MathDetector().detect_inline(text)
        if not regions:
            return html.escape(text)
        parts: list[str] = []
        cursor = 0
        renderer = PreviewFormulaRenderer()
        parser = FormulaParser()
        for region in regions:
            parts.append(html.escape(text[cursor : region.start]))
            try:
                parts.append(renderer.render(parser.parse(region.content)))
            except ValueError:
                parts.append(html.escape(region.content))
            cursor = region.end
        parts.append(html.escape(text[cursor:]))
        return "".join(parts)

    def _failed(self, message: str) -> None:
        self.session.processing_state = "idle"
        self.clean_button.setText(self.tr("action.clean"))
        QMessageBox.critical(self, self.tr("dialog.processing_failed"), message)

    def new(self) -> None:
        if (
            self.session.result_modified
            and QMessageBox.question(self, "确认", "清空未保存内容？")
            != QMessageBox.StandardButton.Yes
        ):
            return
        self.input.clear()
        self.output.clear()
        self.session = DocumentSession()
        self.file_label.setText(self.tr("file.untitled"))

    def open(self) -> None:
        name, _ = QFileDialog.getOpenFileName(
            self, "打开", "", "支持文件 (*.txt *.md *.markdown *.docx)"
        )
        if name:
            try:
                self.input.setPlainText(import_file(Path(name)))
                self.session.current_file = Path(name)
                self.file_label.setText(Path(name).name)
            except Exception as exc:
                QMessageBox.critical(self, "导入失败", str(exc))

    def paste_source(self) -> None:
        self.input.setFocus()
        self.input.paste()

    def load_sample(self) -> None:
        self.input.setPlainText(SAMPLE)

    def clear_source(self) -> None:
        self.input.clear()

    def clear_result(self) -> None:
        self.output.clear()

    def copy_result(self) -> None:
        QApplication.clipboard().setText(self.output.toPlainText())

    def undo_result(self) -> None:
        self.output.undo()

    def restore_result(self) -> None:
        self.output.setPlainText(self.session.local_result_text)

    def save_txt(self) -> None:
        if not self.output.toPlainText():
            return
        name, _ = QFileDialog.getSaveFileName(
            self, "导出 TXT", "CleanText_cleaned.txt", "TXT (*.txt)"
        )
        if name:
            export_txt(self.output.toPlainText(), Path(name))

    def save_word(self) -> None:
        if not self.output.toPlainText():
            return
        if self.session.result_modified:
            export_result = clean_text(self.output.toPlainText(), self.session.cleaning_options)
            export_blocks = export_result.blocks
            residuals = export_result.residuals
        else:
            export_blocks = self.session.result_blocks
            residuals = self.session.residual_warnings
        counts = self._word_structure_counts(export_blocks)
        if any(counts.values()) or residuals:
            box = QMessageBox(self)
            box.setWindowTitle(self.tr("dialog.export_word_title"))
            box.setText(
                "已识别：\n"
                + "\n".join(f"✓ {count} 个{name}" for name, count in counts.items() if count)
                + (f"\n\n⚠ 仍有 {len(residuals)} 处可能残留" if residuals else "")
                + "\n\n推荐导出 Word，可完整保留标题、列表和表格结构。"
            )
            continue_button = box.addButton("继续导出 Word", QMessageBox.ButtonRole.AcceptRole)
            box.addButton("取消", QMessageBox.ButtonRole.RejectRole)
            box.exec()
            if box.clickedButton() != continue_button:
                return
        name, _ = QFileDialog.getSaveFileName(
            self, "导出 Word", "CleanText_cleaned.docx", "Word (*.docx)"
        )
        if name:
            try:
                export_docx_blocks(
                    export_blocks,
                    Path(name),
                    math_export_mode=self.session.cleaning_options.math_export_mode,
                )
                self.result_notice.setText(
                    "导出成功 · 已保留标题结构、表格、列表和中文排版\n" + name
                )
                self.open_folder_button.show()
                with suppress(RuntimeError):
                    self.open_folder_button.clicked.disconnect()
                self.open_folder_button.clicked.connect(
                    lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path(name).parent)))
                )
            except Exception as exc:
                QMessageBox.critical(self, "导出失败", str(exc))

    @staticmethod
    def _word_structure_counts(blocks: list[TextBlock]) -> dict[str, int]:
        return {
            "标题": sum(b.type.value.startswith("heading") for b in blocks),
            "列表": sum("list_item" in b.type.value for b in blocks),
            "表格": sum(b.table is not None for b in blocks),
            "引用": sum(b.type.value == "quote" for b in blocks),
            "代码块": sum(b.type.value == "code" for b in blocks),
        }

    def set_theme_preference(self, theme: Theme) -> None:
        self.theme_preference = theme
        self.settings_store.setValue("theme", theme.value)
        self.apply_theme(theme)

    def _system_theme_changed(self, theme: Theme) -> None:
        if self.theme_preference == Theme.SYSTEM:
            self.apply_theme(theme)

    def toggle_settings_panel(self) -> None:
        self.settings_panel.setVisible(not self.settings_panel.isVisible())

    def apply_theme(self, theme: Theme) -> None:
        effective = self.theme_watcher.current() if theme == Theme.SYSTEM else theme
        app = cast(QApplication | None, QApplication.instance())
        if app:
            app.setStyleSheet(stylesheet(effective))
        for value, action in self.theme_actions.items():
            action.setChecked(value == self.theme_preference)

    def show_settings(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("settings.title"))
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(self.tr("settings.language_region")))
        layout.addWidget(QLabel(self.tr("settings.interface_language")))
        selector = QComboBox(dialog)
        for language in self.i18n.languages():
            label = self.tr("settings.follow_system") if language.code == "system" else language.native_name
            selector.addItem(label, language.code)
        selector.setCurrentIndex(selector.findData(self.i18n.preference))
        layout.addWidget(selector)
        buttons = QHBoxLayout()
        buttons.addStretch()
        cancel = QPushButton(self.tr("dialog.cancel"))
        save = QPushButton(self.tr("dialog.save"))
        save.setObjectName("primary")
        cancel.clicked.connect(dialog.reject)
        save.clicked.connect(dialog.accept)
        buttons.addWidget(cancel)
        buttons.addWidget(save)
        layout.addLayout(buttons)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.i18n.set_language(cast(str, selector.currentData()))

    def _language_changed(self, _code: str) -> None:
        """Refresh the visible shell without touching session or cleaning options."""
        QApplication.instance().setLayoutDirection(self.i18n.direction())  # type: ignore[union-attr]
        QApplication.instance().setFont(FontManager(locale=self.i18n.active).application_font())  # type: ignore[union-attr]
        self.setWindowTitle(self.tr("app.title"))
        self.brand_label.setText("  " + self.tr("brand.title") + "  ")
        self.source_heading.setText(self.tr("panel.source"))
        self.settings_heading.setText(self.tr("panel.settings"))
        self.result_heading.setText(self.tr("panel.result"))
        self.theme_button.setText(self.tr("toolbar.theme"))
        for _theme, action in self.theme_actions.items():
            action.setText(self.tr(cast(str, action.data())))
        self.collapse_action.setText(self.tr("toolbar.collapse_settings"))
        self.settings_action.setText(self.tr("toolbar.settings"))
        self.help_action.setText(self.tr("toolbar.help"))
        self.about_action.setText(self.tr("toolbar.about"))
        for button, key in zip(self.source_buttons, ("action.new", "action.open", "action.paste", "action.sample", "action.clear"), strict=True):
            button.setText(self.tr(key))
        for button, key in zip((self.word_button, self.copy_button, self.txt_button, self.undo_button, self.restore_button, self.clear_result_button), ("action.export_word", "action.copy", "action.export_txt", "action.undo", "action.restore", "action.clear"), strict=True):
            button.setText(self.tr(key))
        self.ai_button.setText(self.tr("action.ai"))
        self.clean_button.setText(self.tr("action.clean"))
        self.input.setPlaceholderText(self.tr("placeholder.source"))
        self.output.setPlaceholderText(self.tr("placeholder.result"))
        self.preset_label.setText(self.tr("preset.label"))
        self.group_basic.setText(self.tr("group.basic"))
        self.group_links.setText(self.tr("group.links"))
        self.group_url.setText(self.tr("group.url"))
        self.group_paragraph.setText(self.tr("group.paragraph"))
        self.group_list.setText(self.tr("group.list"))
        self.group_math.setText(self.tr("group.math"))
        self.group_math_output.setText(self.tr("group.math_output"))
        self.result_mode_label.setText(self.tr("result.mode"))
        self.remove_markdown.setText(self.tr("option.remove_markdown"))
        self.remove_emoji.setText(self.tr("option.remove_emoji"))
        self.clean_instructional.setText(self.tr("option.instructional"))
        self.detect_math.setText(self.tr("option.detect_math"))
        self.protect_math.setText(self.tr("option.protect_math"))
        self.normalize_math.setText(self.tr("option.normalize_math"))
        self.repair_math.setText(self.tr("option.repair_math"))
        self.preserve_equation_numbers.setText(self.tr("option.equation_numbers"))
        self.word_math_omml.setText(self.tr("option.word_omml"))
        self.detect_math.setToolTip(self.tr("tip.detect_math"))
        self.protect_math.setToolTip(self.tr("tip.protect_math"))
        self.normalize_math.setToolTip(self.tr("tip.normalize_math"))
        self.repair_math.setToolTip(self.tr("tip.repair_math"))
        self.word_math_omml.setToolTip(self.tr("tip.word_omml"))
        self.math_output_mode.setToolTip(self.tr("tip.math_output"))
        self.word_tip.setText(self.tr("result.word_tip"))
        self.residual_button.setText(self.tr("action.view_residuals"))
        self.open_folder_button.setText(self.tr("action.open_folder"))
        self.source_meta.setText(
            self.tr(
                "status.source_meta",
                count=len(self.input.toPlainText()),
                paragraphs=len([line for line in self.input.toPlainText().splitlines() if line.strip()]),
                encoding=self.session.encoding,
            )
        )
        self.result_meta.setText(self.tr("status.result_meta", count=len(self.output.toPlainText())))
        self.rule_count.setText(self.tr("status.rules", count=8))
        self.statusBar().showMessage(self.tr("status.ready"))
        self._retranslate_combo(self.result_mode, (("result.text", "text"), ("result.preview", "preview")))
        self._retranslate_combo(self.preset, (("preset.light", "light"), ("preset.standard", "standard"), ("preset.deep", "deep"), ("preset.markdown", "markdown"), ("preset.linebreak", "linebreak"), ("preset.custom", "custom")))
        self._retranslate_combo(self.paragraph_mode, (("paragraph.compact", ParagraphBreakMode.COMPACT), ("paragraph.smart", ParagraphBreakMode.SMART_SECTIONS), ("paragraph.preserve", ParagraphBreakMode.PRESERVE_ALL)))
        self._retranslate_combo(self.list_mode, (("list.keep", ListMode.KEEP), ("list.remove", ListMode.REMOVE_MARKERS), ("list.natural", ListMode.NATURAL_PARAGRAPH)))
        self._retranslate_combo(self.link_mode, (("link.text", LinkMode.TEXT_ONLY), ("link.url", LinkMode.TEXT_AND_URL), ("link.markdown", LinkMode.KEEP_MARKDOWN)))
        self._retranslate_combo(self.url_mode, (("url.keep", IndependentURLMode.PRESERVE), ("url.merge", IndependentURLMode.MERGE_PREVIOUS), ("url.delete", IndependentURLMode.DELETE_TUTORIAL)))
        self._retranslate_combo(self.math_output_mode, (("math.preserve", MathOutputMode.PRESERVE), ("math.latex", MathOutputMode.LATEX), ("math.unicode", MathOutputMode.UNICODE)))

    def _retranslate_combo(self, combo: QComboBox, values: tuple[tuple[str, object], ...]) -> None:
        current = combo.currentData()
        combo.blockSignals(True)
        combo.clear()
        for key, value in values:
            combo.addItem(self.tr(key), value)
        combo.setCurrentIndex(combo.findData(current))
        combo.blockSignals(False)

    def configure_provider(self) -> None:
        dialog = ProviderDialog(self)

        def start_connection(fetch_models: bool = False) -> None:
            try:
                config = dialog.config()
                provider = create_provider(config, dialog.api_key.text())
                if fetch_models:
                    dialog.start_model_fetch(provider)
                else:
                    dialog.start_connection_test(provider)
            except Exception as exc:
                QMessageBox.warning(dialog, "配置不完整", str(exc))

        dialog.test_button.clicked.connect(lambda: start_connection(False))
        dialog.fetch_models.clicked.connect(lambda: start_connection(True))
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        try:
            config = dialog.config()
            self.provider_store.save([config])
            stored = self.credential_store.save(
                config.name, dialog.api_key.text(), dialog.remember.currentIndex() == 0
            )
            message = (
                "配置已保存，API Key 已写入 Windows 凭据库。"
                if stored
                else "配置已保存，API Key 仅保留在本次会话。"
            )
            QMessageBox.information(self, "AI 配置", message)
        except Exception as exc:
            QMessageBox.critical(self, "配置无效", str(exc))

    def start_ai_optimization(self) -> None:
        if self.ai_worker and self.ai_worker.isRunning():
            self.ai_worker.requestInterruption()
            self.ai_worker.provider.cancel()
            self.ai_button.setText(self.tr("action.cancelling"))
            return
        if not self.output.toPlainText():
            QMessageBox.information(self, "AI 智能优化", "请先完成本地清洗。")
            return
        providers = self.provider_store.load()
        if not providers:
            QMessageBox.information(self, "AI 智能优化", "请先在设置中配置你自己的 API。")
            return
        config = providers[0]
        key = self.credential_store.get(config.name)
        if not key:
            QMessageBox.warning(self, "AI 智能优化", "未找到 API Key，请重新配置。")
            return
        provider = create_provider(config, key)
        redacted = redact_sensitive(self.output.toPlainText())
        dialog = SendConfirmationDialog(
            config, provider.estimate_request_size(redacted.text), redacted.counts, self
        )
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        self.ai_button.setText(self.tr("action.cancel_clean"))
        self.ai_worker = AIWorker(provider, redacted.text, dialog.selected_mode())
        self.ai_worker.completed.connect(self._ai_completed)
        self.ai_worker.failed.connect(self._ai_failed)
        self.ai_worker.start()

    def _ai_completed(self, response: OptimizationResponse) -> None:
        self.ai_button.setText(self.tr("action.ai"))
        suggested = "\n".join(block.text for block in response.blocks)
        metadata = response.metadata
        risky = metadata.facts_added or metadata.facts_removed or metadata.references_changed
        dialog = AIDiffDialog(self.output.toPlainText(), suggested, risky, self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.output.setPlainText(suggested)

    def _ai_failed(self, message: str) -> None:
        self.ai_button.setText(self.tr("action.ai"))
        QMessageBox.critical(self, "AI 优化失败", f"{message}\n本地清洗结果未被覆盖。")

    def show_help(self) -> None:
        HelpDialog(self.i18n, self).exec()

    def about(self) -> None:
        AboutDialog(self.i18n, self).exec()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.settings_store.setValue("splitter_sizes", self.splitter.sizes())
        self.theme_watcher.stop()
        self.credential_store.clear_session()
        if (
            self.session.result_modified
            and QMessageBox.question(self, "退出", "结果尚未保存，确定退出？")
            != QMessageBox.StandardButton.Yes
        ):
            event.ignore()
            return
        event.accept()


def create_app() -> tuple[QApplication, MainWindow]:
    app = cast(QApplication | None, QApplication.instance()) or QApplication([])
    app.setApplicationName("CleanText Studio")
    return app, MainWindow()
