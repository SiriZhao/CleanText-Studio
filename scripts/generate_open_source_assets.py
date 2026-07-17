"""Create repository-homepage assets from real, privacy-safe Qt captures.

The source captures are the versioned v1.5.2 screenshots generated from the
application. This helper only copies/crops those real captures and assembles a
short workflow GIF; it never manufactures a UI image.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "assets" / "screenshots" / "v1.5.2"
TARGET = ROOT / "assets" / "screenshots"
MAPPING = {
    "01-main-light.png": "01-main-light.png",
    "02-main-dark.png": "02-main-dark.png",
    "03-before-after-light.png": "03-before-after-light.png",
    "04-before-after-dark.png": "04-before-after-dark.png",
    "05-table-export.png": "05-table-export.png",
    "06-word-export.png": "06-word-export.png",
    "07-settings.png": "07-settings.png",
    "08-about.png": "08-about.png",
}


def _frame(path: Path) -> Image.Image:
    with Image.open(path) as image:
        image = image.convert("RGB")
        width = 960
        height = round(image.height * width / image.width)
        return image.resize((width, height), Image.Resampling.LANCZOS).quantize(colors=128)


def main() -> int:
    if not SOURCE.exists():
        raise SystemExit(f"missing real screenshot source: {SOURCE}")
    for target, source in MAPPING.items():
        origin = SOURCE / source
        if not origin.exists() or origin.stat().st_size == 0:
            raise SystemExit(f"missing source screenshot: {origin}")
        shutil.copy2(origin, TARGET / target)

    frames = [_frame(SOURCE / MAPPING[name]) for name in MAPPING]
    frames[0].save(
        ROOT / "assets" / "demo.gif",
        save_all=True,
        append_images=frames[1:],
        duration=[3000, 3000, 3000, 3000, 3000, 3000, 1000, 1000],
        loop=0,
        optimize=True,
        disposal=2,
    )
    logo_dir = ROOT / "assets" / "logo"
    logo_dir.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "assets" / "icon.png", logo_dir / "cleantext-studio.png")
    shutil.copy2(ROOT / "assets" / "icon.svg", logo_dir / "cleantext-studio.svg")
    print(f"Generated {len(MAPPING)} showcase images and assets/demo.gif")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
