# GitHub launch copy

## Title

**CleanText Studio - Privacy-first AI Text Cleanup & Document Formatting Tool**

## Short description

CleanText Studio is a local-first Windows app that cleans copied and AI-assisted
text, restores document structure, preserves supported LaTeX formulas, and
exports polished DOCX or TXT files.

## Long description

Copied pages and AI-assisted drafts often arrive with Markdown residue, uneven
paragraphs, flattened lists, fragile tables, and formulas that do not travel
well to Word. CleanText Studio keeps the useful structure instead of treating a
document as plain characters. It provides configurable local cleanup, Text and
Preview modes, native Word tables, and supported editable Office Math (OMML)
export.

The core workflow is offline and local. AI refinement is optional; it only uses
a provider and API key supplied by the user. The repository includes Windows
installer and portable release assets, a multilingual UI, tests, and document
quality checks.

## Features

- Markdown, decorative-symbol, and fragmented-label cleanup.
- Paragraph, heading, list, link, and standalone-URL handling.
- Markdown-table recognition and native DOCX table export.
- Supported LaTeX detection, normalization, preview, and editable OMML export.
- DOCX and UTF-8 TXT export.
- Runtime language switching and light/dark themes.
- Optional BYOK AI refinement without a shared project API key.

## Why this matters

Document cleanup is usually either a manual formatting task or a cloud service.
CleanText Studio focuses on a third path: a transparent desktop workflow that
keeps ordinary cleanup and export on the user's machine while retaining the
structure required for a professional Word document.

## Technical highlights

- Python + PySide6 desktop application.
- Structured document blocks shared by cleanup and export paths.
- LaTeX subset parsed into an AST and emitted as native Word OMML where supported.
- Regression coverage for cleanup behavior, formulas, UI localization, and docs.
- Windows CI runs Ruff, MyPy, translations, screenshot checks, freeze checks,
  tests, and packaging.

## Screenshot recommendation

Lead with `assets/screenshots/01-main-light.png`, then show formula handling
with `06-formula-rendering.png`, cleanup settings with `03-settings.png`, and
DOCX export confirmation with `05-word-export.png`. Use only the current,
privacy-safe assets committed in this repository.

## Call to action

Try the latest Windows release, open an issue with a minimal reproducible
document sample when behavior is wrong, or contribute a focused fix,
translation review, test, or documentation improvement.
