# Screenshot audit — v1.5.1

The current README set uses only `assets/screenshots/v1.5.1/`. These images
are captured from a real Qt `MainWindow`, Help dialog, About dialog, and AI
configuration dialog using `scripts/capture_readme_screenshots.py`. The
capture process initializes `FontManager` after `QApplication` creation and
uses the native Windows Qt platform so CJK, Arabic, and Devanagari fallback
fonts are available.

| Group | Files | Validation |
| --- | --- | --- |
| Hero and locale UI | `hero-main-en.png`, `hero-main-zh-cn.png`, `hero-main-dark-en.png`, `main-*.png` | Real UI, fixed window size, public sample text |
| Workflow | `cleaning-before-after.png`, `table-preview.png`, `math-preview.png`, `export-summary.png` | Real cleaned result and preview state |
| Dialogs | `help-*.png`, `about-*.png`, `ai-settings.png` | Real dialogs, no API key entered |
| Visual detail | `rounded-ui-details.png` | Crop of the real settings card |

`scripts/check_screenshot_quality.py` checks the required file set, PNG
signature, dimensions, and non-trivial file size. Older v1.4.x and v1.5.0
screenshots remain historical assets only and are not referenced by current
README pages.
