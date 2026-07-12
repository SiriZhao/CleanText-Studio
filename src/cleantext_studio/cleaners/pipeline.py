from __future__ import annotations

import html
import re
import time
import unicodedata

import emoji
import ftfy
from bs4 import BeautifulSoup

from cleantext_studio.models import (
    CleaningChange,
    CleanOptions,
    CleanResult,
    CleanStats,
    LinkMode,
    MergeLevel,
    TextBlock,
    TextBlockType,
)

from .ai_pattern_cleaner import AIPatternCleaner
from .layout import ParagraphLayoutEngine
from .markdown_cleaner import MarkdownCleaner
from .paragraph_formatter import ParagraphFormatter
from .residuals import detect_block_residuals
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
        TextBlockType.ORDERED_LIST_ITEM,
        TextBlockType.QUOTE,
    }
    if previous.type in protected or current.type in protected:
        return False
    if "#" in previous.text or "#" in current.text:
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
    direct_changes: list[CleaningChange] = []
    markdown_count = emoji_count = separator_count = heading_count = links_processed = 0
    in_code = False
    for position, raw in enumerate(text.split("\n")):
        line = raw.rstrip()
        if re.match(r"^\s*```", line):
            in_code = not in_code
            markdown_count += len(line.strip())
            continue
        if in_code:
            blocks.append(
                TextBlock(
                    TextBlockType.CODE, raw, line, position, protected=True,
                    block_id=f"b{position}", source_start=position, source_end=position,
                )
            )
            continue
        if TABLE.match(line):
            blocks.append(
                TextBlock(
                    TextBlockType.TABLE, raw, line, position, protected=True,
                    block_id=f"b{position}", source_start=position, source_end=position,
                )
            )
            continue
        if markdown_cleaner.is_separator(line):
            separator_count += 1
            markdown_count += len(line.strip())
            direct_changes.append(
                CleaningChange(
                    "horizontal_rule", "remove", raw, "", (position, position),
                    f"b{position}", 1, "删除独立 Markdown 分隔线",
                )
            )
            continue
        markdown_level: int | None = None
        parsed_markdown = None
        if options.remove_markdown:
            parsed_markdown = markdown_cleaner.clean(
                line,
                link_mode=LinkMode.TEXT_AND_URL if options.keep_link_url else options.link_mode,
                list_mode=options.list_mode,
            )
            line = parsed_markdown.text
            markdown_level = parsed_markdown.heading_level
            markdown_count += parsed_markdown.removed
            links_processed += parsed_markdown.links_processed
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
        elif quote_level:
            block_type = TextBlockType.QUOTE
        elif is_list:
            block_type = (
                TextBlockType.ORDERED_LIST_ITEM
                if parsed_markdown and parsed_markdown.ordered_index is not None
                else TextBlockType.LIST_ITEM
            )
        elif markdown_level or NUMBERED.match(line):
            block_type = _heading_type(markdown_level, line)
            heading_count += 1
        else:
            block_type = TextBlockType.PARAGRAPH
        blocks.append(
            TextBlock(
                block_type, raw, line, position, markdown_level, list_level, raw != line,
                block_id=f"b{position}", source_start=position, source_end=position,
                protected=block_type in {TextBlockType.CODE, TextBlockType.TABLE},
                list_marker=parsed_markdown.list_marker if parsed_markdown else None,
                ordered_index=parsed_markdown.ordered_index if parsed_markdown else None,
            )
        )
        if blocks[-1].modified:
            if markdown_level:
                blocks[-1].reasons.append("markdown_heading")
            elif parsed_markdown and parsed_markdown.removed:
                blocks[-1].reasons.append("markdown_marker")
            elif raw.rstrip() != line:
                blocks[-1].reasons.append("whitespace_normalization")
    blocks = consolidate_table_blocks(blocks)
    pending_blank = 0
    previous_nonblank: TextBlock | None = None
    for block in blocks:
        if block.type == TextBlockType.BLANK:
            pending_blank += 1
            continue
        block.original_blank_lines_before = pending_blank
        if previous_nonblank is not None:
            previous_nonblank.original_blank_lines_after = pending_blank
        pending_blank = 0
        previous_nonblank = block
    ai_pattern_count = (
        AIPatternCleaner().clean(blocks) if options.clean_instructional_labels else 0
    )
    ai_pattern_count += URLCleaner().clean(blocks, options.independent_url_mode)
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
    residuals = detect_block_residuals(blocks, result_text)
    table_count = sum(block.table is not None for block in blocks)
    list_count = sum("list_item" in block.type.value for block in blocks)
    change_records = direct_changes + [
        CleaningChange(
            rule_id=block.reasons[-1] if block.reasons else "block_cleanup",
            change_type="remove" if not block.text else "replace",
            original_text=block.original_text[:120],
            cleaned_text=block.text[:120],
            source_range=(block.source_start, block.source_end),
            block_id=block.block_id,
            count=1,
            reason="、".join(block.reasons) or "格式规范化",
        )
        for block in blocks
        if block.modified and block.original_text != block.text
    ]
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
        tables_detected=table_count,
        tables_preserved=table_count,
        list_items_detected=list_count,
        links_processed=links_processed,
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
    return CleanResult(result_text, blocks, stats, changes, residuals, change_records)
