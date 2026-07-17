"""Basic documentation link regressions."""

from __future__ import annotations

from pathlib import Path


def test_readmes_do_not_reference_obsolete_english_file() -> None:
    for path in Path(__file__).parents[2].glob("README*.md"):
        content = path.read_text(encoding="utf-8")
        assert "README_EN.md" not in content
        assert "https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.5.1" in content
