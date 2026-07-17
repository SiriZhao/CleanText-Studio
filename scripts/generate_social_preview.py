"""Create a deterministic GitHub social-preview image from a real capture."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "assets" / "screenshots" / "v1.5.2" / "01-main-light.png"
TARGET = ROOT / "assets" / "social-preview.png"
SIZE = (1280, 640)


def font(size: int) -> ImageFont.FreeTypeFont:
    for name in ("segoeuib.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> int:
    with Image.open(SOURCE) as source:
        screenshot = source.convert("RGB")
    canvas = Image.new("RGB", SIZE, "#171923")
    preview = screenshot.copy()
    preview.thumbnail((790, 500), Image.Resampling.LANCZOS)
    canvas.paste(preview, (450, 92))
    draw = ImageDraw.Draw(canvas)
    draw.text((56, 110), "CleanText Studio", font=font(52), fill="#ffffff")
    draw.text((56, 190), "Privacy-first, local-first", font=font(30), fill="#b9b2ff")
    draw.text((56, 232), "text cleanup and document", font=font(30), fill="#f0f2f8")
    draw.text((56, 272), "formatting for Windows", font=font(30), fill="#f0f2f8")
    draw.rounded_rectangle((56, 360, 346, 410), radius=18, fill="#756be0")
    draw.text((82, 374), "DOCX / TXT · Local", font=font(20), fill="#ffffff")
    draw.text((56, 550), "github.com/SiriZhao/CleanText-Studio", font=font(18), fill="#aeb6ca")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(TARGET, "PNG", optimize=True)
    print(TARGET)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
