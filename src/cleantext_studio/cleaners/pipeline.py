from __future__ import annotations

import html
import re
import time
import unicodedata

import emoji
import ftfy
from bs4 import BeautifulSoup

from cleantext_studio.math import MathDetector, MathNormalizer, detect_math_warnings
from cleantext_studio.math.protector import MathProtector, ProtectedMath
from cleantext_studio.models import (
    CleaningChange,
    CleanOptions,
    CleanResult,
    CleanStats,
    LinkMode,
    MergeLevel,
    ResidualWarning,
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
        TextBlockType.DISPLAY_MATH,
        TextBlockType.MATH_PARAGRAPH,
        TextBlockType.EQUATION_GROUP,
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
    math_protector = MathProtector(options.normalize_math_spacing, options.math_output_mode)
    math_detector = MathDetector()
    markdown_cleaner = MarkdownCleaner()
    blocks: list[TextBlock] = []
    direct_changes: list[CleaningChange] = []
    markdown_count = emoji_count = separator_count = heading_count = links_processed = 0
    in_code = False
    raw_lines = text.split("\n")
    position = 0
    while position < len(raw_lines):
        raw = raw_lines[position]
        line = raw.rstrip()
        if re.match(r"^\s*```", line):
            in_code = not in_code
            markdown_count += len(line.strip())
            position += 1
            continue
        if in_code:
            blocks.append(
                TextBlock(
                    TextBlockType.CODE,
                    raw,
                    line,
                    position,
                    protected=True,
                    block_id=f"b{position}",
                    source_start=position,
                    source_end=position,
                )
            )
            position += 1
            continue
        if options.detect_math:
            stripped = line.strip()
            display_end: str | None = None
            content_start = ""
            environment = math_detector.environment_start(stripped)
            if stripped.startswith("$$"):
                display_end, content_start = "$$", stripped[2:]
            elif stripped.startswith(r"\["):
                display_end, content_start = r"\]", stripped[2:]
            if display_end is not None or environment is not None:
                collected = [raw]
                if (
                    display_end
                    and content_start.endswith(display_end)
                    and len(content_start) > len(display_end)
                ):
                    content = content_start[: -len(display_end)].strip()
                else:
                    cursor = position + 1
                    while cursor < len(raw_lines) and cursor - position < 1000:
                        collected.append(raw_lines[cursor])
                        if (
                            display_end
                            and re.match(
                                rf".*{re.escape(display_end)}(?:\s*[（(]\d+[)）])?\s*$",
                                raw_lines[cursor],
                            )
                        ) or (
                            environment
                            and math_detector.environment_ended(raw_lines[cursor], environment)
                        ):
                            break
                        cursor += 1
                    position = cursor
                    source = "\n".join(collected)
                    if display_end:
                        body = source.strip()[2:]
                        content = re.sub(
                            rf"{re.escape(display_end)}(?:\s*[（(]\d+[)）])?\s*$", "", body
                        ).strip()
                    else:
                        content = source.strip()
                source = "\n".join(collected)
                equation_match = re.search(r"[（(]\d+[)）]\s*$", source)
                equation_number = (
                    equation_match.group()
                    if equation_match and options.preserve_equation_numbers
                    else None
                )
                if equation_number and display_end:
                    content = re.sub(
                        rf"{re.escape(display_end)}\s*{re.escape(equation_number)}\s*$", "", content
                    ).strip()
                data = math_protector.display_data(
                    source, content, position - len(collected) + 1, position, equation_number
                )
                warnings = detect_math_warnings(source, f"b{position}", position + 1)
                data.warnings.extend(w.warning_type for w in warnings)
                if options.math_output_mode.value == "unicode":
                    rendered_math = MathNormalizer().to_unicode(data.normalized_text)
                elif source.strip().startswith("$$"):
                    rendered_math = f"$$\n{data.normalized_text}\n$$"
                elif source.strip().startswith(r"\["):
                    rendered_math = f"\\[\n{data.normalized_text}\n\\]"
                else:
                    rendered_math = source
                if data.equation_number:
                    rendered_math += f" {data.equation_number}"
                blocks.append(
                    TextBlock(
                        TextBlockType.DISPLAY_MATH,
                        source,
                        rendered_math,
                        position,
                        protected=True,
                        block_id=f"b{position}",
                        source_start=data.source_start,
                        source_end=data.source_end,
                        math=data,
                        warnings=list(data.warnings),
                    )
                )
                position += 1
                continue
            standalone = math_detector.detect_line(line)
            if standalone and standalone.display_mode.value == "block":
                normalized = (
                    MathNormalizer().normalize(standalone.content)
                    if options.normalize_math_spacing
                    else standalone.content
                )
                from cleantext_studio.models import MathBlockData

                data = MathBlockData(
                    standalone.source,
                    normalized,
                    standalone.math_format,
                    standalone.display_mode,
                    standalone.equation_number,
                    position,
                    position,
                    standalone.confidence,
                )
                blocks.append(
                    TextBlock(
                        TextBlockType.MATH_PARAGRAPH,
                        raw,
                        normalized,
                        position,
                        protected=True,
                        block_id=f"b{position}",
                        source_start=position,
                        source_end=position,
                        math=data,
                    )
                )
                position += 1
                continue
        if TABLE.match(line):
            blocks.append(
                TextBlock(
                    TextBlockType.TABLE,
                    raw,
                    line,
                    position,
                    protected=True,
                    block_id=f"b{position}",
                    source_start=position,
                    source_end=position,
                )
            )
            position += 1
            continue
        if markdown_cleaner.is_separator(line):
            separator_count += 1
            markdown_count += len(line.strip())
            direct_changes.append(
                CleaningChange(
                    "horizontal_rule",
                    "remove",
                    raw,
                    "",
                    (position, position),
                    f"b{position}",
                    1,
                    "删除独立 Markdown 分隔线",
                )
            )
            position += 1
            continue
        inline_math: list[ProtectedMath] = []
        if options.detect_math and options.protect_math:
            line, inline_math = math_protector.protect_inline(line, position)
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
        line = math_protector.restore(line, inline_math)
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
                block_type,
                raw,
                line,
                position,
                markdown_level,
                list_level,
                raw != line,
                block_id=f"b{position}",
                source_start=position,
                source_end=position,
                protected=block_type in {TextBlockType.CODE, TextBlockType.TABLE},
                list_marker=parsed_markdown.list_marker if parsed_markdown else None,
                ordered_index=parsed_markdown.ordered_index if parsed_markdown else None,
                metadata={"inline_math": [item.data for item in inline_math]},
            )
        )
        if blocks[-1].modified:
            if markdown_level:
                blocks[-1].reasons.append("markdown_heading")
            elif parsed_markdown and parsed_markdown.removed:
                blocks[-1].reasons.append("markdown_marker")
            elif raw.rstrip() != line:
                blocks[-1].reasons.append("whitespace_normalization")
        position += 1
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
    ai_pattern_count = AIPatternCleaner().clean(blocks) if options.clean_instructional_labels else 0
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
    math_warnings = []
    for block in blocks:
        if block.type not in {TextBlockType.CODE, TextBlockType.TABLE}:
            math_warnings.extend(
                detect_math_warnings(block.original_text, block.block_id, block.position + 1)
            )
    residuals.extend(
        ResidualWarning(
            line=warning.line_number,
            kind=f"math:{warning.warning_type}",
            excerpt=warning.snippet,
            severity=warning.severity,
            suggestion=warning.suggestion,
            block_id=warning.block_id,
        )
        for warning in math_warnings
    )
    table_count = sum(block.table is not None for block in blocks)
    table_formula_count = sum(
        len(math_detector.detect_inline(cell))
        for block in blocks
        if block.table is not None
        for row in [block.table.headers, *block.table.rows]
        for cell in row
    )
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
        formulas_detected=sum(bool(block.math) for block in blocks)
        + sum(
            len(value) if isinstance((value := block.metadata.get("inline_math")), list) else 0
            for block in blocks
        )
        + table_formula_count,
        inline_formulas_detected=sum(
            len(value) if isinstance((value := block.metadata.get("inline_math")), list) else 0
            for block in blocks
        )
        + table_formula_count,
        display_formulas_detected=sum(block.math is not None for block in blocks),
        formulas_normalized=sum(
            bool(block.math and block.math.normalized_text != block.math.source_text)
            for block in blocks
        ),
        formula_warnings=len(math_warnings),
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
