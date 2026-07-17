# Theme visual audit — v1.5.2

## Fixed for the formal capture state

- Result toolbar actions now use two balanced three-button rows. This prevents
  labels such as **Export Word**, **Export TXT**, and **Restore result** from
  being clipped in a three-column window.
- Light and dark showcase captures use the same 1600×960 window, language,
  source text, cleanup result, and settings scroll position.
- Existing theme tokens remain the sole source for card surfaces, controls,
  selection, focus borders, scroll bars, and the purple primary action.

## Evidence

- `assets/screenshots/v1.5.2/01-main-light.png`
- `assets/screenshots/v1.5.2/02-main-dark.png`
- `assets/screenshots/v1.5.2/07-settings.png`

The change is limited to result-toolbar layout. It does not modify cleaning,
table, formula, export, or AI request behavior.
