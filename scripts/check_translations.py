"""Fail fast when a formal UI catalog is unreadable or incomplete.

The product must never rely on a per-key English fallback: that is precisely
what creates a mixed-language window at runtime.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
CATALOGS = ROOT / "src" / "cleantext_studio" / "i18n" / "translations"
REQUIRED = {"zh_CN", "zh_TW", "en_US", "ja_JP", "ko_KR", "es_ES", "fr_FR", "de_DE", "pt_BR", "ru_RU", "ar", "hi_IN"}

def main() -> int:
    catalogs = {path.stem: json.loads(path.read_text(encoding="utf-8")) for path in CATALOGS.glob("*.json")}
    missing = REQUIRED - catalogs.keys()
    if missing:
        raise SystemExit(f"missing translation catalogs: {sorted(missing)}")
    keys = set(catalogs["en_US"])
    for code, catalog in catalogs.items():
        if any(not str(value).strip() for value in catalog.values()):
            raise SystemExit(f"empty translation in {code}")
        missing_keys = keys - set(catalog)
        unknown = set(catalog) - keys
        if missing_keys or unknown:
            details: list[str] = []
            if missing_keys:
                details.append(f"missing={sorted(missing_keys)}")
            if unknown:
                details.append(f"unknown={sorted(unknown)}")
            raise SystemExit(f"catalog key mismatch in {code}: {'; '.join(details)}")
    print(f"translation catalogs OK: {len(catalogs)} catalogs, {len(keys)} base keys")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
