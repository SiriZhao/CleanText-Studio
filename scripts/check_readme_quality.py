from __future__ import annotations

from pathlib import Path

"""Validate versioned README links and the shared documentation structure."""


ROOT = Path(__file__).parents[1]
README_FILES = (
    "README.md", "README.zh-CN.md", "README.zh-TW.md", "README.ja.md",
    "README.ko.md", "README.es.md", "README.fr.md", "README.de.md",
    "README.pt-BR.md", "README.ru.md", "README.ar.md", "README.hi.md",
)
REQUIRED_MARKERS = ("<!-- section:download -->", "<!-- section:features -->", "<!-- section:privacy -->", "<!-- section:build -->", "<!-- section:license -->")


def main() -> int:
    errors: list[str] = []
    for name in README_FILES:
        path = ROOT / name
        if not path.exists():
            errors.append(f"missing {name}")
            continue
        content = path.read_text(encoding="utf-8")
        if len(content) < 1_500:
            errors.append(f"{name} is too short for a project landing page")
        if "v1.5.1" not in content:
            errors.append(f"{name} does not identify v1.5.1")
        if "README_EN.md" in content or "TODO" in content:
            errors.append(f"{name} contains obsolete documentation text")
        for marker in REQUIRED_MARKERS:
            if marker not in content:
                errors.append(f"{name} is missing {marker}")
    if errors:
        raise SystemExit("README quality check failed:\n- " + "\n- ".join(errors))
    print(f"README quality OK: {len(README_FILES)} localized landing pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
