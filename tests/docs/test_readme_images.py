"""Public README images must resolve to current release assets."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_screenshot_quality_gate() -> None:
    root = Path(__file__).parents[2]
    result = subprocess.run(
        [sys.executable, "scripts/check_screenshot_quality.py"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
