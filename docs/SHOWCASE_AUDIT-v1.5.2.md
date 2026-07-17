# Showcase audit — v1.5.2

The public homepage now uses the eight real Qt captures in
`assets/screenshots/v1.5.2/`. Earlier root-level and v1.5.0/v1.5.1 image sets
remain historical assets only and are no longer referenced by README pages.

| Asset | README use | Review | Decision |
| --- | --- | --- | --- |
| `01-main-light.png` | Hero, all localized pages | Stable English demo text; complete three-panel window; no formula source commands | Keep |
| `02-main-dark.png` | Main README gallery | Same text, setting state, DPI, and geometry as light capture | Keep |
| `03-before-after-light.png` | Main README and localized pages | Real cleaned result with headings/list/table input | Keep |
| `04-before-after-dark.png` | Supporting gallery | Same safe demo in dark theme | Keep |
| `05-table-export.png` | Tables section | Real Preview-mode table workflow | Keep |
| `06-word-export.png` | Export section | Real application export workflow state | Keep |
| `07-settings.png` | Settings/AI documentation | Real settings crop; no credentials | Keep |
| `08-about.png` | About/identity documentation | Real About dialog, version and license facts | Keep |

## Removed from public use

The README no longer references `math-preview.png`, complex formula-index
captures, v1.4.x/v1.5.0/v1.5.1 screenshot paths, or unversioned root showcase
images. Those historical files are retained only to avoid deleting unrelated
repository history.

## Manual visual checks

The captures were inspected after generation: no local paths, API keys, taskbar,
debug console, unrendered backslash commands, clipped result buttons, or mixed
UI language are present. `scripts/check_showcase_assets.py` validates file
format, dimensions, and the formal set on every CI run.
