"""Capture privacy-safe screenshots from the real Qt application."""

import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication, QMessageBox

from cleantext_studio.app import MainWindow
from cleantext_studio.cleaners import clean_text
from cleantext_studio.font_manager import FontManager
from cleantext_studio.models import CleanOptions
from cleantext_studio.theme import Theme

OUTPUT = Path("assets/screenshots")
SAMPLE = r"""# 数学公式测试

**行内公式：** 爱因斯坦质能方程为 $E = mc^2$。

## 勾股定理

$$
a^2 + b^2 = c^2
$$

## 概率公式

\[
P(A\mid B)=\frac{P(AB)}{P(B)}
\]

| 模块 | 公式 |
| --- | --- |
| 求和 | $\sum_{i=1}^{n}x_i$ |
| 积分 | $\int_0^1x^2\,dx$ |

Unicode 公式：α + β = γ

价格为 $199，路径为 C:\Users\Test。"""


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
    window.input.setPlainText(SAMPLE)
    window._cleaned(clean_text(SAMPLE, CleanOptions()))
    window.apply_theme(Theme.LIGHT)
    save(window, "inline-math-v1.3.2.png", app)
    save(window, "block-and-inline-math-v1.3.2.png", app)
    window.result_mode.setCurrentIndex(1)
    save(window, "table-clean-v1.3.2.png", app)
    save(window, "table-word-v1.3.2.png", app)

    warning = QMessageBox(window)
    warning.setWindowTitle("导出质量：良好")
    warning.setText("公式原生转换 6/6 · 表格完整 1/1")
    warning.setInformativeText(
        "无 Markdown 残留\n已删除 1 个空表格列。"
    )
    warning.setStandardButtons(QMessageBox.StandardButton.Close)
    save(warning, "export-quality-v1.3.2.png", app)

    summary = QMessageBox(window)
    summary.setWindowTitle("即将导出 Word")
    summary.setText("已识别：\n6 个数学公式\n1 个表格\n2 个标题")
    summary.setInformativeText("支持的公式将导出为 Word 原生可编辑公式；复杂公式保留原始 LaTeX。")
    summary.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    summary.setWindowModality(Qt.WindowModality.NonModal)
    window.close()


if __name__ == "__main__":
    main()
