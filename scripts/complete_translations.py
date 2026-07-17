"""One-time catalog completion utility for v1.5.1.

It writes static JSON resources only; the application has no translation
service dependency and never contacts the network at runtime.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

from deep_translator import GoogleTranslator

ROOT = Path(__file__).parents[1]
CATALOG_DIR = ROOT / "src" / "cleantext_studio" / "i18n" / "translations"
TARGETS = {
    "zh_CN": "zh-CN", "zh_TW": "zh-TW", "ja_JP": "ja", "ko_KR": "ko",
    "es_ES": "es", "fr_FR": "fr", "de_DE": "de", "pt_BR": "pt",
    "ru_RU": "ru", "ar": "ar", "hi_IN": "hi",
}
EXTRA_ENGLISH = {
    "action.cancelling": "Cancelling…",
    "status.residual_count": " · {count} possible residual items detected",
    "statistics.summary": "This run: Markdown {markdown} · AI labels {ai} · blank lines {blank} · emoji {emoji} · headings {headings} · empty table columns {columns} · {elapsed:.1f} ms",
    "help.title": "Help",
    "dialog.ai.title": "AI optimization configuration",
    "dialog.ai.fetch_models": "Refresh models",
    "dialog.ai.restore_default": "Restore defaults",
    "dialog.ai.show_key": "Show key",
    "dialog.ai.advanced": "Show advanced settings",
    "dialog.ai.test_connection": "Test connection",
    "dialog.ai.testing": "Testing…",
    "dialog.ai.refreshing": "Refreshing…",
    "dialog.ai.custom_url": "Custom endpoint URL",
    "help.quick_start.title": "Quick start", "help.quick_start.body": "Paste or open text, choose a cleaning preset, then select Clean. Use Preview mode to inspect preserved structure before export.",
    "help.import.title": "Import text", "help.import.body": "Open TXT, Markdown, or DOCX files, or paste text from the clipboard. Local cleanup works without a network connection.",
    "help.cleaning.title": "Cleaning settings", "help.cleaning.body": "Use the preset as a starting point. Each option is local and can be adjusted without changing the source document.",
    "help.paragraphs.title": "Paragraphs and line breaks", "help.paragraphs.body": "Choose compact output, section-aware spacing, or preserved paragraph breaks according to your document layout.",
    "help.headings.title": "Headings and lists", "help.headings.body": "The app preserves detected headings and lists so that structured export can recreate them in Word.",
    "help.tables.title": "Tables", "help.tables.body": "Markdown tables are parsed as document structure. Preview and Word export use the same cleaned table model.",
    "help.math.title": "Math formulas", "help.math.body": "Supported formulas are protected during cleanup. Word export uses native equations when conversion is available and preserves readable fallback text otherwise.",
    "help.word.title": "Word export", "help.word.body": "Word export preserves headings, lists, tables, and supported formulas. Review the export summary before saving.",
    "help.ai.title": "AI configuration", "help.ai.body": "AI optimization is optional. Bring your own provider and API key; local cleanup never sends text to an online service.",
    "help.privacy.title": "Privacy and security", "help.privacy.body": "Basic cleanup is performed locally. API requests are only made after you explicitly configure and use an AI provider.",
    "help.faq.title": "FAQ", "help.faq.body": "If a document contains unusual markup, review Preview mode and residual warnings before exporting. Complex LaTeX macros may remain readable text.",
    "dialog.open": "Open", "dialog.overwrite": "Overwrite", "dialog.clear_confirmation": "Clear the current content?", "dialog.exit_confirmation": "The result has unsaved changes. Exit anyway?",
    "dialog.export_word_title": "Export Word", "dialog.export_txt_title": "Export TXT", "dialog.import_failed": "Import failed", "dialog.export_failed": "Export failed", "dialog.processing_failed": "Processing failed",
    "status.cleaning": "Cleaning…", "status.exported_word": "Word export completed", "status.exported_txt": "TXT export completed", "status.file_open_failed": "Could not open the file", "status.file_busy": "The file is in use",
    "about.title": "About CleanText Studio", "about.copy_version": "Copy version information", "about.details": "Version: v{version}\nDeveloper: SiriZhao\n\nA local-first text cleanup, document-structure, and Word/TXT formatting tool.\n\nProject homepage: {repository}\n\nCopyright © 2026 SiriZhao. All rights reserved.\nLicense: MIT License\n\nBasic cleanup is performed locally. AI optimization only calls a third-party API that you configure yourself.",
    "about.license_message": "CleanText Studio is distributed under the MIT License. See the repository LICENSE file for the complete text.", "about.open_failed": "Copy this project address: {repository}",
    "tip.detect_math": "Detect LaTeX, Unicode, and common equations before text cleaning.", "tip.protect_math": "Protect delimiters, subscripts, and commands before Markdown cleaning.", "tip.normalize_math": "Fix only clear formula spacing; never calculate or rewrite math.", "tip.repair_math": "Repair a formula delimiter only when the correction is unambiguous.", "tip.word_omml": "Convert supported formulas to native Word equations; complex formulas use a safe fallback.", "tip.math_output": "Choose how formulas are represented in cleaned text and TXT output.",
}


def protect(value: str) -> tuple[str, dict[str, str]]:
    """Use numeric placeholders; some translator endpoints reject braces."""
    tokens = list(dict.fromkeys(re.findall(r"\{[^}]+\}", value)))
    replacements = {str(900000 + index): token for index, token in enumerate(tokens)}
    for marker, token in replacements.items():
        value = value.replace(token, marker)
    return value, replacements


def restore(value: str, replacements: dict[str, str]) -> str:
    for marker, token in replacements.items():
        value = value.replace(marker, token)
    return value


def translate(locale: str, values: dict[str, str]) -> dict[str, str]:
    translator = GoogleTranslator(source="en", target=TARGETS[locale])
    output: dict[str, str] = {}
    prepared = [(key, *protect(value)) for key, value in values.items()]
    for start in range(0, len(prepared), 20):
        batch = prepared[start : start + 20]
        try:
            translated = translator.translate_batch([item[1] for item in batch])
        except Exception as exc:  # network errors must be visible to release work
            raise RuntimeError(f"translation batch failed for {locale}") from exc
        for (key, _source, replacements), value in zip(batch, translated, strict=True):
            output[key] = restore(value, replacements)
        time.sleep(0.2)
    return output


def main() -> int:
    en_path = CATALOG_DIR / "en_US.json"
    english = json.loads(en_path.read_text(encoding="utf-8"))
    english.update(EXTRA_ENGLISH)
    en_path.write_text(json.dumps(english, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    requested = tuple(sys.argv[1:]) or tuple(TARGETS)
    invalid = set(requested) - set(TARGETS)
    if invalid:
        raise SystemExit(f"unknown locales: {sorted(invalid)}")
    for locale in requested:
        path = CATALOG_DIR / f"{locale}.json"
        existing = json.loads(path.read_text(encoding="utf-8"))
        missing = {key: value for key, value in english.items() if key not in existing}
        if missing:
            existing.update(translate(locale, missing))
        path.write_text(json.dumps(existing, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"{locale}: {len(existing)}/{len(english)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
