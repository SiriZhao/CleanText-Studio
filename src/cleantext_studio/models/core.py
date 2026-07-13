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
    ORDERED_LIST_ITEM = "ordered_list_item"
    HORIZONTAL_RULE = "horizontal_rule"
    RAW = "raw"
    INLINE_MATH = "inline_math"
    DISPLAY_MATH = "display_math"
    EQUATION_GROUP = "equation_group"
    EQUATION_NUMBER = "equation_number"
    MATH_PARAGRAPH = "math_paragraph"


class MathFormat(StrEnum):
    LATEX = "latex"
    MATHML = "mathml"
    ASCIIMATH = "asciimath"
    UNICODE_MATH = "unicode_math"
    PLAIN_EQUATION = "plain_equation"
    UNKNOWN = "unknown"


class MathDisplayMode(StrEnum):
    INLINE = "inline"
    BLOCK = "block"


class InlineRunType(StrEnum):
    TEXT = "text"
    INLINE_MATH = "inline_math"
    LINK = "link"
    CODE = "code"
    BOLD = "bold"
    ITALIC = "italic"


@dataclass(slots=True, frozen=True)
class InlineRun:
    type: InlineRunType
    text: str
    math: MathBlockData | None = None


@dataclass(slots=True)
class MathBlockData:
    source_text: str
    normalized_text: str
    math_format: MathFormat
    display_mode: MathDisplayMode
    equation_number: str | None = None
    source_start: int = 0
    source_end: int = 0
    confidence: float = 1.0
    warnings: list[str] = field(default_factory=list)
    protected: bool = True
    metadata: dict[str, object] = field(default_factory=dict)
    raw_source: str = ""
    expression_source: str = ""
    delimiter_type: str = "none"
    normalized_latex: str = ""
    conversion_status: str = "pending"


@dataclass(slots=True)
class TableData:
    headers: list[str]
    rows: list[list[str]]
    alignments: list[str]
    source: str
    malformed_rows: list[int] = field(default_factory=list)
    caption: str | None = None

    @property
    def column_count(self) -> int:
        return len(self.headers)

    @property
    def source_markdown(self) -> str:
        return self.source


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
    table: TableData | None = None
    block_id: str = ""
    source_start: int = 0
    source_end: int = 0
    list_marker: str | None = None
    ordered_index: int | None = None
    protected: bool = False
    original_blank_lines_before: int = 0
    original_blank_lines_after: int = 0
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, object] = field(default_factory=dict)
    math: MathBlockData | None = None
    runs: list[InlineRun] = field(default_factory=list)

    @property
    def cleaned_text(self) -> str:
        return self.text

    @cleaned_text.setter
    def cleaned_text(self, value: str) -> None:
        self.text = value


@dataclass(slots=True)
class CleanStats:
    original_chars: int = 0
    result_chars: int = 0
    removed_chars: int = 0
    merged_linebreaks: int = 0
    removed_emoji: int = 0
    removed_markdown: int = 0
    removed_separators: int = 0
    removed_ai_patterns: int = 0
    removed_blank_lines: int = 0
    headings_detected: int = 0
    residual_count: int = 0
    elapsed_ms: float = 0
    tables_detected: int = 0
    tables_preserved: int = 0
    empty_table_columns_removed: int = 0
    list_items_detected: int = 0
    links_processed: int = 0
    formulas_detected: int = 0
    inline_formulas_detected: int = 0
    display_formulas_detected: int = 0
    formulas_normalized: int = 0
    formula_delimiters_fixed: int = 0
    formula_warnings: int = 0
    formulas_exported_as_omml: int = 0
    formulas_exported_as_text: int = 0
    formula_conversion_failures: int = 0


@dataclass(slots=True, frozen=True)
class CleaningChange:
    rule_id: str
    change_type: str
    original_text: str
    cleaned_text: str
    source_range: tuple[int, int]
    block_id: str
    count: int
    reason: str


@dataclass(slots=True)
class CleanResult:
    text: str
    blocks: list[TextBlock]
    stats: CleanStats
    changes: list[str]
    residuals: list[ResidualWarning] = field(default_factory=list)
    change_records: list[CleaningChange] = field(default_factory=list)


@dataclass(slots=True, frozen=True)
class ResidualWarning:
    line: int
    kind: str
    excerpt: str
    column: int = 1
    severity: str = "warning"
    suggestion: str = "再次清理或检查该位置"
    block_id: str = ""

    @property
    def warning_type(self) -> str:
        return self.kind

    @property
    def line_number(self) -> int:
        return self.line

    @property
    def snippet(self) -> str:
        return self.excerpt
