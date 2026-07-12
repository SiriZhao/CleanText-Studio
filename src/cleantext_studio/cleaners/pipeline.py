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
    ListMode,
    MergeLevel,
    TextBlock,
    TextBlockType,
)

from .layout import ParagraphLayoutEngine
from .residuals import detect_residuals
from .tables import consolidate_table_blocks

MARKDOWN_HEADING = re.compile(r"^[\s\u3000]*([#＃]{1,6})[\s\u3000]*")
OUTER_EMPHASIS = re.compile(r"^(?:\*{1,3}|_{1,3})(.*?)(?:\*{1,3}|_{1,3})$")
NUMBERED = re.compile(
    r"^(?:第一[章节篇部]|[一二三四五六七八九十]+、|（[一二三四五六七八九十]+）|"
    r"\d+(?:\.\d+){1,3}(?:\s+|$))"
)
LIST = re.compile(r"^(?P<indent>\s*)(?P<marker>[-+*•▪◦]|\d+[.、)]|[（(]\d+[）)])\s+")
TABLE = re.compile(r"^\s*\|.*\|\s*$")
END = re.compile(r"[。！？.!?；;]$")
STEP = re.compile(r"^(?:第[一二三四五六七八九十]+步|步骤\s*\d+|Step\s+\d+)")
REFERENCE = re.compile(r"^\s*(?:\[\d+]|\d+\.\s+).*(?:19|20)\d{2}")
SEPARATOR = re.compile(r"^\s*(?:(?:[-*_—]\s*){3,})$")
DECORATIONS = "◆◇■□●○▶▷★☆🔹🔸"
OPENERS = ("当然可以，以下是整理后的内容", "好的，下面为你整理", "以下是优化后的版本")
CLOSERS = (
    "希望以上内容对你有所帮助",
    "如有需要，我可以继续修改",
    "如果你愿意，我还可以",
    "以上就是完整内容",
)


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


def _strip_inline_markdown(line: str, keep_url: bool) -> tuple[str, int]:
    old = line
    line = re.sub(
        r"!\[([^]]*)]\(([^)]+)\)",
        lambda m: f"[图片：{m.group(1)}]" if m.group(1) else "[图片]",
        line,
    )
    line = re.sub(
        r"(?<!!)\[([^]]+)]\(([^)]+)\)",
        (r"\1（\2）" if keep_url else r"\1"),
        line,
    )
    line = re.sub(r"(?<!\\)(\*{3}|_{3})(.+?)\1", r"\2", line)
    line = re.sub(r"(?<!\\)(\*\*|__)(.+?)\1", r"\2", line)
    line = re.sub(r"(?<![\w\\])([*_])([^\n*_]+?)\1(?!\w)", r"\2", line)
    line = re.sub(r"(?<!\\)`([^`]+)`", r"\1", line)
    line = re.sub(r"\\([#*_>`])", r"\1", line)
    return line, max(0, len(old) - len(line))


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


def _trim_chat_phrases(blocks: list[TextBlock]) -> int:
    removed = 0
    for index in list(range(min(3, len(blocks)))):
        if index < len(blocks) and blocks[index].text.rstrip("：:。.!！ ").startswith(OPENERS):
            blocks[index].text = ""
            removed += 1
    for index in range(max(0, len(blocks) - 3), len(blocks)):
        if blocks[index].text.rstrip("：:。.!！ ").startswith(CLOSERS):
            blocks[index].text = ""
            removed += 1
    return removed


def clean_text(text: str, options: CleanOptions | None = None) -> CleanResult:
    """Run deterministic block-aware cleaning without changing document meaning."""
    started = time.perf_counter()
    options = options or CleanOptions()
    original = text
    text = _html_to_text(_normalize(text))
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
        if SEPARATOR.fullmatch(line):
            separator_count += 1
            markdown_count += len(line.strip())
            continue
        markdown_level: int | None = None
        heading_match = MARKDOWN_HEADING.match(line)
        if heading_match:
            markdown_level = len(heading_match.group(1))
            markdown_count += len(heading_match.group(0))
            line = line[heading_match.end() :]
        outer = OUTER_EMPHASIS.match(line)
        if outer and MARKDOWN_HEADING.match(outer.group(1)):
            line = outer.group(1)
            heading_match = MARKDOWN_HEADING.match(line)
            assert heading_match is not None
            markdown_level = len(heading_match.group(1))
            line = line[heading_match.end() :]
        if options.remove_markdown:
            line, removed = _strip_inline_markdown(line, options.keep_link_url)
            markdown_count += removed
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
        list_match = LIST.match(line)
        list_level = None
        if list_match:
            list_level = len(list_match.group("indent")) // 2
            content = line[list_match.end() :]
            if options.list_mode == ListMode.KEEP:
                marker = list_match.group("marker")
                line = f"• {content}" if marker in "-+*•▪◦" else f"{marker} {content}"
            else:
                line = content
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
        elif list_match:
            block_type = TextBlockType.LIST_ITEM
        else:
            block_type = TextBlockType.PARAGRAPH
        blocks.append(
            TextBlock(block_type, raw, line, position, markdown_level, list_level, raw != line)
        )
    blocks = consolidate_table_blocks(blocks)
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
    output: list[str] = []
    for block in blocks:
        if block.text or (output and output[-1]):
            output.append(block.text)
    while output and not output[-1]:
        output.pop()
    result_text = "\n".join(output)
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
        headings_detected=heading_count,
        residual_count=len(residuals),
        elapsed_ms=(time.perf_counter() - started) * 1000,
    )
    changes = [
        f"删除 Markdown 标记 {markdown_count} 个",
        f"删除 Emoji {emoji_count} 个",
        f"删除分隔线 {separator_count} 条",
        f"合并换行 {merged} 处",
        f"识别标题 {heading_count} 个",
    ]
    return CleanResult(result_text, blocks, stats, changes, residuals)
