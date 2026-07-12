from __future__ import annotations

import html
import re
import time
import unicodedata

import emoji
import ftfy
from bs4 import BeautifulSoup

from cleantext_studio.models import (
    CleanOptions,
    CleanResult,
    CleanStats,
    MergeLevel,
    TextBlock,
    TextBlockType,
)

from .ai_pattern_cleaner import AIPatternCleaner
from .layout import ParagraphLayoutEngine
from .markdown_cleaner import MarkdownCleaner
from .paragraph_formatter import ParagraphFormatter
from .residuals import detect_residuals
from .tables import consolidate_table_blocks
from .url_cleaner import URLCleaner

NUMBERED = re.compile(
    r"^(?:第一[章节篇部]|[一二三四五六七八九十]+、|（[一二三四五六七八九十]+）|"
    r"\d+(?:\.\d+){1,3}(?:\s+|$))"
)
LIST = re.compile(r"^(?P<indent>\s*)(?P<marker>[-+*•▪◦]|\d+[.、)]|[（(]\d+[）)])\s+")
TABLE = re.compile(r"^\s*\|.*\|\s*$")
END = re.compile(r"[。！？.!?；;]$")
STEP = re.compile(r"^(?:第[一二三四五六七八九十]+步|步骤\s*\d+|Step\s+\d+)")
REFERENCE = re.compile(r"^\s*(?:\[\d+]|\d+\.\s+).*(?:19|20)\d{2}")
DECORATIONS = "◆◇■□●○▶▷★☆🔹🔸"


def _normalize(text: str) -> str:
    text = html.unescape(text).replace("\r\n", "\n").replace("\r", "\n")
    text = ftfy.fix_text(text)
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff]),(?=(?:\n)?[\u4e00-\u9fff])", "，", text)
    return re.sub(r"[\u00a0\u2000-\u200b\u202f\u205f\u3000]", " ", text)


def _html_to_text(text: str) -> str:
    if not re.search(r"</?(?:p|br|strong|em|span|div)\b", text, re.I):
        return text
    return BeautifulSoup(text, "html.parser").get_text("\n")


def _heading_type(markdown_level: int | None, line: str) -> TextBlockType:
    number = re.match(r"^(\d+(?:\.\d+){0,3})", line)
    if number:
        depth = min(3, number.group(1).count(".") + 1)
        return TextBlockType(f"heading_{depth}")
    if markdown_level:
        return TextBlockType(f"heading_{min(3, markdown_level)}")
    if line.startswith("第") and ("章" in line[:8] or "节" in line[:8]):
        return TextBlockType.HEADING_1
    return TextBlockType.HEADING_1


def _should_merge(previous: TextBlock, current: TextBlock, level: MergeLevel) -> bool:
    protected = {
        TextBlockType.CODE,
        TextBlockType.TABLE,
        TextBlockType.LIST_ITEM,
        TextBlockType.QUOTE,
    }
    if previous.type in protected or current.type in protected:
        return False
    if previous.type.value.startswith("heading") or current.type.value.startswith("heading"):
        return False
    a, b = previous.text, current.text
    if not a or not b or END.search(a) or STEP.match(b) or REFERENCE.match(a) or REFERENCE.match(b):
        return False
    if a.endswith(("，", "、", "：", ",", ":", "和", "与", "及", "或")):
        return True
    if a[-1:].isascii() and b[:1].islower():
        return True
    limit = {MergeLevel.CONSERVATIVE: 24, MergeLevel.STANDARD: 60, MergeLevel.AGGRESSIVE: 100}[
        level
    ]
    return len(a) < limit and not STEP.match(a)


def _join(a: str, b: str) -> str:
    if a[-1:].isascii() and b[:1].isascii() and a[-1:].isalnum() and b[:1].isalnum():
        return f"{a} {b}"
    return a + b


def clean_text(text: str, options: CleanOptions | None = None) -> CleanResult:
    """Run deterministic block-aware cleaning without changing document meaning."""
    started = time.perf_counter()
    options = options or CleanOptions()
    original = text
    text = _html_to_text(_normalize(text))
    markdown_cleaner = MarkdownCleaner()
    blocks: list[TextBlock] = []
    markdown_count = emoji_count = separator_count = heading_count = 0
    in_code = False
    for position, raw in enumerate(text.split("\n")):
        line = raw.rstrip()
        if re.match(r"^\s*```", line):
            in_code = not in_code
            markdown_count += len(line.strip())
            continue
        if in_code:
            blocks.append(TextBlock(TextBlockType.CODE, raw, line, position))
            continue
        if TABLE.match(line):
            blocks.append(TextBlock(TextBlockType.TABLE, raw, line, position))
            continue
        if markdown_cleaner.is_separator(line):
            separator_count += 1
            markdown_count += len(line.strip())
            continue
        markdown_level: int | None = None
        parsed_markdown = None
        if options.remove_markdown:
            parsed_markdown = markdown_cleaner.clean(
                line, keep_url=options.keep_link_url, list_mode=options.list_mode
            )
            line = parsed_markdown.text
            markdown_level = parsed_markdown.heading_level
            markdown_count += parsed_markdown.removed
        quote_level = 0
        quote = re.match(r"^\s*(>+)\s*", line)
        if quote:
            quote_level = len(quote.group(1))
            line = line[quote.end() :]
            markdown_count += quote_level
        if options.remove_emoji:
            before = line
            line = emoji.replace_emoji(line, replace="")
            emoji_count += len(before) - len(line)
        if options.remove_decorations:
            line = line.translate(str.maketrans("", "", DECORATIONS))
        line = re.sub(r"[ \t]+", " ", line).strip()
        list_match = LIST.match(line) if parsed_markdown is None else None
        list_level = parsed_markdown.list_level if parsed_markdown else None
        is_list = parsed_markdown.is_list if parsed_markdown else bool(list_match)
        if list_match:
            list_level = len(list_match.group("indent")) // 2
            line = line[list_match.end() :]
        if options.normalize_punctuation:
            line = re.sub(r"([!?！？。])\1+", r"\1", line)
            line = re.sub(r"(?<=[\u4e00-\u9fff]),(?=[\u4e00-\u9fff])", "，", line)
        if not line:
            block_type = TextBlockType.BLANK
        elif markdown_level or NUMBERED.match(line):
            block_type = _heading_type(markdown_level, line)
            heading_count += 1
        elif quote_level:
            block_type = TextBlockType.QUOTE
        elif is_list:
            block_type = TextBlockType.LIST_ITEM
        else:
            block_type = TextBlockType.PARAGRAPH
        blocks.append(
            TextBlock(block_type, raw, line, position, markdown_level, list_level, raw != line)
        )
    blocks = consolidate_table_blocks(blocks)
    ai_pattern_count = AIPatternCleaner().clean(blocks)
    ai_pattern_count += URLCleaner().clean(blocks)
    merged = 0
    if options.merge_fragments:
        compact: list[TextBlock] = []
        for block in blocks:
            if compact and _should_merge(compact[-1], block, options.merge_level):
                compact[-1].text = _join(compact[-1].text, block.text)
                compact[-1].modified = True
                compact[-1].reasons.append("fragment_linebreak")
                merged += 1
            else:
                compact.append(block)
        blocks = compact
    formatted = ParagraphFormatter().format(blocks)
    result_text = formatted.text
    if options.paragraph_break_mode.value == "compact":
        layout = ParagraphLayoutEngine().render(blocks, options.paragraph_break_mode)
        result_text = layout.text
        merged += layout.removed_breaks
    residuals = detect_residuals(result_text)
    stats = CleanStats(
        original_chars=len(original),
        result_chars=len(result_text),
        removed_chars=max(0, len(original) - len(result_text)),
        merged_linebreaks=merged,
        removed_emoji=emoji_count,
        removed_markdown=markdown_count,
        removed_separators=separator_count,
        removed_ai_patterns=ai_pattern_count,
        removed_blank_lines=formatted.removed_blank_lines,
        headings_detected=heading_count,
        residual_count=len(residuals),
        elapsed_ms=(time.perf_counter() - started) * 1000,
    )
    changes = [
        f"删除 Markdown 标记 {markdown_count} 个",
        f"删除 Emoji {emoji_count} 个",
        f"删除分隔线 {separator_count} 条",
        f"删除 AI 模板 {ai_pattern_count} 处",
        f"清理多余空行 {formatted.removed_blank_lines} 处",
        f"合并换行 {merged} 处",
        f"识别标题 {heading_count} 个",
    ]
    return CleanResult(result_text, blocks, stats, changes, residuals)
