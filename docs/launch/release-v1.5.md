# CleanText Studio v1.5 release announcement

## CleanText Studio v1.5

CleanText Studio v1.5 strengthens the local-first document workflow: a more
consistent multilingual UI, structured formula handling, editable Word
equations where supported, and a clearer open-source project experience.

## New features

- Runtime UI support for the project's 12 supported languages.
- Structured Help, About, export, warning, and AI-configuration dialogs.
- Supported LaTeX detection and an AST-to-OMML path for editable Word formulas.
- Real project screenshots, documentation checks, and a Windows CI workflow.

## Improvements

- A unified visual system for card surfaces, controls, focus states, and themes.
- Formula boundary handling in prose, lists, and table content.
- Complete multilingual project pages and clearer privacy documentation.

## Bug fixes

- Corrected mixed-language UI paths and translated enum display issues.
- Fixed several complex-formula conversions and duplicate Word list numbering.
- Improved About-dialog handling of fixed project and license names.

## Migration notes

Existing cleanup settings remain compatible. The normal cleanup baseline remains
protected by regression checks. Review custom formula/macros after upgrading:
unsupported syntax may use a readable fallback rather than native Word math.

## What is next

The project will prioritize reproducible document-quality fixes, translation
review, and packaging reliability. Additional platforms, providers, or plugin
work are exploratory until implemented, tested, and released.
