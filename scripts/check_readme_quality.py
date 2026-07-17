"""Quality gate for the committed v1.5.2 multilingual project homepages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
README_FILES = (
    "README.md", "README.zh-CN.md", "README.zh-TW.md", "README.ja.md",
    "README.ko.md", "README.es.md", "README.fr.md", "README.de.md",
    "README.pt-BR.md", "README.ru.md", "README.ar.md", "README.hi.md",
)
VERSION = "v1.5.2"
RELEASE = "https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.5.2"
REQUIRED_IMAGES = {
    "hero-main-en.png", "cleaning-before-after.png", "table-preview.png",
    "math-preview.png", "ai-settings.png", "rounded-ui-details.png",
}
FORBIDDEN = (
    "README_EN.md", "screenshots/v1.4", "screenshots/v1.5.0", "TODO",
    "ai-detector-bypass", "undetectable-ai", "plagiarism-bypass",
    "C:\\Users\\", "/Users/", "api_key=",
)
IMAGE_RE = re.compile(r"!?\[[^]]*]\((assets/screenshots/v1\.5\.2/[^)]+)\)")


def main() -> int:
    errors: list[str] = []
    heading_counts: dict[str, int] = {}
    all_images: set[str] = set()
    for name in README_FILES:
        path = ROOT / name
        if not path.exists():
            errors.append(f"missing {name}")
            continue
        content = path.read_text(encoding="utf-8")
        headings = len(re.findall(r"(?m)^#{1,3} ", content))
        heading_counts[name] = headings
        if len(content) < 10_000:
            errors.append(f"{name} is too short ({len(content)} characters)")
        if headings < 45:
            errors.append(f"{name} has too few sections ({headings})")
        if VERSION not in content or RELEASE not in content:
            errors.append(f"{name} does not identify the current release")
        if "CleanText Studio" not in content or "README.zh-CN.md" not in content:
            errors.append(f"{name} has no complete language/project navigation")
        for forbidden in FORBIDDEN:
            # ``todo`` is a normal Spanish/Portuguese word; only the uppercase
            # engineering placeholder is a documentation defect.
            present = forbidden in content if forbidden == "TODO" else forbidden.casefold() in content.casefold()
            if present:
                errors.append(f"{name} contains forbidden content: {forbidden}")
        images = set(IMAGE_RE.findall(content))
        all_images.update(images)
        if not images:
            errors.append(f"{name} has no v1.5.2 screenshots")
        for image in images:
            image_path = ROOT / image
            if not image_path.exists() or image_path.stat().st_size == 0:
                errors.append(f"{name} references missing image: {image}")
    missing = REQUIRED_IMAGES - {Path(image).name for image in all_images}
    if missing:
        errors.append(f"flagship images are not referenced: {sorted(missing)}")
    if max(heading_counts.values(), default=0) - min(heading_counts.values(), default=0) > 8:
        errors.append(f"README section parity is too uneven: {heading_counts}")
    if errors:
        raise SystemExit("README quality check failed:\n- " + "\n- ".join(errors))
    print(f"README quality OK: {len(README_FILES)} pages, {len(all_images)} referenced v1.5.2 images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
