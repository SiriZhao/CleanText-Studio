from __future__ import annotations

import re

import emoji

from cleantext_studio.models import ResidualWarning, TextBlock, TextBlockType

PATTERNS = (
    ("markdown_heading", re.compile(r"^\s*[#＃]+")),
    ("separator", re.compile(r"^\s*(?:(?:[-*_—]\s*){3,})$")),
    ("markdown_emphasis", re.compile(r"(?:\*\*|__)[^\n]+(?:\*\*|__)")),
    ("markdown_link", re.compile(r"!?\[[^]]*]\([^)]+\)")),
    ("code_fence", re.compile(r"^\s*```")),
    ("quote_marker", re.compile(r"^\s*>")),
    ("html_tag", re.compile(r"</?(?:p|br|strong|em|span|div)\b", re.I)),
    ("trailing_space", re.compile(r"[ \t]+$")),
    (
        "instructional_label",
        re.compile(r"^\s*(?:填写|输入|点击|打开|进入|选择|上传|等待|确认|保存|提交|访问|登录)\s*[：:]\s*$"),
    ),
)


def detect_residuals(text: str) -> list[ResidualWarning]:
    """Return suspicious formatting outside fenced code and Markdown tables."""
    warnings: list[ResidualWarning] = []
    in_code = False
    for number, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*```", line):
            in_code = not in_code
            continue
        if in_code or re.match(r"^\s*\|.*\|\s*$", line):
            continue
        for kind, pattern in PATTERNS:
            if pattern.search(line):
                warnings.append(ResidualWarning(number, kind, line[:120]))
                break
        else:
            if emoji.emoji_count(line):
                warnings.append(ResidualWarning(number, "emoji", line[:120]))
    if re.search(r"\n{3,}", text):
        warnings.append(ResidualWarning(1, "excess_blank_lines", "连续空行"))
    return warnings


def detect_block_residuals(blocks: list[TextBlock], rendered_text: str) -> list[ResidualWarning]:
    """Detect residuals while excluding protected code and valid table blocks."""
    warnings: list[ResidualWarning] = []
    for block in blocks:
        if block.type == TextBlockType.TABLE and block.table and block.table.malformed_rows:
            warnings.append(
                ResidualWarning(
                    block.position + 1,
                    "malformed_table",
                    block.text[:120],
                    block_id=block.block_id,
                )
            )
        if not block.text or block.protected or block.type in {TextBlockType.CODE, TextBlockType.TABLE}:
            continue
        for kind, pattern in PATTERNS:
            match = pattern.search(block.text)
            if match:
                warnings.append(
                    ResidualWarning(
                        block.position + 1,
                        kind,
                        block.text[:120],
                        match.start() + 1,
                        "warning",
                        "检查该结构或再次清理",
                        block.block_id,
                    )
                )
                break
        else:
            if emoji.emoji_count(block.text):
                warnings.append(
                    ResidualWarning(
                        block.position + 1, "emoji", block.text[:120], block_id=block.block_id
                    )
                )
    if re.search(r"\n{3,}", rendered_text):
        warnings.append(ResidualWarning(1, "excess_blank_lines", "连续空行"))
    return warnings
