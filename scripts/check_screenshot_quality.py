"""Validate README screenshots without depending on a browser renderer."""

from __future__ import annotations

import struct
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCREENSHOTS = ROOT / "assets" / "screenshots" / "v1.5.1"
MIN_BYTES = 20_000
MIN_WIDTH = 700
EXPECTED = {
    "hero-main-en.png", "hero-main-zh-cn.png", "hero-main-dark-en.png",
    "main-zh-tw.png", "main-ja.png", "main-ko.png", "main-es.png",
    "main-fr.png", "main-de.png", "main-pt-br.png", "main-ru.png",
    "main-ar-rtl.png", "main-hi.png", "cleaning-before-after.png",
    "table-preview.png", "math-preview.png", "help-en.png", "help-zh-cn.png",
    "about-en.png", "about-zh-cn.png", "ai-settings.png", "export-summary.png",
    "rounded-ui-details.png",
}


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        signature = handle.read(8)
        if signature != b"\x89PNG\r\n\x1a\n":
            raise ValueError("not a PNG")
        _length = handle.read(4)
        if handle.read(4) != b"IHDR":
            raise ValueError("missing PNG IHDR")
        return struct.unpack(">II", handle.read(8))


def main() -> int:
    errors: list[str] = []
    found = {path.name for path in SCREENSHOTS.glob("*.png")} if SCREENSHOTS.exists() else set()
    missing = EXPECTED - found
    if missing:
        errors.append(f"missing screenshots: {sorted(missing)}")
    for name in sorted(EXPECTED & found):
        path = SCREENSHOTS / name
        try:
            width, height = png_size(path)
        except ValueError as exc:
            errors.append(f"{name}: {exc}")
            continue
        if path.stat().st_size < MIN_BYTES:
            errors.append(f"{name}: too small ({path.stat().st_size} bytes)")
        if width < MIN_WIDTH or height < 500:
            errors.append(f"{name}: insufficient dimensions ({width}x{height})")
    if errors:
        raise SystemExit("Screenshot quality check failed:\n- " + "\n- ".join(errors))
    print(f"Screenshot quality OK: {len(EXPECTED)} v1.5.1 PNG files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
