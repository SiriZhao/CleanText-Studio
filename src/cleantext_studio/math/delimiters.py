from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DelimitedFormula:
    raw_source: str
    expression_source: str
    delimiter_type: str
    display: bool


def strip_formula_delimiters(source: str) -> DelimitedFormula:
    value = source.strip()
    for left, right, kind, display in (
        ("$$", "$$", "dollar_display", True),
        (r"\[", r"\]", "bracket_display", True),
        (r"\(", r"\)", "paren_inline", False),
        ("$", "$", "dollar_inline", False),
    ):
        if value.startswith(left) and value.endswith(right) and len(value) >= len(left) + len(right):
            return DelimitedFormula(source, value[len(left):-len(right)].strip(), kind, display)
    environment = re.fullmatch(r"\\begin\{([^}]+)\}([\s\S]*)\\end\{\1\}", value)
    if environment:
        name = environment.group(1)
        return DelimitedFormula(source, value, f"environment:{name}", True)
    return DelimitedFormula(source, value, "none", False)
