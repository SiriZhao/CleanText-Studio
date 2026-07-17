"""Validate the formal v1.5.2 showcase assets used by every README."""

from __future__ import annotations

import struct
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCREENSHOTS = ROOT / "assets" / "screenshots" / "v1.5.2"
EXPECTED = {
    "01-main-light.png",
    "02-main-dark.png",
    "03-before-after-light.png",
    "04-before-after-dark.png",
    "05-table-export.png",
    "06-word-export.png",
    "07-settings.png",
    "08-about.png",
}


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        if handle.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ValueError("not a PNG")
        handle.read(4)
        if handle.read(4) != b"IHDR":
            raise ValueError("missing PNG header")
        return struct.unpack(">II", handle.read(8))


def main() -> int:
    errors: list[str] = []
    for name in sorted(EXPECTED):
        path = SCREENSHOTS / name
        if not path.exists() or path.stat().st_size < 20_000:
            errors.append(f"missing or too small: {name}")
            continue
        try:
            width, height = png_size(path)
        except ValueError as exc:
            errors.append(f"{name}: {exc}")
            continue
        # The settings asset is an intentional tall panel crop; every other
        # capture is a full 1600×960 window.
        if name == "07-settings.png":
            valid_size = width >= 700 and height >= 900
        else:
            valid_size = width >= 900 and height >= 500
        if not valid_size:
            errors.append(f"{name}: insufficient size {width}x{height}")
    demo = ROOT / "assets" / "demo.gif"
    if not demo.exists() or demo.stat().st_size < 100_000:
        errors.append("missing or too small: assets/demo.gif")
    elif demo.read_bytes()[:6] not in {b"GIF87a", b"GIF89a"}:
        errors.append("assets/demo.gif is not a GIF")
    if errors:
        raise SystemExit("Showcase asset check failed:\n- " + "\n- ".join(errors))
    print(f"Showcase assets OK: {len(EXPECTED)} v1.5.2 PNG files and demo.gif")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
