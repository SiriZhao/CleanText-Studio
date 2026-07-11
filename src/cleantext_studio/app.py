from __future__ import annotations

import sys
from pathlib import Path
from typing import cast

from PySide6.QtCore import QSettings, Qt, QThread, Signal
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSplitter,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from cleantext_studio import __version__
from cleantext_studio.cleaners import clean_text
from cleantext_studio.exporters import export_docx, export_txt
from cleantext_studio.importers import import_file
from cleantext_studio.models import CleanOptions, CleanResult, DocumentSession, ListMode, MergeLevel
from cleantext_studio.theme import Theme, stylesheet

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


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.session = DocumentSession()
        self.worker: CleanWorker | None = None
        self.settings_store = QSettings("CleanText Studio", "CleanText Studio")
        self.setWindowTitle("净文排版 · CleanText Studio")
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)
        root = Path(getattr(sys, "_MEIPASS", Path(__file__).parents[3]))
        icon = root / "assets" / "icon.png"
        if icon.exists():
            self.setWindowIcon(QIcon(str(icon)))
        self._global_toolbar()
        self._build_ui()
        self._shortcuts()
        self.apply_theme(Theme.LIGHT)
        saved = self.settings_store.value("splitter_sizes")
        self.splitter.setSizes(
            [int(x) for x in saved] if isinstance(saved, list) else [520, 290, 520]
        )
        self.statusBar().showMessage("就绪 · 文本仅在本机处理")

    def _global_toolbar(self) -> None:
        bar = QToolBar("全局")
        bar.setMovable(False)
        self.addToolBar(bar)
        title = QLabel("  净文排版 · CleanText Studio  ")
        title.setStyleSheet("font-size:16px;font-weight:600")
        self.file_label = QLabel("未命名")
        self.file_label.setObjectName("muted")
        self.dirty_label = QLabel("")
        bar.addWidget(title)
        bar.addSeparator()
        bar.addWidget(self.file_label)
        bar.addWidget(self.dirty_label)
        spacer = QWidget()
        spacer.setSizePolicy(
            spacer.sizePolicy().Policy.Expanding, spacer.sizePolicy().Policy.Preferred
        )
        bar.addWidget(spacer)
        self.theme_action = QAction("深色", self)
        self.theme_action.triggered.connect(self.toggle_theme)
        bar.addAction(self.theme_action)
        bar.addAction("折叠设置", self.toggle_settings_panel)
        bar.addAction("设置", self.show_settings)
        bar.addAction("帮助", self.show_help)
        bar.addAction("关于", self.about)

    def _panel(self, title: str) -> tuple[QFrame, QVBoxLayout]:
        panel = QFrame()
        panel.setObjectName("panel")
        layout = QVBoxLayout(panel)
        heading = QLabel(title)
        heading.setStyleSheet("font-size:16px;font-weight:600")
        layout.addWidget(heading)
        return panel, layout

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
        left, lv = self._panel("原始文本")
        self._buttons(
            lv,
            [
                ("新建", self.new, "新建 Ctrl+N"),
                ("打开", self.open, "打开 Ctrl+O"),
                ("粘贴", self.paste_source, "粘贴 Ctrl+V"),
                ("示例", self.load_sample, "载入示例"),
                ("清空", self.clear_source, "清空原文"),
            ],
        )[-1].setObjectName("danger")
        self.input = QPlainTextEdit()
        self.input.setPlaceholderText("在此粘贴文本，或拖入 TXT、Markdown、Word 文件")
        lv.addWidget(self.input)
        self.source_meta = QLabel("0 字符 · 0 段 · UTF-8")
        self.source_meta.setObjectName("muted")
        lv.addWidget(self.source_meta)
        middle, mv = self._panel("清洗设置")
        self.settings_panel = middle
        self.preset = QComboBox()
        self.preset.addItems(
            ["轻度清洗", "标准清洗", "深度清洗", "仅清除 Markdown", "仅修复换行", "自定义"]
        )
        self.preset.setCurrentText("标准清洗")
        mv.addWidget(QLabel("清洗预设"))
        mv.addWidget(self.preset)
        rules = QWidget()
        rv = QVBoxLayout(rules)
        self.remove_markdown = QCheckBox("删除 Markdown 标记\n清除 #、**、--- 等格式符号")
        self.remove_markdown.setChecked(True)
        self.remove_emoji = QCheckBox("删除表情和装饰符号")
        self.remove_emoji.setChecked(True)
        self.chat_phrases = QCheckBox("清理聊天式套话（仅开头和结尾）")
        self.merge_level = QComboBox()
        self.merge_level.addItems(["保守", "标准", "积极"])
        self.merge_level.setCurrentText("标准")
        self.list_mode = QComboBox()
        self.list_mode.addItems(
            ["保留列表结构", "删除项目符号，保留逐行内容", "智能转换为自然段（实验性）"]
        )
        for widget in (
            QLabel("基础格式"),
            self.remove_markdown,
            self.remove_emoji,
            QLabel("段落与换行"),
            self.merge_level,
            QLabel("标题与列表"),
            self.list_mode,
            QLabel("高级选项"),
            self.chat_phrases,
        ):
            rv.addWidget(widget)
        rv.addStretch()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(rules)
        mv.addWidget(scroll)
        self.rule_count = QLabel("将应用 8 项规则")
        self.rule_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mv.addWidget(self.rule_count)
        self.clean_button = QPushButton("开始清洗")
        self.clean_button.setObjectName("primary")
        self.clean_button.setEnabled(False)
        self.clean_button.clicked.connect(self.start_clean)
        mv.addWidget(self.clean_button)
        right, ov = self._panel("清洗结果")
        result_buttons = self._buttons(
            ov,
            [
                ("导出 Word", self.save_word, "导出 Word Ctrl+Shift+W"),
                ("复制", self.copy_result, "复制结果 Ctrl+Shift+C"),
                ("导出 TXT", self.save_txt, "导出 TXT Ctrl+Shift+T"),
                ("撤销", self.undo_result, "撤销 Ctrl+Z"),
                ("恢复本次", self.restore_result, "恢复本次清洗结果"),
                ("清空", self.clear_result, "清空结果"),
            ],
        )
        self.word_button, self.copy_button, self.txt_button = result_buttons[:3]
        self.output = QPlainTextEdit()
        self.output.setPlaceholderText("清洗后的文本将在这里显示")
        ov.addWidget(self.output)
        self.result_notice = QLabel("尚未清洗")
        self.result_notice.setObjectName("muted")
        self.result_notice.setWordWrap(True)
        ov.addWidget(self.result_notice)
        self.result_meta = QLabel("0 字符 · 0 项修改")
        self.result_meta.setObjectName("muted")
        ov.addWidget(self.result_meta)
        self.splitter = QSplitter()
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
        self.preset.currentTextChanged.connect(self._preset_changed)
        for control in (self.remove_markdown, self.remove_emoji, self.chat_phrases):
            control.toggled.connect(self._customized)
        self.merge_level.currentTextChanged.connect(self._customized)
        self.list_mode.currentTextChanged.connect(self._customized)
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
        levels = {
            "保守": MergeLevel.CONSERVATIVE,
            "标准": MergeLevel.STANDARD,
            "积极": MergeLevel.AGGRESSIVE,
        }
        modes = {0: ListMode.KEEP, 1: ListMode.REMOVE_MARKERS, 2: ListMode.NATURAL_PARAGRAPH}
        return CleanOptions(
            remove_markdown=self.remove_markdown.isChecked(),
            remove_emoji=self.remove_emoji.isChecked(),
            remove_template_phrases=self.chat_phrases.isChecked(),
            merge_level=levels[self.merge_level.currentText()],
            list_mode=modes[self.list_mode.currentIndex()],
        )

    def _source_changed(self) -> None:
        text = self.input.toPlainText()
        self.session.source_text = text
        self.session.source_modified = True
        self.clean_button.setEnabled(
            bool(text.strip()) and not (self.worker and self.worker.isRunning())
        )
        self.source_meta.setText(
            f"{len(text):,} 字符 · {len([x for x in text.splitlines() if x.strip()]):,} 段 · {self.session.encoding}"
        )
        if self.session.local_result_text:
            self.session.result_outdated = True
            self.result_notice.setText("注意：原始文本已改变，当前结果可能已过期 · 可重新清洗")

    def _result_changed(self) -> None:
        text = self.output.toPlainText()
        self.session.edited_result_text = text
        if self.session.local_result_text and text != self.session.local_result_text:
            self.session.result_modified = True
            self.result_notice.setText("结果已手动修改")
        self.result_meta.setText(f"{len(text):,} 字符")
        self._set_result_actions(bool(text))

    def _set_result_actions(self, enabled: bool) -> None:
        for button in (self.word_button, self.copy_button, self.txt_button):
            button.setEnabled(enabled)

    def _customized(self, *_: object) -> None:
        if self.preset.currentText() != "自定义":
            self.preset.blockSignals(True)
            self.preset.setCurrentText("自定义")
            self.preset.blockSignals(False)

    def _preset_changed(self, name: str) -> None:
        if name == "自定义":
            return
        self.remove_markdown.setChecked(name != "仅修复换行")
        self.remove_emoji.setChecked(name not in {"仅清除 Markdown", "仅修复换行"})
        self.merge_level.setCurrentText(
            "保守" if name == "轻度清洗" else "积极" if name == "深度清洗" else "标准"
        )

    def start_clean(self) -> None:
        if not self.input.toPlainText().strip():
            return
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.clean_button.setText("正在取消…")
            return
        self.session.processing_state = "processing"
        self.clean_button.setText("取消清洗")
        self.clean_button.setEnabled(True)
        self.worker = CleanWorker(self.input.toPlainText(), self._options())
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
        self.clean_button.setText("开始清洗")
        self.clean_button.setEnabled(True)
        self._set_result_actions(bool(result.text))
        warning = f" · 检测到 {len(result.residuals)} 项残留" if result.residuals else ""
        self.result_notice.setText(
            f"清洗完成 · 删除 {result.stats.removed_chars} 个字符 · 合并 {result.stats.merged_linebreaks} 处换行{warning}"
        )
        self.result_meta.setText(
            f"Markdown {result.stats.removed_markdown} · 表情 {result.stats.removed_emoji} · 分隔线 {result.stats.removed_separators} · 标题 {result.stats.headings_detected} · {result.stats.elapsed_ms:.1f} ms"
        )

    def _failed(self, message: str) -> None:
        self.session.processing_state = "idle"
        self.clean_button.setText("开始清洗")
        QMessageBox.critical(self, "处理失败", message)

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
        self.file_label.setText("未命名")

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
        name, _ = QFileDialog.getSaveFileName(
            self, "导出 Word", "CleanText_cleaned.docx", "Word (*.docx)"
        )
        if name:
            try:
                export_docx(self.output.toPlainText(), Path(name))
            except Exception as exc:
                QMessageBox.critical(self, "导出失败", str(exc))

    def toggle_theme(self) -> None:
        theme = Theme.DARK if self.theme_action.text() == "深色" else Theme.LIGHT
        self.apply_theme(theme)

    def toggle_settings_panel(self) -> None:
        self.settings_panel.setVisible(not self.settings_panel.isVisible())

    def apply_theme(self, theme: Theme) -> None:
        app = cast(QApplication | None, QApplication.instance())
        if app:
            app.setStyleSheet(stylesheet(theme))
        self.theme_action.setText("浅色" if theme == Theme.DARK else "深色")

    def show_settings(self) -> None:
        QMessageBox.information(
            self, "设置", f"CleanText Studio v{__version__}\n文本只在本机处理，不收集遥测。"
        )

    def show_help(self) -> None:
        QMessageBox.information(self, "帮助", "粘贴或打开文本，选择清洗规则，然后点击开始清洗。")

    def about(self) -> None:
        QMessageBox.about(self, "关于", f"净文排版 · CleanText Studio\nv{__version__}\nMIT License")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.settings_store.setValue("splitter_sizes", self.splitter.sizes())
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
