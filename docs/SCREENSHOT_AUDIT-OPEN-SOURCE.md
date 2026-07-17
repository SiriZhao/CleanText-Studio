# Open-source showcase screenshot audit

The unversioned showcase assets below are committed copies of real Qt captures
from `assets/screenshots/v1.5.2/`. They are intentionally small, stable paths
for the project homepage; no browser, desktop taskbar, private path, API key,
or generated design mockup is used.

| Showcase asset | Real capture source | Purpose |
| --- | --- | --- |
| `assets/screenshots/01-main-light.png` | `v1.5.2/hero-main-en.png` | Main product hero (kept under the requested stable filename) |
| `assets/screenshots/02-main-dark.png` | `v1.5.2/hero-main-dark-en.png` | Dark-theme UI |
| `assets/screenshots/03-settings.png` | `v1.5.2/rounded-ui-details.png` | Cleanup controls and rounded surfaces |
| `assets/screenshots/04-about.png` | `v1.5.2/about-en.png` | Product identity and license facts |
| `assets/screenshots/05-word-export.png` | `v1.5.2/export-summary.png` | Native DOCX export confirmation |
| `assets/screenshots/06-formula-rendering.png` | `v1.5.2/math-preview.png` | Formula preview and structure preservation |
| `assets/demo.gif` | The six captures above | 20-second real application workflow montage |

`scripts/check_showcase_assets.py` validates the committed asset signatures,
minimum size, and dimensions. `scripts/check_screenshot_quality.py` validates
the locale-specific v1.5.2 screenshot set used by localized documentation.
