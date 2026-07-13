from __future__ import annotations

import re


class MathNormalizer:
    """Apply conservative presentation-only LaTeX normalization."""

    def normalize(self, expression: str) -> str:
        value = expression.strip()
        value = re.sub(r"\\(frac|sqrt)\s+\{", r"\\\1{", value)
        value = re.sub(r"\}\s+\{", "}{", value)
        value = re.sub(r"\{\s+([^{}]*?)\s+\}", r"{\1}", value)
        value = re.sub(r"\s*([_^])\s*", r"\1", value)
        value = re.sub(r"(?<!\\)\s*([+=])\s*", r" \1 ", value)
        value = re.sub(r"[ \t]{2,}", " ", value)
        return value.strip()

    def to_latex(self, expression: str) -> str:
        replacements = {
            "×": r"\times ",
            "÷": r"\div ",
            "≤": r"\le ",
            "≥": r"\ge ",
            "≠": r"\ne ",
            "≈": r"\approx ",
            "∑": r"\sum ",
            "∫": r"\int ",
            "α": r"\alpha ",
            "β": r"\beta ",
            "γ": r"\gamma ",
            "π": r"\pi ",
            "∞": r"\infty ",
        }
        value = expression
        for source, target in replacements.items():
            value = value.replace(source, target)
        return self.normalize(value)

    def to_unicode(self, expression: str) -> str:
        replacements = {
            r"\times": "×",
            r"\div": "÷",
            r"\le": "≤",
            r"\ge": "≥",
            r"\ne": "≠",
            r"\approx": "≈",
            r"\sum": "∑",
            r"\int": "∫",
            r"\alpha": "α",
            r"\beta": "β",
            r"\gamma": "γ",
            r"\pi": "π",
            r"\infty": "∞",
        }
        value = expression
        for source, target in replacements.items():
            value = value.replace(source, target)
        superscripts = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        value = re.sub(
            r"\^\{?(\d+)\}?", lambda match: match.group(1).translate(superscripts), value
        )
        return self.normalize(value)
