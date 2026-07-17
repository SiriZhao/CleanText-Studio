# Translation guide

UI catalogs live in `src/cleantext_studio/i18n/translations`. Add a UTF-8 JSON file using a supported locale name, keep keys stable, preserve placeholders, and run `python scripts/check_translations.py` plus the GUI tests. Do not translate user text, URLs, API keys, model names, LaTeX, Markdown, JSON/schema keys, or enum IDs. Arabic must be verified in RTL mode.
