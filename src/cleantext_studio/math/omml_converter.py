from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from docx.oxml import OxmlElement
from docx.oxml.ns import qn

_GREEK = {"alpha": "α", "beta": "β", "gamma": "γ", "pi": "π", "infty": "∞"}
_OPERATORS = {
    "le": "≤",
    "ge": "≥",
    "ne": "≠",
    "approx": "≈",
    "times": "×",
    "div": "÷",
    "mid": "|",
    "sum": "∑",
    "int": "∫",
}
_SUPPORTED_COMMANDS = (
    set(_GREEK)
    | set(_OPERATORS)
    | {
        "frac",
        "sqrt",
        "left",
        "right",
        "begin",
        "end",
    }
)


@dataclass(slots=True)
class OMMLConversionResult:
    element: Any | None
    converted: bool
    fallback_text: str
    warning: str | None = None


class OMMLConverter:
    """Convert a safe, useful LaTeX subset to native Office Math nodes."""

    def convert(self, expression: str, display: bool = False) -> OMMLConversionResult:
        try:
            unknown = set(re.findall(r"\\([A-Za-z]+)", expression)) - _SUPPORTED_COMMANDS
            if unknown:
                raise ValueError(f"不支持的 LaTeX 命令: {', '.join(sorted(unknown))}")
            root = OxmlElement("m:oMathPara") if display else OxmlElement("m:oMath")
            math = OxmlElement("m:oMath") if display else root
            if display:
                root.append(math)
            self._append_expression(math, self._strip_delimiters(expression.strip()), 0)
            return OMMLConversionResult(root, True, expression)
        except (ValueError, IndexError, RecursionError) as exc:
            return OMMLConversionResult(None, False, expression, str(exc))

    def _append_expression(self, parent: Any, expression: str, depth: int) -> None:
        if depth > 24 or len(expression) > 20000:
            raise ValueError("公式超过安全复杂度限制")
        frac = self._full_command(expression, "frac", 2)
        if frac:
            node = OxmlElement("m:f")
            numerator, denominator = OxmlElement("m:num"), OxmlElement("m:den")
            self._append_expression(numerator, frac[0], depth + 1)
            self._append_expression(denominator, frac[1], depth + 1)
            node.extend((numerator, denominator))
            parent.append(node)
            return
        sqrt = self._full_command(expression, "sqrt", 1)
        if sqrt:
            radical, degree, element = (
                OxmlElement("m:rad"),
                OxmlElement("m:deg"),
                OxmlElement("m:e"),
            )
            self._append_expression(element, sqrt[0], depth + 1)
            radical.extend((degree, element))
            parent.append(radical)
            return
        matrix = re.fullmatch(r"\\begin\{([pb]?matrix)\}(.+)\\end\{\1\}", expression, re.S)
        if matrix:
            self._append_matrix(parent, matrix.group(2), depth)
            return
        scripts = re.fullmatch(r"(.+?)(?:_\{?([^{}^]+)\}?)?(?:\^\{?([^{}]+)\}?)?", expression)
        if scripts and (scripts.group(2) or scripts.group(3)):
            base, sub, sup = scripts.groups()
            tag = "m:sSubSup" if sub and sup else ("m:sSub" if sub else "m:sSup")
            node, element = OxmlElement(tag), OxmlElement("m:e")
            self._append_text(element, base)
            node.append(element)
            if sub:
                sub_node = OxmlElement("m:sub")
                self._append_text(sub_node, sub)
                node.append(sub_node)
            if sup:
                sup_node = OxmlElement("m:sup")
                self._append_text(sup_node, sup)
                node.append(sup_node)
            parent.append(node)
            return
        self._append_text(parent, expression)

    def _append_matrix(self, parent: Any, body: str, depth: int) -> None:
        matrix = OxmlElement("m:m")
        for raw_row in re.split(r"\\\\", body.strip()):
            row = OxmlElement("m:mr")
            for raw_cell in raw_row.split("&"):
                cell = OxmlElement("m:e")
                self._append_expression(cell, raw_cell.strip(), depth + 1)
                row.append(cell)
            matrix.append(row)
        parent.append(matrix)

    def _append_text(self, parent: Any, value: str) -> None:
        value = re.sub(
            r"\\([A-Za-z]+)",
            lambda m: _GREEK.get(m.group(1), _OPERATORS.get(m.group(1), m.group(0))),
            value,
        )
        run, text = OxmlElement("m:r"), OxmlElement("m:t")
        text.set(qn("xml:space"), "preserve")
        text.text = value
        run.append(text)
        parent.append(run)

    @staticmethod
    def _full_command(text: str, command: str, groups: int) -> list[str] | None:
        prefix = f"\\{command}"
        if not text.startswith(prefix):
            return None
        position, result = len(prefix), []
        for _ in range(groups):
            while position < len(text) and text[position].isspace():
                position += 1
            if position >= len(text) or text[position] != "{":
                return None
            start, level = position + 1, 1
            position += 1
            while position < len(text) and level:
                level += text[position] == "{"
                level -= text[position] == "}"
                position += 1
            if level:
                raise ValueError("未闭合的命令参数")
            result.append(text[start : position - 1])
        return result if not text[position:].strip() else None

    @staticmethod
    def _strip_delimiters(text: str) -> str:
        for left, right in (("$$", "$$"), (r"\[", r"\]"), (r"\(", r"\)"), ("$", "$")):
            if text.startswith(left) and text.endswith(right):
                return text[len(left) : -len(right)].strip()
        return text
