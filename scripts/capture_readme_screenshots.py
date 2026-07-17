"""Capture the v1.5.1 README images from the real Qt application.

The script intentionally uses the native Windows Qt platform, not ``offscreen``:
the latter can omit Windows CJK fallback fonts and produce tofu in PNG output.
All sample material is public, synthetic text and no provider credentials are
inserted into a dialog.
"""

from __future__ import annotations

import time
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QEvent, QRect
from PySide6.QtGui import QColor, QPainter, QPalette, QPixmap
from PySide6.QtWidgets import QApplication

from cleantext_studio.about_dialog import AboutDialog
from cleantext_studio.ai_dialogs import ProviderDialog
from cleantext_studio.app import MainWindow
from cleantext_studio.cleaners import clean_text
from cleantext_studio.font_manager import FontManager
from cleantext_studio.help_dialog import HelpDialog
from cleantext_studio.models import CleanOptions
from cleantext_studio.theme import Theme

ROOT = Path(__file__).parents[1]
OUTPUT = ROOT / "assets" / "screenshots" / "v1.5.1"
WINDOW_SIZE = (1440, 900)
MIN_BYTES = 20_000

SAMPLE_EN = r"""# CleanText Studio research notes

---

**Purpose:** turn copied material into a readable document. ✨

- Preserve meaningful headings and lists
- Remove decorative formatting residue

| Area | Result | Notes |
| --- | --- | --- |
| Tables | Native Word table | Clean cell text |
| Mathematics | \( E = mc^2 \) | Editable when supported |

\[
S = k_B \ln \Omega
\]

https://example.com/reference
"""

SAMPLE_ZH = r"""# 净文排版示例

---

**目标：** 将复制文本整理为可编辑文档。 ✨

- 保留有意义的标题和列表
- 清理装饰符号与冗余格式

| 功能 | 结果 | 说明 |
| --- | --- | --- |
| 表格 | Word 原生表格 | 清理单元格文本 |
| 公式 | \( E = mc^2 \) | 支持时可编辑 |

\[
S = k_B \ln \Omega
\]

https://example.com/reference
"""

SAMPLE_BY_LOCALE = {
    "en_US": SAMPLE_EN,
    "zh_CN": SAMPLE_ZH,
    "zh_TW": SAMPLE_ZH.replace("净文", "淨文").replace("标题", "標題").replace("列表", "清單").replace("清理", "清理"),
    "ja_JP": "# 文書整理の例\n\n**目的:** コピーした文章を編集可能な文書に整理します。\n\n- 見出しとリストを保持する\n- 装飾記号を削除する\n\nhttps://example.com/reference\n",
    "ko_KR": "# 문서 정리 예시\n\n**목적:** 복사한 텍스트를 편집 가능한 문서로 정리합니다.\n\n- 의미 있는 제목과 목록 유지\n- 장식 기호 제거\n\nhttps://example.com/reference\n",
    "es_ES": "# Ejemplo de limpieza de documento\n\n**Objetivo:** convertir texto copiado en un documento editable.\n\n- Conservar títulos y listas útiles\n- Eliminar símbolos decorativos\n\nhttps://example.com/reference\n",
    "fr_FR": "# Exemple de nettoyage de document\n\n**Objectif :** transformer un texte copié en document modifiable.\n\n- Conserver les titres et les listes utiles\n- Supprimer les symboles décoratifs\n\nhttps://example.com/reference\n",
    "de_DE": "# Beispiel für Dokumentbereinigung\n\n**Ziel:** kopierten Text in ein bearbeitbares Dokument verwandeln.\n\n- Sinnvolle Überschriften und Listen erhalten\n- Dekorative Symbole entfernen\n\nhttps://example.com/reference\n",
    "pt_BR": "# Exemplo de limpeza de documento\n\n**Objetivo:** transformar texto copiado em um documento editável.\n\n- Preservar títulos e listas úteis\n- Remover símbolos decorativos\n\nhttps://example.com/reference\n",
    "ru_RU": "# Пример очистки документа\n\n**Цель:** превратить скопированный текст в редактируемый документ.\n\n- Сохранить полезные заголовки и списки\n- Удалить декоративные символы\n\nhttps://example.com/reference\n",
    "ar": "# مثال لتنظيف مستند\n\n**الهدف:** تحويل النص المنسوخ إلى مستند قابل للتحرير.\n\n- الاحتفاظ بالعناوين والقوائم المفيدة\n- إزالة الرموز الزخرفية\n\nhttps://example.com/reference\n",
    "hi_IN": "# दस्तावेज़ सफाई उदाहरण\n\n**लक्ष्य:** कॉपी किए गए पाठ को संपादन योग्य दस्तावेज़ में बदलना।\n\n- उपयोगी शीर्षक और सूचियाँ सुरक्षित रखना\n- सजावटी चिह्न हटाना\n\nhttps://example.com/reference\n",
}

TABLE_SAMPLE = """# Table export example

| Topic | Export result | Note |
| --- | --- | --- |
| Headings | Preserved | Readable structure |
| Tables | Native Word table | Clean cell text |
| Formulas | Editable when supported | OMML output |
"""

MATH_SAMPLE = r"""# Formula preview example

The entropy relation is \( S = k_B \ln \Omega \).

\[
\frac{dO}{dt}=I-\lambda O+\xi(t)
\]
"""

LOCALE_SHOTS = {
    "en_US": "hero-main-en.png",
    "zh_CN": "hero-main-zh-cn.png",
    "zh_TW": "main-zh-tw.png",
    "ja_JP": "main-ja.png",
    "ko_KR": "main-ko.png",
    "es_ES": "main-es.png",
    "fr_FR": "main-fr.png",
    "de_DE": "main-de.png",
    "pt_BR": "main-pt-br.png",
    "ru_RU": "main-ru.png",
    "ar": "main-ar-rtl.png",
    "hi_IN": "main-hi.png",
}


def pump(app: QApplication, milliseconds: int = 180) -> None:
    deadline = time.monotonic() + milliseconds / 1_000
    while time.monotonic() < deadline:
        app.processEvents()


def save(widget: object, path: Path, app: QApplication, background: QColor | None = None) -> None:
    window = widget
    window.show()  # type: ignore[attr-defined]
    pump(app)
    pixmap = window.grab()  # type: ignore[attr-defined]
    if background is not None:
        composed = QPixmap(pixmap.size())
        composed.fill(background)
        painter = QPainter(composed)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        pixmap = composed
    if not pixmap.save(str(path), "PNG"):
        raise RuntimeError(f"could not write {path}")
    window.hide()  # type: ignore[attr-defined]


def save_crop(widget: MainWindow, rect: QRect, path: Path, app: QApplication) -> None:
    widget.show()
    pump(app)
    ratio = widget.devicePixelRatioF()
    pixmap: QPixmap = widget.grab()
    crop = pixmap.copy(QRect(
        int(rect.x() * ratio), int(rect.y() * ratio),
        int(rect.width() * ratio), int(rect.height() * ratio),
    ))
    if not crop.save(str(path), "PNG"):
        raise RuntimeError(f"could not write {path}")


def set_locale(window: MainWindow, locale: str, app: QApplication) -> None:
    window.i18n.set_language(locale)
    app.setFont(FontManager(locale=locale).application_font())
    pump(app)


def clean_sample(window: MainWindow, sample: str, app: QApplication) -> None:
    window.input.setPlainText(sample)
    window._cleaned(clean_text(sample, CleanOptions()))
    # Preview widgets are replaced with deleteLater(); flush that queue before
    # grabbing so an old table cannot be composited into a new capture.
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    pump(app, 120)


def validate() -> None:
    expected = set(LOCALE_SHOTS.values()) | {
        "hero-main-dark-en.png", "cleaning-before-after.png", "table-preview.png",
        "math-preview.png", "help-en.png", "help-zh-cn.png", "about-en.png",
        "about-zh-cn.png", "ai-settings.png", "export-summary.png",
        "rounded-ui-details.png",
    }
    missing = [name for name in sorted(expected) if not (OUTPUT / name).exists()]
    small = [name for name in sorted(expected) if (OUTPUT / name).exists()
             and (OUTPUT / name).stat().st_size < MIN_BYTES]
    if missing or small:
        raise RuntimeError(f"bad screenshot set; missing={missing}, too_small={small}")


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    app.setApplicationName("CleanText Studio")
    app.setFont(FontManager(locale="en_US").application_font())
    window = MainWindow()
    window.resize(*WINDOW_SIZE)
    window.show()
    pump(app, 300)

    for locale, name in LOCALE_SHOTS.items():
        set_locale(window, locale, app)
        clean_sample(window, SAMPLE_BY_LOCALE[locale], app)
        window.result_mode.setCurrentIndex(0)
        save(window, OUTPUT / name, app)

    set_locale(window, "en_US", app)
    window.apply_theme(Theme.DARK)
    clean_sample(window, SAMPLE_EN, app)
    window.result_mode.setCurrentIndex(0)
    save(window, OUTPUT / "hero-main-dark-en.png", app)
    window.apply_theme(Theme.LIGHT)

    clean_sample(window, SAMPLE_EN, app)
    window.result_mode.setCurrentIndex(0)
    save(window, OUTPUT / "cleaning-before-after.png", app)
    clean_sample(window, TABLE_SAMPLE, app)
    window.result_mode.setCurrentIndex(1)
    save(window, OUTPUT / "table-preview.png", app)
    clean_sample(window, MATH_SAMPLE, app)
    window.result_mode.setCurrentIndex(1)
    save(window, OUTPUT / "math-preview.png", app)

    set_locale(window, "en_US", app)
    save(HelpDialog(window.i18n, window), OUTPUT / "help-en.png", app)
    save(AboutDialog(window.i18n, window), OUTPUT / "about-en.png", app)
    set_locale(window, "zh_CN", app)
    save(HelpDialog(window.i18n, window), OUTPUT / "help-zh-cn.png", app)
    save(AboutDialog(window.i18n, window), OUTPUT / "about-zh-cn.png", app)

    set_locale(window, "en_US", app)
    ai = ProviderDialog(window)
    # ProviderDialog is intentionally transparent around its layout; a native
    # window grab otherwise encodes that transparent area as black.  Give the
    # real dialog the same application-window surface for the capture only.
    palette = ai.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#f5f7fb"))
    ai.setPalette(palette)
    ai.setAutoFillBackground(True)
    save(ai, OUTPUT / "ai-settings.png", app, QColor("#f5f7fb"))
    # Export information is represented by the actual cleaned-result state and
    # result toolbar, not a fabricated design mockup.
    clean_sample(window, SAMPLE_EN, app)
    save(window, OUTPUT / "export-summary.png", app)

    settings = window.settings_panel.geometry()
    save_crop(window, settings.adjusted(0, 0, 0, 0), OUTPUT / "rounded-ui-details.png", app)
    window.close()
    validate()
    print(f"Captured {len(list(OUTPUT.glob('*.png')))} README screenshots in {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
