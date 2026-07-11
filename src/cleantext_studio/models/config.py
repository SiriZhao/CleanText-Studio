from enum import StrEnum

from pydantic import BaseModel, Field


class MergeLevel(StrEnum):
    CONSERVATIVE = "conservative"
    STANDARD = "standard"
    AGGRESSIVE = "aggressive"


class ListMode(StrEnum):
    KEEP = "keep"
    REMOVE_MARKERS = "remove_markers"
    NATURAL_PARAGRAPH = "natural_paragraph"


class CleanOptions(BaseModel):
    remove_markdown: bool = True
    remove_emoji: bool = True
    remove_decorations: bool = True
    merge_fragments: bool = True
    merge_level: MergeLevel = MergeLevel.STANDARD
    keep_bullets: bool = True
    list_mode: ListMode = ListMode.KEEP
    normalize_punctuation: bool = True
    remove_template_phrases: bool = False
    keep_link_url: bool = False


class DocumentTemplate(BaseModel):
    name: str = "通用文档"
    title_font: str = "黑体"
    body_font: str = "宋体"
    title_size: float = Field(22, ge=8, le=72)
    body_size: float = Field(12, ge=8, le=36)
    line_spacing: float = Field(1.5, ge=1, le=3)
    first_line_chars: float = Field(2, ge=0, le=10)
    margin_cm: float = Field(2.54, ge=1, le=5)
    page_numbers: bool = True
    header: str = ""
    toc: bool = False
