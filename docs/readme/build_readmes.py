"""Generate localized README pages from the English v1.5.0 factual master.

Generated files remain ordinary Markdown.  This script is a maintenance aid,
not an application dependency.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
MASTER = ROOT / "README.md"
TARGETS = {
    "zh-CN": "README.zh-CN.md",
    "zh-TW": "README.zh-TW.md", "ja": "README.ja.md", "ko": "README.ko.md",
    "es": "README.es.md", "fr": "README.fr.md", "de": "README.de.md",
    "pt": "README.pt-BR.md", "ru": "README.ru.md", "ar": "README.ar.md",
    "hi": "README.hi.md",
}


def translatable(line: str, code: bool) -> bool:
    stripped = line.strip()
    return bool(
        stripped
        and not code
        and "http" not in line
        and "assets/" not in line
        and not stripped.startswith("[!")
        and not stripped.startswith("<!--")
    )


def translate_document(target: str, text: str) -> str:
    from deep_translator import GoogleTranslator

    translator = GoogleTranslator(source="en", target=target)
    lines: list[str] = []
    code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            code = not code
            lines.append(line)
        elif translatable(line, code):
            prefix = re.match(r"^(\s*(?:#{1,6}\s+|-\s+|\d+\.\s+)?)", line)
            assert prefix is not None
            head = prefix.group(1)
            body = line[len(head):]
            try:
                lines.append(head + translator.translate(body))
            except Exception:
                lines.append(line)
        else:
            lines.append(line)
    result = "\n".join(lines) + "\n\n> Translation review from the community is welcome.\n"
    if target == "ar":
        result = "<div dir=\"rtl\">\n\n" + result + "\n</div>\n"
    return result


def main() -> int:
    selected = set(sys.argv[1:]) or set(TARGETS)
    unknown = selected - set(TARGETS)
    if unknown:
        raise SystemExit(f"unknown locales: {sorted(unknown)}")
    master = MASTER.read_text(encoding="utf-8")
    for locale, filename in TARGETS.items():
        if locale in selected:
            (ROOT / filename).write_text(translate_document(locale, master), encoding="utf-8")
            print(filename)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
