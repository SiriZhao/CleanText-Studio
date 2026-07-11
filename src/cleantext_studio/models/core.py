from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class TextBlockType(StrEnum):
    TITLE = "title"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    QUOTE = "quote"
    CODE = "code"
    TABLE = "table"
    BLANK = "blank"


@dataclass(slots=True)
class TextBlock:
    type: TextBlockType
    original_text: str
    text: str
    position: int
    heading_level: int | None = None
    list_level: int | None = None
    modified: bool = False
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CleanStats:
    original_chars: int = 0
    result_chars: int = 0
    removed_chars: int = 0
    merged_linebreaks: int = 0
    removed_emoji: int = 0
    removed_markdown: int = 0
    removed_separators: int = 0
    headings_detected: int = 0
    residual_count: int = 0
    elapsed_ms: float = 0


@dataclass(slots=True)
class CleanResult:
    text: str
    blocks: list[TextBlock]
    stats: CleanStats
    changes: list[str]
    residuals: list[ResidualWarning] = field(default_factory=list)


@dataclass(slots=True, frozen=True)
class ResidualWarning:
    line: int
    kind: str
    excerpt: str
