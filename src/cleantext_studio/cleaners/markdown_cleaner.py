from __future__ import annotations

import re
from dataclasses import dataclass

from cleantext_studio.models import LinkMode, ListMode

HEADING = re.compile(r"^[\s\u3000]*([#＃]{1,6})(?!\d)[\s\u3000]*")
SEPARATOR = re.compile(r"^\s*(?:(?:[-*_—─]\s*){3,})$")
LIST = re.compile(r"^(?P<indent>\s*)(?P<marker>[-+*•▪◦]|\d+[.、)]|[（(]\d+[）)])\s+")


@dataclass(slots=True, frozen=True)
class MarkdownLine:
    text: str
    heading_level: int | None = None
    list_level: int | None = None
    is_list: bool = False
    removed: int = 0
    links_processed: int = 0
    list_marker: str | None = None
    ordered_index: int | None = None


class MarkdownCleaner:
    """Remove Markdown presentation syntax while retaining document structure."""

    @staticmethod
    def is_separator(line: str) -> bool:
        return bool(SEPARATOR.fullmatch(line))

    def clean(self, line: str, *, link_mode: LinkMode, list_mode: ListMode) -> MarkdownLine:
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
        links_processed = len(re.findall(r"(?<!!)\[([^]]+)]\(([^)]+)\)", line))
        if link_mode != LinkMode.KEEP_MARKDOWN:
            line = re.sub(
                r"(?<!!)\[([^]]+)]\(([^)]+)\)",
                r"\1（\2）" if link_mode == LinkMode.TEXT_AND_URL else r"\1",
                line,
            )
            line = re.sub(r"[（(]\[([^]]+)]\[\d+][）)]", r"\1", line)
            line = re.sub(r"^\[\d+]:\s+\S+(?:\s+\"[^\"]*\")?\s*$", "", line)
        line = re.sub(r"(?<!\\)(\*{3}|_{3})(.+?)\1", r"\2", line)
        line = re.sub(r"(?<!\\)(\*\*|__)(.+?)\1", r"\2", line)
        line = re.sub(r"(?<![\w\\])([*_])([^\n*_]+?)\1(?!\w)", r"\2", line)
        line = re.sub(r"(?<!\\)`([^`]+)`", r"\1", line)
        line = re.sub(r"\\([#*_>`])", r"\1", line)
        list_match = LIST.match(line)
        list_level = None
        list_marker = None
        ordered_index = None
        if list_match:
            list_level = len(list_match.group("indent")) // 2
            content = line[list_match.end() :]
            marker = list_match.group("marker")
            list_marker = marker
            number = re.match(r"[（(]?(\d+)", marker)
            ordered_index = int(number.group(1)) if number else None
            line = (
                f"• {content}" if list_mode == ListMode.KEEP and marker in "-+*•▪◦" else
                f"{marker} {content}" if list_mode == ListMode.KEEP else content
            )
        line = re.sub(r"[ \t]+", " ", line).strip()
        return MarkdownLine(
            line, heading_level, list_level, list_match is not None,
            max(0, len(original) - len(line)), links_processed, list_marker, ordered_index,
        )
