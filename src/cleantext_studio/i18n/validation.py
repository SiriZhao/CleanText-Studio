"""Catalog-level validation used by the application and CI."""

from __future__ import annotations

import json
from pathlib import Path

FORMAL_LOCALES = (
    "zh_CN", "zh_TW", "en_US", "ja_JP", "ko_KR", "es_ES", "fr_FR",
    "de_DE", "pt_BR", "ru_RU", "ar", "hi_IN",
)


def validate_catalogs(directory: Path | None = None) -> dict[str, bool]:
    """Return catalog-level completeness without silently falling back per key."""
    root = directory or Path(__file__).with_name("translations")
    baseline = json.loads((root / "en_US.json").read_text(encoding="utf-8"))
    keys = set(baseline)
    result: dict[str, bool] = {}
    for locale in FORMAL_LOCALES:
        path = root / f"{locale}.json"
        if not path.exists():
            result[locale] = False
            continue
        catalog = json.loads(path.read_text(encoding="utf-8"))
        result[locale] = set(catalog) == keys and all(str(value).strip() for value in catalog.values())
    return result
