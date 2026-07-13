<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio Logo"></p>

# CleanText Studio

A local-first Windows app for text cleanup, document structure, math typesetting, and TXT/DOCX export.

[![Version](https://img.shields.io/badge/version-v1.3.2-4f46e5)](https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.3.2) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![License](https://img.shields.io/badge/license-MIT-green)

## Windows download

Download the x64 installer or portable package from the [v1.3.2 release](https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.3.2). Current version: **v1.3.2**. Developer: **SiriZhao**.

## v1.3.2 stability fixes

- Native inline Word OMML for formulas mixed with Chinese body text.
- No supported LaTeX delimiters or commands in normal Word text.
- Empty decorative Emoji columns and soft-line fragments are removed from tables.
- Preview and DOCX now use the same paragraph-run and table structure.

## Screenshots

| Inline math | Block and inline math |
|---|---|
| ![Inline math](assets/screenshots/inline-math-v1.3.2.png) | ![Block and inline math](assets/screenshots/block-and-inline-math-v1.3.2.png) |

## Formula rendering

![Table cleanup](assets/screenshots/table-clean-v1.3.2.png)

## Native Word equations

![Word table export](assets/screenshots/table-word-v1.3.2.png)

## Clean tables and formulas

![Export quality](assets/screenshots/export-quality-v1.3.2.png)

## Core features

Deterministic Markdown cleanup, structured headings/lists/quotes/code/tables/math, three paragraph modes, TXT/DOCX import/export, system/light/dark themes, and optional BYOK AI providers.

## Before and after

`**Formula:** \[S = k_B \ln \Omega\]` becomes clean text with a rendered preview and editable Word equation. Markdown headings, emphasis, separators, and table-cell markers are removed without flattening document structure.

## Formats and usage

Imports `.txt`, `.md`, `.markdown`, and `.docx`; exports UTF-8 TXT and structured DOCX. Paste or open text, choose a preset, clean, review in text/preview mode, and export.

## BYOK AI configuration

AI is optional and disabled by default. Keys are stored in Windows Credential Manager or session memory. The project does not provide keys, pay provider fees, or proxy model services.

## Offline mode and privacy

Cleanup, preview, TXT, and Word export work entirely offline. No telemetry or automatic text upload is used. Third-party handling applies only after the user explicitly invokes a configured API.

## Word and math support

Word export uses native headings, lists, tables, and OMML. Supported math includes `$`, `$$`, `\(\)`, `\[\]`, common equation/align/matrix/cases environments, scripts, fractions, roots, sums, integrals, relations, functions, Greek letters, and `\text{...}`. The app never evaluates or rewrites math semantics.

## Known limitations

Complex custom macros, uncommon environments, and deeply nested TeX may use readable text fallback. The lightweight preview is not a complete TeX engine. DOCX import does not preserve images or all advanced styles.

## Install, develop, test, and build

The installer uses per-user installation; the portable build needs no Python. For source development:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
.\.venv\Scripts\python -m cleantext_studio.main
.\.venv\Scripts\ruff check .
.\.venv\Scripts\mypy src/cleantext_studio
.\.venv\Scripts\pytest
.\scripts\build_windows.ps1
```

## Roadmap, contributing, developer, and license

Future work covers broader complex-math compatibility, templates, granular diff restoration, and accessibility. See [CONTRIBUTING.md](CONTRIBUTING.md). Developer: **SiriZhao** · [Repository](https://github.com/SiriZhao/CleanText-Studio). MIT licensed.

This project does not provide AI-detection evasion, plagiarism bypass, or academic misconduct features.
