"""Fail fast if a formal UI catalog is unreadable or incomplete after fallback."""

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
        if code == "en_US":
            continue
        # Catalogs can intentionally inherit keys from English; explicitly supplied keys must be valid.
        unknown = set(catalog) - keys
        if unknown:
            raise SystemExit(f"unknown translation keys in {code}: {sorted(unknown)}")
    print(f"translation catalogs OK: {len(catalogs)} catalogs, {len(keys)} base keys")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
