"""Capture privacy-safe screenshots from the real Qt application."""

import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication, QMessageBox

from cleantext_studio.about_dialog import AboutDialog
from cleantext_studio.ai_dialogs import ProviderDialog
from cleantext_studio.app import MainWindow
from cleantext_studio.cleaners import clean_text
from cleantext_studio.font_manager import FontManager
from cleantext_studio.models import CleanOptions
from cleantext_studio.theme import Theme

OUTPUT = Path("assets/screenshots")
SAMPLE = """### 禾小二 FieldGPT 创业方案

填写：

项目概述

---

| 模块 | 功能 |
| --- | --- |
| AI 病虫害识别 | 拍照识别病害、虫害和草害 |
| 农事处方生成 | 提供用药建议与风险提示 |

## 服务对象

- 农户
- 合作社

> 本工具用于本地文本清理和文档排版。
"""


def save(widget: object, name: str, app: QApplication) -> None:
    widget.show()  # type: ignore[attr-defined]
    app.processEvents()
    widget.grab().save(str(OUTPUT / name), "PNG")  # type: ignore[attr-defined]
    widget.hide()  # type: ignore[attr-defined]


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    system_font = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "msyh.ttc"
    if system_font.exists():
        QFontDatabase.addApplicationFont(str(system_font))
    app.setFont(FontManager().application_font())
    window = MainWindow()
    window.resize(1440, 900)
    window.preset.setCurrentText("深度清洗")
    window.input.setPlainText(SAMPLE)
    result = clean_text(SAMPLE, CleanOptions(clean_instructional_labels=True))
    window._cleaned(result)

    window.apply_theme(Theme.LIGHT)
    save(window, "main-light-v1.2.2.png", app)
    save(window, "cleaning-before-after-v1.2.2.png", app)
    window.result_mode.setCurrentIndex(1)
    save(window, "table-preview-v1.2.2.png", app)

    window.apply_theme(Theme.DARK)
    save(window, "main-dark-v1.2.2.png", app)
    window.apply_theme(Theme.LIGHT)

    provider = ProviderDialog(window)
    save(provider, "ai-config-v1.2.2.png", app)
    about = AboutDialog(window)
    save(about, "about-v1.2.2.png", app)

    residual = QMessageBox(window)
    residual.setWindowTitle("可能的格式残留")
    residual.setText("检测到 2 处可能残留")
    residual.setInformativeText("第 12 行 · Markdown 强调标记\n第 24 行 · 未解析表格行")
    residual.setStandardButtons(QMessageBox.StandardButton.Close)
    save(residual, "residual-warning-v1.2.2.png", app)

    summary = QMessageBox(window)
    summary.setWindowTitle("即将导出 Word")
    summary.setText("已识别：\n✓ 2 个标题\n✓ 2 个列表\n✓ 1 个表格\n✓ 1 个引用")
    summary.setInformativeText("推荐导出 Word，可完整保留标题、列表和表格结构。")
    summary.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    summary.setWindowModality(Qt.WindowModality.NonModal)
    save(summary, "word-export-summary-v1.2.2.png", app)
    window.close()


if __name__ == "__main__":
    main()
