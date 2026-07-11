from __future__ import annotations

import html
import re
import time

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

HEADING_RE = re.compile(r"^(?P<marks>#{1,3})\s+(?P<text>.+)$")
NUMBERED_HEADING_RE = re.compile(
    r"^(第一[章节篇部]|[一二三四五六七八九十]+、|（[一二三四五六七八九十]+）|\d+(?:\.\d+){1,2}\s+).+"
)
LIST_RE = re.compile(r"^\s*(?:[-+*•]\s+|\d+[.、)]\s+|[（(]\d+[）)]\s+)")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
END_RE = re.compile(r"[。！？.!?；;：:]$|[”’\"']$")
DECORATIONS = "◆◇■□●○▶▷★☆🔹🔸"
OPENERS = ("以下是整理后的内容", "以下为优化后的版本", "当然可以", "好的，下面是")
CLOSERS = (
    "希望以上内容对你有所帮助",
    "如有需要，我还可以继续",
    "如果你愿意，我可以",
    "以上就是完整内容",
)


def _markdown(line: str, options: CleanOptions) -> tuple[str, int, int | None]:
    count = 0
    level = None
    match = HEADING_RE.match(line)
    if match:
        level = len(match.group("marks"))
        count += level
        line = match.group("text")
    if re.fullmatch(r"\s{0,3}(?:-{3,}|\*{3,}|_{3,})\s*", line):
        return "", count + len(line.strip()), level
    old = line
    line = re.sub(r"\[([^]]+)]\(([^)]+)\)", (r"\1 (\2)" if options.keep_link_url else r"\1"), line)
    line = re.sub(r"(?<!\w)(\*\*|__)(.+?)\1(?!\w)", r"\2", line)
    line = re.sub(r"(?<!\w)([*_])([^\n*_]+?)\1(?!\w)", r"\2", line)
    line = re.sub(r"`([^`]+)`", r"\1", line)
    line = re.sub(r"^\s*>\s?", "", line)
    return line, count + max(0, len(old) - len(line)), level


def _is_heading(line: str) -> bool:
    return bool(NUMBERED_HEADING_RE.match(line)) or (len(line) <= 30 and line.endswith(("：", ":")))


def _join(a: str, b: str) -> str:
    if a and b and a[-1].isascii() and b[0].isascii() and (a[-1].isalnum() and b[0].isalnum()):
        return a + " " + b
    return a + b


def _should_merge(a: str, b: str, level: MergeLevel) -> bool:
    if a.startswith("\ue000") or b.startswith("\ue000"):
        return False
    if not a or not b or _is_heading(a) or _is_heading(b) or LIST_RE.match(a) or LIST_RE.match(b):
        return False
    if END_RE.search(a):
        return False
    if len(a) <= 20 and not re.search(r"[，,、：:]", a) and END_RE.search(b):
        return False
    if a.endswith(("，", "、", ",", "和", "与", "及", "或")):
        return True
    if a[-1:].isascii() and b[:1].isascii() and b[:1].islower():
        return True
    if level == MergeLevel.CONSERVATIVE:
        return len(a) < 25
    if level == MergeLevel.AGGRESSIVE:
        return len(a) < 100
    return len(a) < 60


def clean_text(text: str, options: CleanOptions | None = None) -> CleanResult:
    """Clean text with a deterministic, idempotent and block-aware pipeline."""
    started = time.perf_counter()
    options = options or CleanOptions()
    original = text
    text = ftfy.fix_text(html.unescape(text)).replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"(?<=[\u4e00-\u9fff]),(?=(?:\n)?[\u4e00-\u9fff])", "\uff0c", text)
    if "<" in text and ">" in text:
        text = BeautifulSoup(text, "html.parser").get_text("\n")
    lines = text.split("\n")
    blocks: list[TextBlock] = []
    output: list[str] = []
    markdown_count = emoji_count = merged = 0
    in_code = False
    for pos, raw in enumerate(lines):
        line = raw.rstrip()
        if re.match(r"^\s*```", line):
            in_code = not in_code
            markdown_count += len(line.strip())
            continue
        if in_code:
            blocks.append(TextBlock(TextBlockType.CODE, raw, line, pos))
            output.append(line)
            continue
        is_table = bool(TABLE_RE.match(line))
        heading_level = None
        if options.remove_markdown and not is_table:
            line, removed, heading_level = _markdown(line, options)
            markdown_count += removed
        if options.remove_emoji:
            before = line
            line = emoji.replace_emoji(line, replace="")
            emoji_count += len(before) - len(line)
        if options.remove_decorations and not (options.keep_bullets and LIST_RE.match(line)):
            line = line.translate(str.maketrans("", "", DECORATIONS))
        line = re.sub(r"[ \t]+", " ", line).strip()
        if options.normalize_punctuation:
            line = re.sub(r"([!?！？。])\1+", r"\1", line)
        block_type = TextBlockType.TABLE if is_table else TextBlockType.PARAGRAPH
        if heading_level:
            block_type = TextBlockType(f"heading_{heading_level}")
            line = "\ue000" + line
        elif LIST_RE.match(line):
            block_type = TextBlockType.LIST_ITEM
            if not options.keep_bullets:
                line = LIST_RE.sub("", line)
        elif _is_heading(line):
            block_type = TextBlockType.HEADING_1
        elif not line:
            block_type = TextBlockType.BLANK
        blocks.append(TextBlock(block_type, raw, line, pos, heading_level, modified=raw != line))
        if line or (output and output[-1] != ""):
            output.append(line)
    if options.merge_fragments:
        merged_output: list[str] = []
        for line in output:
            if (
                merged_output
                and line
                and merged_output[-1]
                and not TABLE_RE.match(line)
                and not TABLE_RE.match(merged_output[-1])
                and _should_merge(merged_output[-1], line, options.merge_level)
            ):
                merged_output[-1] = _join(merged_output[-1], line)
                merged += 1
            else:
                merged_output.append(line)
        output = merged_output
    while output and not output[-1]:
        output.pop()
    result = "\n".join(output).replace("\ue000", "")
    if options.remove_template_phrases and result:
        parts = result.splitlines()
        if parts and parts[0].rstrip("：:。. ").startswith(OPENERS):
            parts.pop(0)
        while parts and not parts[-1]:
            parts.pop()
        if parts and parts[-1].rstrip("。.!！ ").startswith(CLOSERS):
            parts.pop()
        result = "\n".join(parts).strip()
    stats = CleanStats(
        len(original),
        len(result),
        max(0, len(original) - len(result)),
        merged,
        emoji_count,
        markdown_count,
        (time.perf_counter() - started) * 1000,
    )
    changes = [
        f"合并换行 {merged} 处",
        f"删除 Emoji {emoji_count} 个",
        f"删除 Markdown 标记 {markdown_count} 个",
    ]
    return CleanResult(result, blocks, stats, changes)
