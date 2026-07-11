from __future__ import annotations

import re

import emoji

from cleantext_studio.models import ResidualWarning

PATTERNS = (
    ("markdown_heading", re.compile(r"^\s*[#＃]+")),
    ("separator", re.compile(r"^\s*(?:(?:[-*_—]\s*){3,})$")),
    ("markdown_emphasis", re.compile(r"(?:\*\*|__)[^\n]+(?:\*\*|__)")),
    ("markdown_link", re.compile(r"!?\[[^]]*]\([^)]+\)")),
    ("code_fence", re.compile(r"^\s*```")),
    ("quote_marker", re.compile(r"^\s*>")),
    ("html_tag", re.compile(r"</?(?:p|br|strong|em|span|div)\b", re.I)),
    ("trailing_space", re.compile(r"[ \t]+$")),
)


def detect_residuals(text: str) -> list[ResidualWarning]:
    """Return suspicious formatting outside fenced code and Markdown tables."""
    warnings: list[ResidualWarning] = []
    in_code = False
    for number, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*```", line):
            in_code = not in_code
            continue
        if in_code or re.match(r"^\s*\|.*\|\s*$", line):
            continue
        for kind, pattern in PATTERNS:
            if pattern.search(line):
                warnings.append(ResidualWarning(number, kind, line[:120]))
                break
        else:
            if emoji.emoji_count(line):
                warnings.append(ResidualWarning(number, "emoji", line[:120]))
    if re.search(r"\n{4,}", text):
        warnings.append(ResidualWarning(1, "excess_blank_lines", "连续空行"))
    return warnings
