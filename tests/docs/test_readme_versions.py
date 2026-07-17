"""Current documentation must identify only the current public release."""

from __future__ import annotations

from pathlib import Path


def test_readmes_reference_v152_assets() -> None:
    for path in Path(__file__).parents[2].glob("README*.md"):
        content = path.read_text(encoding="utf-8")
        assert "v1.5.2" in content, path.name
        assert "assets/screenshots/v1.5.2/" in content, path.name
        assert "assets/screenshots/v1.5.0/" not in content, path.name
        assert "assets/screenshots/v1.4" not in content, path.name
