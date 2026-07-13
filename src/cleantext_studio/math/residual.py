from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class MathWarning:
    warning_type: str
    severity: str
    block_id: str
    line_number: int
    snippet: str
    suggestion: str


def detect_math_warnings(text: str, block_id: str = "", line_number: int = 1) -> list[MathWarning]:
    warnings: list[MathWarning] = []
    if text.count("$$") % 2:
        warnings.append(
            MathWarning(
                "unclosed_display_dollar",
                "warning",
                block_id,
                line_number,
                text[:100],
                "检查 $$ 块级公式定界符",
            )
        )
    without_currency = re.sub(r"\$\s*\d+(?:[.,]\d+)?", "", text.replace("$$", ""))
    single = without_currency.count("$")
    # A single currency prefix such as $199 is not a math delimiter.
    if single % 2:
        warnings.append(
            MathWarning(
                "unclosed_inline_dollar",
                "warning",
                block_id,
                line_number,
                text[:100],
                "检查 $ 行内公式定界符",
            )
        )
    for opening, closing, kind in ((r"\(", r"\)", "paren"), (r"\[", r"\]", "bracket")):
        if text.count(opening) != text.count(closing):
            warnings.append(
                MathWarning(
                    f"unbalanced_{kind}",
                    "warning",
                    block_id,
                    line_number,
                    text[:100],
                    "检查 LaTeX 公式定界符",
                )
            )
    depth = 0
    for char in text:
        depth += char == "{"
        depth -= char == "}"
        if depth < 0:
            break
    if depth:
        warnings.append(
            MathWarning(
                "unbalanced_braces", "warning", block_id, line_number, text[:100], "检查公式花括号"
            )
        )
    begins = re.findall(r"\\begin\{([^}]+)\}", text)
    ends = re.findall(r"\\end\{([^}]+)\}", text)
    if begins != ends:
        warnings.append(
            MathWarning(
                "unbalanced_environment",
                "warning",
                block_id,
                line_number,
                text[:100],
                "检查 LaTeX 环境的 begin/end",
            )
        )
    if r"\frac" in text and not re.search(r"\\frac\s*\{[^{}]+\}\s*\{[^{}]+\}", text):
        warnings.append(
            MathWarning(
                "incomplete_fraction",
                "warning",
                block_id,
                line_number,
                text[:100],
                "检查 \\frac 的两个参数",
            )
        )
    return warnings
