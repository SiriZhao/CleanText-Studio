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


class ParagraphBreakMode(StrEnum):
    COMPACT = "compact"
    SMART_SECTIONS = "smart_sections"
    PRESERVE_ALL = "preserve_all"


class LinkMode(StrEnum):
    TEXT_ONLY = "text_only"
    TEXT_AND_URL = "text_and_url"
    KEEP_MARKDOWN = "keep_markdown"


class IndependentURLMode(StrEnum):
    PRESERVE = "preserve"
    MERGE_PREVIOUS = "merge_previous"
    DELETE_TUTORIAL = "delete_tutorial"


class MathOutputMode(StrEnum):
    PRESERVE = "preserve"
    LATEX = "latex"
    UNICODE = "unicode"


class MathExportMode(StrEnum):
    WORD_OMML = "word_omml"
    LATEX_TEXT = "latex_text"
    UNICODE_TEXT = "unicode_text"


class CleanOptions(BaseModel):
    remove_markdown: bool = True
    remove_emoji: bool = True
    remove_decorations: bool = True
    merge_fragments: bool = True
    merge_level: MergeLevel = MergeLevel.STANDARD
    paragraph_break_mode: ParagraphBreakMode = ParagraphBreakMode.SMART_SECTIONS
    keep_bullets: bool = True
    list_mode: ListMode = ListMode.KEEP
    normalize_punctuation: bool = True
    keep_link_url: bool = False
    link_mode: LinkMode = LinkMode.TEXT_ONLY
    clean_instructional_labels: bool = False
    independent_url_mode: IndependentURLMode = IndependentURLMode.PRESERVE
    detect_math: bool = True
    protect_math: bool = True
    normalize_math_spacing: bool = True
    repair_math_delimiters: bool = True
    preserve_equation_numbers: bool = True
    math_output_mode: MathOutputMode = MathOutputMode.PRESERVE
    math_export_mode: MathExportMode = MathExportMode.WORD_OMML
    preserve_unconverted_math: bool = True


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
