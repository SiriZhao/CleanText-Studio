"""The localized project pages should remain substantial and structurally close."""

import re
from pathlib import Path

README_FILES = tuple(Path(__file__).parents[2].glob("README*.md"))


def test_readme_section_parity() -> None:
    counts = {
        path.name: len(re.findall(r"(?m)^#{1,3} ", path.read_text(encoding="utf-8")))
        for path in README_FILES
    }
    assert len(counts) == 12
    assert min(counts.values()) >= 45
    assert max(counts.values()) - min(counts.values()) <= 8


def test_readme_pages_are_not_summary_stubs() -> None:
    for path in README_FILES:
        assert len(path.read_text(encoding="utf-8")) >= 10_000, path.name
