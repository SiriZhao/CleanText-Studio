"""Regression gate for the public multilingual documentation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_readme_quality_gate() -> None:
    root = Path(__file__).parents[2]
    completed = subprocess.run(
        [sys.executable, "scripts/check_readme_quality.py"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
