<p align="center">
  <img src="assets/icon.png" width="96" alt="CleanText Studio logo">
</p>

<h1 align="center">CleanText Studio</h1>

<p align="center"><strong>Local-first text cleanup, document structure recovery, formula-aware preview, and polished DOCX/TXT export for copied and AI-generated text.</strong></p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.de.md">Deutsch</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.hi.md">हिन्दी</a>
</p>

<p align="center">
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.5.1"><img src="https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver" alt="Latest release"></a>
  <a href="https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml"><img src="https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Windows-x64-0078D4" alt="Windows x64">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2ea44f" alt="MIT License"></a>
</p>

> **Current release: v1.5.1 · Windows x64 · local-first by default**

<p align="center">
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.1/CleanText-Studio-v1.5.1-Windows-x64-Setup.exe"><strong>Download installer</strong></a> ·
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.1/CleanText-Studio-v1.5.1-Windows-x64-Portable.zip"><strong>Download portable ZIP</strong></a> ·
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.1/SHA256SUMS.txt">SHA256 checksums</a>
</p>

![CleanText Studio English interface](assets/screenshots/v1.5.1/hero-main-en.png)

CleanText Studio turns messy copied text into a readable, editable document without treating useful structure as noise. It removes redundant Markdown and decoration, recovers headings, lists, tables and common mathematical notation, then gives you a text view, a structured preview, and DOCX or TXT export. Basic cleanup is performed on the device; optional AI optimization uses only an API provider that you configure yourself.

**Why it is useful**

- Keep the meaning while removing visual residue from web pages, chats, notes, and generated drafts.
- Preserve a document model so headings, tables, links, and formulas do not silently flatten before export.
- Review the result before writing a native Word table, editable equation, or UTF-8 text file.
- Switch the interface language and theme at runtime without changing the source, result, or cleanup settings.

## Download for Windows

CleanText Studio v1.5.1 is released for **Windows x64**. Choose the installer for a normal per-user installation, or choose the portable ZIP when you prefer to run from an extracted folder. Neither package requires a separate Python installation.

| Package | Intended use | Download |
| --- | --- | --- |
| Setup | Install, Start-menu entry, and uninstall support | [CleanText-Studio-v1.5.1-Windows-x64-Setup.exe](https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.1/CleanText-Studio-v1.5.1-Windows-x64-Setup.exe) |
| Portable | Run after extracting the ZIP; no installation | [CleanText-Studio-v1.5.1-Windows-x64-Portable.zip](https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.1/CleanText-Studio-v1.5.1-Windows-x64-Portable.zip) |
| Verification | Check the downloaded package | [SHA256SUMS.txt](https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.1/SHA256SUMS.txt) |

The release page is the source of truth for available files: [CleanText Studio v1.5.1](https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.5.1).

## What CleanText Studio does

### Built for practical document cleanup

Copied content often arrives with headings written as markers, repeated separators, decorative emoji, broken line wraps, tutorial labels, pasted links, or tables that are only visually tabular. CleanText Studio makes those choices explicit instead of applying a hidden one-size-fits-all rewrite. Pick a preset, inspect the result, and export only after the structure looks right.

### Typical scenarios

- Normalize research notes, meeting notes, knowledge-base extracts, and web-page copy.
- Prepare AI-assisted drafts for editing and professional document delivery.
- Recover a Markdown table before sending it as a native Word table.
- Preserve simple inline and block mathematics while removing surrounding formatting noise.
- Create a clean TXT handoff when a Word layout is unnecessary.

## Core capabilities

### Markdown and formatting cleanup

The cleanup pipeline can remove Markdown heading markers, emphasis markers, inline-code markers, image syntax, horizontal rules, copied HTML residue, decorative symbols, emoji, and fragmented instructional labels. It preserves ordinary text and makes cleanup options visible in the settings panel.

### Document structure recovery

Headings, lists, quotations, code blocks, paragraphs, tables, links, and mathematical blocks are represented as document structure rather than being blindly collapsed into a character stream. This is why preview and export can make the same structural decisions.

### Headings and lists

Choose whether to preserve markers, naturalize a structure, or remove markers where appropriate. The tool is designed to retain useful hierarchy and list semantics; it is not a generic rewriter that invents a new outline.

### Paragraphs and line breaks

Three modes cover common source material:

| Mode | Use it when |
| --- | --- |
| Compact | You want ordinary wrapped source lines joined into compact paragraphs. |
| Smart sections | You want natural paragraph spacing while retaining meaningful section breaks. |
| Preserve all | You need the source paragraph boundaries kept as closely as possible. |

### Links and standalone URLs

Link handling can keep Markdown, keep display text only, or preserve display text together with its URL. Standalone URLs can be retained, merged with the preceding paragraph, or removed when they are only tutorial residue. URLs are handled deliberately rather than disappearing as a side effect of Markdown cleanup.

## Tables, equations, and preview

### Markdown tables and Word tables

Markdown tables are parsed into structured table blocks. Preview mode displays the table as a table, and DOCX export creates a native Word table with a header row, readable cell content, borders, and widths chosen from content rather than a fixed equal split. Markdown separator rows, residual emphasis markers, meaningless empty columns, and accidental soft line breaks are cleaned before export when the active cleanup settings allow it.

![Structured table preview](assets/screenshots/v1.5.1/table-preview.png)

### Math formulas and editable Word equations

Common inline and display LaTeX delimiters, Unicode mathematical expressions, and simple equations are protected while surrounding text is cleaned. Supported formulas are emitted as Word OMML native equations, so common variables and expressions remain editable in Word. Formula spacing, obvious delimiter issues, and formula numbering can be normalized according to the selected options.

Complex custom macros are not silently discarded. When a formula is outside the supported conversion range, the application keeps a readable fallback and reports it in the export quality information.

![Formula-aware preview](assets/screenshots/v1.5.1/math-preview.png)

### Text mode and preview mode

Text mode is useful for reviewing the normalized plain result. Preview mode shows headings, lists, tables, links, and formulas in a document-oriented form. Switching display mode does not rerun cleanup or change your result.

## Before and after

The following compact example shows the kind of residue the application is designed to clean while preserving useful content.

**Source**

```markdown
### **Project notes** ✨
---
Read the **draft** first.

- Keep the main conclusion
- Remove decorative labels

| Item | Value |
| --- | --- |
| Formula | \( E = mc^2 \) |

https://example.com/reference
```

**Result concept**

```text
Project notes

Read the draft first.

• Keep the main conclusion
• Remove decorative labels

The table and E = mc² formula remain structured in Preview and DOCX export.
```

![Source and cleaned result](assets/screenshots/v1.5.1/cleaning-before-after.png)

## Export formats

### Export Word

Choose Word export when the destination needs headings, lists, tables, and supported formulas as editable document elements. The exporter produces a `.docx` file; it does not automate a locally installed Word application. Before export, the app can show a structure and quality summary so that recoverable formula/table limitations are visible.

### Export TXT

Choose TXT for a portable UTF-8 plain-text result. TXT export preserves the normalized textual content, but cannot represent Word-native tables or editable OMML equations as rich document objects.

| Input | Output |
| --- | --- |
| TXT, Markdown, MD, DOCX | UTF-8 TXT and structured DOCX |

## Languages, themes, and accessibility

The desktop interface offers Simplified Chinese, Traditional Chinese, English, Japanese, Korean, Spanish, French, German, Brazilian Portuguese, Russian, Arabic, and Hindi. Language changes are applied at runtime and retain text, results, current selections, and undo history. Arabic uses a right-to-left interface while technical values such as URLs, API keys, and code remain readable left-to-right.

Light and dark themes share the same panel, control, focus, and rounded-surface system. The application uses legal system-font fallbacks where available; it does **not** bundle Apple PingFang files.

![Dark theme and rounded surfaces](assets/screenshots/v1.5.1/rounded-ui-details.png)

## Optional AI optimization (BYOK)

AI optimization is optional. Basic cleanup, preview, TXT export, and DOCX export are available without a network connection. When you deliberately enable AI optimization, you choose a supported provider, endpoint, model, and your own API key. The application does not provide a shared free API key or proxy your provider account.

DeepSeek and other providers exposed by the installed application configuration can be selected through the AI settings dialog. Provider and model identifiers remain separate from translated display labels. Review the provider’s own data terms before sending sensitive material.

![AI configuration](assets/screenshots/v1.5.1/ai-settings.png)

## Quick start

1. Launch CleanText Studio and paste text, or open a supported file.
2. Choose a cleaning preset and adjust only the options needed for this document.
3. Click **Clean**, then inspect Text mode or Preview mode.
4. Export to Word for structured delivery, or TXT for a normalized plain-text file.
5. If needed, configure your own AI provider and consciously choose when to send text to it.

### Installer or portable version

- **Installer:** run the Setup executable, follow the installer, and launch CleanText Studio from the Start menu. Use Windows Apps settings or the uninstaller to remove it.
- **Portable:** extract the ZIP to a writable folder and start the executable inside it. Keep the extracted files together; do not run it directly from a compressed archive.

### Complete workflow

1. Put source text in the left panel.
2. Use the center panel to decide how Markdown, links, paragraphs, lists, and formulas are handled.
3. Review the cleaned result at right and use Preview for tables and equations.
4. Use the result toolbar to copy, undo, restore the most recent result, clear, export TXT, or export Word.
5. Keep a copy of the original source whenever the document has legal, archival, or publication significance.

## Privacy, security, and data flow

### Local-first basic processing

Basic cleanup runs locally. The application has no account system, advertising service, telemetry service, or shared public API key. Your text is not uploaded merely because it is pasted, previewed, cleaned, or exported locally.

### AI requests are opt-in

Only an explicit AI optimization action uses the third-party provider you configure. The provider receives the material needed for that request under its own terms. Do not use a provider request for material you are not entitled to share.

### API key handling

API keys are user-provided and are not written into exported document configuration. On Windows, the application uses its configured credential-storage mechanism when available; if secure credential storage is unavailable, it falls back safely rather than silently exporting a plaintext key. Treat your operating-system account and provider credentials as security boundaries.

## System requirements

- Windows x64.
- A current supported Windows desktop environment.
- No separately installed Python runtime for release packages.
- Internet access is optional and only needed for GitHub downloads, optional AI use, or links opened by the user.

Windows SmartScreen can show a reputation warning for a new unsigned or low-reputation build. Download only from the repository release page, verify the SHA256 checksum, and follow your organization’s software-installation policy.

## Technical stack and project architecture

CleanText Studio is a Python desktop application using PySide6 for the interface, python-docx for DOCX writing, PyInstaller for portable packaging, Inno Setup for the Windows installer, and pytest/Ruff/mypy for quality checks. The cleanup and document-block model sit below the presentation layer, allowing text, preview, and export to consume the same normalized structure.

```text
src/cleantext_studio/
├── app.py                 # desktop window and presentation wiring
├── cleaners/              # stable text-cleaning pipeline
├── math/                  # detection, parsing, preview, and OMML support
├── exporters/             # DOCX and TXT exporters
├── i18n/                  # locale catalogs and runtime translation service
├── ui/                    # cards, controls, and theme components
└── llm/                   # optional provider configuration and requests
assets/                    # icon, screenshots, and packaged resources
scripts/                   # validation, screenshot, and Windows-build helpers
tests/                     # unit, GUI, integration, and regression checks
```

## Run from source

The following commands match the repository’s development layout on PowerShell.

```powershell
git clone https://github.com/SiriZhao/CleanText-Studio.git
cd CleanText-Studio
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```

## Test and build

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\ruff check .
.\.venv\Scripts\mypy src/cleantext_studio
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python scripts/check_translations.py
.\.venv\Scripts\python scripts/check_readme_quality.py
.\.venv\Scripts\python scripts/check_screenshot_quality.py
.\.venv\Scripts\python scripts/verify_cleaning_freeze.py
.\scripts\build_windows.ps1
```

The Windows build writes its current artifacts, checksums, and release notes to `dist/`. Build output is intentionally not committed to the repository.

## Release artifacts and SHA256 verification

Each release provides the Setup executable, Portable ZIP, `SHA256SUMS.txt`, and release notes when available. In PowerShell, compare a downloaded artifact with the published checksum:

```powershell
Get-FileHash .\CleanText-Studio-v1.5.1-Windows-x64-Setup.exe -Algorithm SHA256
Get-Content .\SHA256SUMS.txt
```

## Internationalization and translation contributions

The official locale catalogs are `zh_CN`, `zh_TW`, `en_US`, `ja_JP`, `ko_KR`, `es_ES`, `fr_FR`, `de_DE`, `pt_BR`, `ru_RU`, `ar`, and `hi_IN`. See [docs/TRANSLATION_GLOSSARY.md](docs/TRANSLATION_GLOSSARY.md) and [docs/README_TRANSLATION_STATUS.md](docs/README_TRANSLATION_STATUS.md) before proposing terminology changes. Community translation review is welcome; this repository does not claim that every documentation translation has received native-speaker review.

## Roadmap

The current public release is Windows x64. Future platform work, richer import fidelity, and broader formula coverage are roadmap topics rather than current shipping claims. Feature requests and issue reports are welcome, but a roadmap item is not a commitment or release announcement.

## Known limitations

- Complex custom LaTeX macros can require a readable fallback instead of native Word equation conversion.
- DOCX import cannot preserve every original style, embedded object, or layout feature from arbitrary Word files.
- TXT cannot encode rich Word-native tables or editable equations.
- Optional AI output is produced by the third-party provider you select and requires human review.
- Windows packaging is the only published platform stated here; macOS, Linux, Android, and iOS are not currently advertised as released builds.

## FAQ

### Must I be online?

No. Local cleanup, preview, and local export work without a network connection. Network access is only needed for actions such as downloading releases, opening an external link, or an AI request you choose to make.

### Will the application upload my text?

Not for basic local processing. A third-party request occurs only when you explicitly use AI optimization with your own configured provider.

### Must I configure an API key?

No. An API key is needed only for optional AI optimization.

### Which files can I use?

The application accepts TXT, Markdown/MD, and DOCX input and can export UTF-8 TXT or structured DOCX.

### What is the difference between Word and TXT export?

Word can retain rich structure such as headings, native tables, and supported editable equations. TXT is a clean UTF-8 text handoff without rich document objects.

### Why is Word export recommended for some documents?

It is the format that can carry the recovered document structure most faithfully, especially tables and supported formulas.

### Are formulas editable?

Supported formulas are exported as Word OMML native equations. Complex unsupported macros may use a readable fallback and should be checked before publishing.

### Are tables exported as Word tables?

Structured Markdown tables are exported as native Word tables when Word export is selected.

### How do I change language or theme?

Use the language and theme controls in the application toolbar/settings. The runtime switch preserves the active document and cleanup selections.

### Where is my API key stored?

The app uses its configured Windows credential-storage path when available and does not include the key in exported configuration. Review the installed build’s settings and your system security policy.

### Installer or portable ZIP?

Choose the installer for normal Windows integration and uninstall support. Choose portable when you want an extracted, self-contained folder.

### How do I report a problem or contribute a translation?

Open an issue or pull request in [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio), including a non-sensitive sample and expected result where possible.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Keep changes focused, add tests when behavior changes, avoid committing build output or credentials, and preserve the project’s local-first privacy posture.

## Developer

Maintained by [SiriZhao](https://github.com/SiriZhao). Project home: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio).

## Third-party licenses

See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) for distributed and runtime dependency notices. CleanText Studio does not package Apple PingFang font files.

## License

CleanText Studio is available under the [MIT License](LICENSE).
