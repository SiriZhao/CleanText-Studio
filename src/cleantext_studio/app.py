from __future__ import annotations

import sys
from pathlib import Path
from typing import cast

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QAction, QCloseEvent, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
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
from cleantext_studio.models import CleanOptions, CleanResult, CleanStats


class CleanWorker(QThread):
    completed = Signal(object)
    failed = Signal(str)

    def __init__(self, text: str, options: CleanOptions) -> None:
        super().__init__()
        self.text = text
        self.options = options

    def run(self) -> None:
        try:
            self.completed.emit(clean_text(self.text, self.options))
        except Exception as exc:
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"净文排版 CleanText Studio {__version__}")
        root = Path(getattr(sys, "_MEIPASS", Path(__file__).parents[3]))
        icon = root / "assets" / "icon.png"
        if icon.exists():
            self.setWindowIcon(QIcon(str(icon)))
        self.resize(1440, 900)
        self.current_file: Path | None = None
        self.worker: CleanWorker | None = None
        self.last_stats: CleanStats | None = None
        self.input = QPlainTextEdit()
        self.input.setPlaceholderText("在此粘贴原始文本，或打开 TXT / Markdown / DOCX 文件")
        self.output = QPlainTextEdit()
        self.output.setPlaceholderText("清洗结果将在此显示，并可继续编辑")
        self.remove_emoji = QCheckBox("删除表情符号")
        self.remove_emoji.setChecked(True)
        self.keep_bullets = QCheckBox("保留合法项目符号")
        self.keep_bullets.setChecked(False)
        self.template_phrases = QCheckBox("删除模板化提示语（谨慎）")
        rules = QWidget()
        rv = QVBoxLayout(rules)
        for w in (
            QLabel("基础清洗"),
            self.remove_emoji,
            self.keep_bullets,
            QLabel("结构整理"),
            self.template_phrases,
        ):
            rv.addWidget(w)
        rv.addStretch()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(rules)
        scroll.setMinimumWidth(240)
        left = QWidget()
        lv = QVBoxLayout(left)
        lv.addWidget(QLabel("原始文本"))
        lv.addWidget(self.input)
        right = QWidget()
        ov = QVBoxLayout(right)
        ov.addWidget(QLabel("清洗结果"))
        ov.addWidget(self.output)
        splitter = QSplitter()
        splitter.addWidget(left)
        splitter.addWidget(scroll)
        splitter.addWidget(right)
        splitter.setSizes([550, 260, 550])
        self.setCentralWidget(splitter)
        self._toolbar()
        self.statusBar().showMessage("就绪 · 文本仅在本机处理")
        self.input.textChanged.connect(self._counts)
        self.output.textChanged.connect(self._counts)

    def _toolbar(self) -> None:
        tb = QToolBar("工具栏")
        self.addToolBar(tb)
        actions = [
            ("新建", self.new),
            ("打开文件", self.open),
            ("粘贴", self.input.paste),
            ("开始清洗", self.start_clean),
            ("撤销", self.output.undo),
            ("恢复", self.output.redo),
            ("复制结果", self.output.copy),
            ("导出 TXT", self.save_txt),
            ("导出 Word", self.save_word),
            ("设置", self.settings),
            ("关于", self.about),
        ]
        for name, callback in actions:
            action = QAction(name, self)
            action.triggered.connect(callback)
            action.setToolTip(name)
            tb.addAction(action)

    def _counts(self) -> None:
        a, b = self.input.toPlainText(), self.output.toPlainText()
        self.statusBar().showMessage(
            f"原始字符 {len(a)} · 结果字符 {len(b)} · {'有未保存修改' if b else '就绪'}"
        )

    def new(self) -> None:
        if (
            self.output.document().isModified()
            and QMessageBox.question(self, "确认", "清空未保存内容？")
            != QMessageBox.StandardButton.Yes
        ):
            return
        self.input.clear()
        self.output.clear()
        self.current_file = None

    def open(self) -> None:
        name, _ = QFileDialog.getOpenFileName(
            self, "打开", "", "支持文件 (*.txt *.md *.markdown *.docx)"
        )
        if name:
            try:
                self.input.setPlainText(import_file(Path(name)))
                self.current_file = Path(name)
            except Exception as exc:
                QMessageBox.critical(self, "导入失败", str(exc))

    def start_clean(self) -> None:
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            return
        opts = CleanOptions(
            remove_emoji=self.remove_emoji.isChecked(),
            keep_bullets=self.keep_bullets.isChecked(),
            remove_template_phrases=self.template_phrases.isChecked(),
        )
        self.worker = CleanWorker(self.input.toPlainText(), opts)
        self.worker.completed.connect(self._cleaned)
        self.worker.failed.connect(lambda e: QMessageBox.critical(self, "处理失败", e))
        self.worker.start()
        self.statusBar().showMessage("正在清洗…再次点击可请求取消")

    def _cleaned(self, result: CleanResult) -> None:
        self.output.setPlainText(result.text)
        self.last_stats = result.stats
        self.statusBar().showMessage(
            f"完成 · 删除 {result.stats.removed_chars} 字符 · 合并 {result.stats.merged_linebreaks} 处 · {result.stats.elapsed_ms:.1f} ms"
        )

    def save_txt(self) -> None:
        name, _ = QFileDialog.getSaveFileName(
            self, "导出 TXT", "CleanText_cleaned.txt", "TXT (*.txt)"
        )
        if name:
            export_txt(self.output.toPlainText(), Path(name))
            self.output.document().setModified(False)

    def save_word(self) -> None:
        name, _ = QFileDialog.getSaveFileName(
            self, "导出 Word", "CleanText_cleaned.docx", "Word (*.docx)"
        )
        if name:
            try:
                export_docx(self.output.toPlainText(), Path(name))
                self.output.document().setModified(False)
            except Exception as exc:
                QMessageBox.critical(self, "导出失败", str(exc))

    def settings(self) -> None:
        QMessageBox.information(
            self,
            "设置",
            "浅色 / 深色 / 跟随系统及草稿选项将在配置目录中保存。\n文本默认只在本机处理，不收集遥测。",
        )

    def about(self) -> None:
        QMessageBox.about(
            self,
            "关于",
            f"净文排版 CleanText Studio v{__version__}\n本地优先的文本格式清洗与文档排版工具。\nMIT License",
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        if (
            self.output.document().isModified()
            and QMessageBox.question(self, "退出", "结果尚未保存，确定退出？")
            != QMessageBox.StandardButton.Yes
        ):
            event.ignore()
            return
        event.accept()


def create_app() -> tuple[QApplication, MainWindow]:
    app = cast(QApplication | None, QApplication.instance()) or QApplication([])
    app.setApplicationName("CleanText Studio")
    window = MainWindow()
    return app, window
