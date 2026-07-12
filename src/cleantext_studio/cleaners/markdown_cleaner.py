from __future__ import annotations

import re
from dataclasses import dataclass

from cleantext_studio.models import ListMode

HEADING = re.compile(r"^[\s\u3000]*([#＃]{1,6})[\s\u3000]*")
SEPARATOR = re.compile(r"^\s*(?:(?:[-*_—]\s*){3,})$")
LIST = re.compile(r"^(?P<indent>\s*)(?P<marker>[-+*•▪◦]|\d+[.、)]|[（(]\d+[）)])\s+")


@dataclass(slots=True, frozen=True)
class MarkdownLine:
    text: str
    heading_level: int | None = None
    list_level: int | None = None
    is_list: bool = False
    removed: int = 0


class MarkdownCleaner:
    """Remove Markdown presentation syntax while retaining document structure."""

    @staticmethod
    def is_separator(line: str) -> bool:
        return bool(SEPARATOR.fullmatch(line))

    def clean(self, line: str, *, keep_url: bool, list_mode: ListMode) -> MarkdownLine:
        original = line
        heading_level: int | None = None
        outer = re.fullmatch(r"(?:\*{1,3}|_{1,3})(.*?)(?:\*{1,3}|_{1,3})", line)
        if outer and HEADING.match(outer.group(1)):
            line = outer.group(1)
        match = HEADING.match(line)
        if match:
            heading_level = len(match.group(1))
            line = line[match.end() :]
        line = re.sub(
            r"!\[([^]]*)]\(([^)]+)\)",
            lambda m: f"[图片：{m.group(1)}]" if m.group(1) else "[图片]",
            line,
        )
        line = re.sub(
            r"(?<!!)\[([^]]+)]\(([^)]+)\)", r"\1（\2）" if keep_url else r"\1", line
        )
        line = re.sub(r"(?<!\\)(\*{3}|_{3})(.+?)\1", r"\2", line)
        line = re.sub(r"(?<!\\)(\*\*|__)(.+?)\1", r"\2", line)
        line = re.sub(r"(?<![\w\\])([*_])([^\n*_]+?)\1(?!\w)", r"\2", line)
        line = re.sub(r"(?<!\\)`([^`]+)`", r"\1", line)
        line = re.sub(r"\\([#*_>`])", r"\1", line)
        list_match = LIST.match(line)
        list_level = None
        if list_match:
            list_level = len(list_match.group("indent")) // 2
            content = line[list_match.end() :]
            marker = list_match.group("marker")
            line = (
                f"• {content}" if list_mode == ListMode.KEEP and marker in "-+*•▪◦" else
                f"{marker} {content}" if list_mode == ListMode.KEEP else content
            )
        line = re.sub(r"[ \t]+", " ", line).strip()
        return MarkdownLine(
            line, heading_level, list_level, list_match is not None,
            max(0, len(original) - len(line)),
        )
