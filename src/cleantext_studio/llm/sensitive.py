import re
from dataclasses import dataclass

PATTERNS = {
    "SECRET": re.compile(
        r"(?:sk-[A-Za-z0-9_-]{16,}|-----BEGIN [A-Z ]+PRIVATE KEY-----|Authorization:\s*\S+)", re.I
    ),
    "EMAIL": re.compile(r"(?<![\w.-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "PHONE": re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)"),
    "ID": re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"),
    "CARD": re.compile(r"(?<!\d)(?:\d[ -]?){16,19}(?!\d)"),
    "INTERNAL_URL": re.compile(
        r"https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+)[^\s]*", re.I
    ),
}


@dataclass(slots=True)
class RedactionResult:
    text: str
    mapping: dict[str, str]
    counts: dict[str, int]


def redact_sensitive(text: str) -> RedactionResult:
    mapping: dict[str, str] = {}
    counts: dict[str, int] = {}
    for kind, pattern in PATTERNS.items():

        def replace(match: re.Match[str], label: str = kind, source: str = text) -> str:
            counts[label] = counts.get(label, 0) + 1
            placeholder = f"[{label}_{counts[label]}]"
            while placeholder in source or placeholder in mapping:
                counts[label] += 1
                placeholder = f"[{label}_{counts[label]}]"
            mapping[placeholder] = match.group(0)
            return placeholder

        text = pattern.sub(replace, text)
    return RedactionResult(text, mapping, counts)


def restore_sensitive(text: str, mapping: dict[str, str]) -> str:
    for placeholder, value in mapping.items():
        if placeholder not in text:
            raise ValueError(f"Sensitive placeholder missing: {placeholder}")
        text = text.replace(placeholder, value)
    return text
