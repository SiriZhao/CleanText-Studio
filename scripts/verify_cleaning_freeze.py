"""Verify that the UI localization release did not modify cleaning output."""

from __future__ import annotations

import hashlib
from pathlib import Path

from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import CleanOptions

ROOT = Path(__file__).parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "cleaning_freeze.md"
EXPECTED_SHA256 = "9e2cc2a0a3e44030c7efc77e77f184bc0268c38ed55971ddae754ec3b077fc72"

def main() -> int:
    result = clean_text(FIXTURE.read_text(encoding="utf-8"), CleanOptions())
    digest = hashlib.sha256(result.text.encode("utf-8")).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"cleaning freeze mismatch: expected {EXPECTED_SHA256}, got {digest}")
    print(f"cleaning freeze OK: {digest}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
