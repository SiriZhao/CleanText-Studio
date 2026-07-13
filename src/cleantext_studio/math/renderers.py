from __future__ import annotations

import html
from typing import Any

from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from .ast import (
    Cases,
    FormulaNode,
    Fraction,
    Function,
    GreekLetter,
    Group,
    Identifier,
    Matrix,
    Nary,
    Number,
    Operator,
    Relation,
    Root,
    Sequence,
    Subscript,
    SubSuperscript,
    Superscript,
    Text,
)


class UnicodeFormulaRenderer:
    """Create a readable, delimiter-free fallback without changing meaning."""

    def render(self, node: FormulaNode) -> str:
        if isinstance(node, (Identifier, Number, Operator, Relation, Text, GreekLetter)):
            return node.value
        if isinstance(node, Function):
            return node.name
        if isinstance(node, Sequence):
            return "".join(self.render(child) for child in node.children)
        if isinstance(node, Group):
            return self.render(node.content)
        if isinstance(node, Superscript):
            return f"{self.render(node.base)}^({self.render(node.exponent)})"
        if isinstance(node, Subscript):
            return f"{self.render(node.base)}_({self.render(node.subscript)})"
        if isinstance(node, SubSuperscript):
            return (
                f"{self.render(node.base)}_({self.render(node.subscript)})"
                f"^({self.render(node.exponent)})"
            )
        if isinstance(node, Fraction):
            return f"({self.render(node.numerator)})/({self.render(node.denominator)})"
        if isinstance(node, Root):
            return f"√({self.render(node.radicand)})"
        if isinstance(node, Nary):
            return node.symbol + self.render(node.body)
        if isinstance(node, Matrix):
            rows = [", ".join(self.render(cell) for cell in row) for row in node.rows]
            return "[" + "; ".join(rows) + "]"
        if isinstance(node, Cases):
            rows = [", ".join(self.render(cell) for cell in row) for row in node.rows]
            return "{ " + "; ".join(rows)
        raise TypeError(type(node).__name__)


class PreviewFormulaRenderer:
    """Render the safe AST as local Qt rich text, with no scripts or network."""

    def render(self, node: FormulaNode) -> str:
        return (
            '<span style="font-family:\'Cambria Math\',serif;font-size:16px">'
            f"{self._node(node)}</span>"
        )

    def _node(self, node: FormulaNode) -> str:
        if isinstance(node, (Identifier, Number, Operator, Relation, Text, GreekLetter)):
            return html.escape(node.value)
        if isinstance(node, Function):
            return f'<span style="font-style:normal">{html.escape(node.name)}</span>'
        if isinstance(node, Sequence):
            return "".join(self._node(child) for child in node.children)
        if isinstance(node, Group):
            return self._node(node.content)
        if isinstance(node, Superscript):
            return f"{self._node(node.base)}<sup>{self._node(node.exponent)}</sup>"
        if isinstance(node, Subscript):
            return f"{self._node(node.base)}<sub>{self._node(node.subscript)}</sub>"
        if isinstance(node, SubSuperscript):
            return (
                f"{self._node(node.base)}<sub>{self._node(node.subscript)}</sub>"
                f"<sup>{self._node(node.exponent)}</sup>"
            )
        if isinstance(node, Fraction):
            return (
                '<table cellspacing="0" cellpadding="1" style="display:inline-table">'
                '<tr><td align="center" style="border-bottom:1px solid">'
                f"{self._node(node.numerator)}</td></tr>"
                f'<tr><td align="center">{self._node(node.denominator)}</td></tr></table>'
            )
        if isinstance(node, Root):
            return f'√<span style="border-top:1px solid">{self._node(node.radicand)}</span>'
        if isinstance(node, Nary):
            return html.escape(node.symbol) + self._node(node.body)
        if isinstance(node, (Matrix, Cases)):
            rows = "".join(
                "<tr>"
                + "".join(
                    f'<td style="padding:2px 8px">{self._node(cell)}</td>' for cell in row
                )
                + "</tr>"
                for row in node.rows
            )
            left, right = ("{", "") if isinstance(node, Cases) else (
                (node.delimiter[0], node.delimiter[1]) if node.delimiter else ("", "")
            )
            return (
                f"{html.escape(left)}"
                f'<table style="display:inline-table">{rows}</table>{html.escape(right)}'
            )
        raise TypeError(type(node).__name__)


class WordOMMLRenderer:
    """Recursively emit native Office Math from a safe formula AST."""

    def render(self, node: FormulaNode, display: bool = False) -> Any:
        root = OxmlElement("m:oMathPara") if display else OxmlElement("m:oMath")
        math = OxmlElement("m:oMath") if display else root
        if display:
            root.append(math)
        self._append(math, node)
        return root

    def _append(self, parent: Any, node: FormulaNode) -> None:
        if isinstance(node, (Identifier, Number, Operator, Relation, Text, GreekLetter)):
            self._run(parent, node.value)
        elif isinstance(node, Function):
            self._run(parent, node.name)
        elif isinstance(node, Sequence):
            for child in node.children:
                self._append(parent, child)
        elif isinstance(node, Group):
            self._append(parent, node.content)
        elif isinstance(node, Fraction):
            fraction = OxmlElement("m:f")
            numerator = OxmlElement("m:num")
            denominator = OxmlElement("m:den")
            self._append(numerator, node.numerator)
            self._append(denominator, node.denominator)
            fraction.extend((numerator, denominator))
            parent.append(fraction)
        elif isinstance(node, Root):
            radical = OxmlElement("m:rad")
            degree = OxmlElement("m:deg")
            content = OxmlElement("m:e")
            if node.degree:
                self._append(degree, node.degree)
            self._append(content, node.radicand)
            radical.extend((degree, content))
            parent.append(radical)
        elif isinstance(node, (Superscript, Subscript, SubSuperscript)):
            self._script(parent, node)
        elif isinstance(node, Nary):
            self._nary(parent, node.symbol, node.body, node.lower, node.upper)
        elif isinstance(node, Matrix):
            self._matrix(parent, node.rows)
        elif isinstance(node, Cases):
            delimiter = OxmlElement("m:d")
            props = OxmlElement("m:dPr")
            begin = OxmlElement("m:begChr")
            begin.set(qn("m:val"), "{")
            props.append(begin)
            delimiter.append(props)
            content = OxmlElement("m:e")
            self._matrix(content, node.rows)
            delimiter.append(content)
            parent.append(delimiter)
        else:
            raise TypeError(type(node).__name__)

    def _script(self, parent: Any, node: Superscript | Subscript | SubSuperscript) -> None:
        if isinstance(node.base, Nary):
            lower = node.subscript if isinstance(node, (Subscript, SubSuperscript)) else None
            upper = node.exponent if isinstance(node, (Superscript, SubSuperscript)) else None
            self._nary(parent, node.base.symbol, node.base.body, lower, upper)
            return
        tag = "m:sSubSup" if isinstance(node, SubSuperscript) else (
            "m:sSup" if isinstance(node, Superscript) else "m:sSub"
        )
        script = OxmlElement(tag)
        base = OxmlElement("m:e")
        self._append(base, node.base)
        script.append(base)
        if isinstance(node, (Subscript, SubSuperscript)):
            sub = OxmlElement("m:sub")
            self._append(sub, node.subscript)
            script.append(sub)
        if isinstance(node, (Superscript, SubSuperscript)):
            sup = OxmlElement("m:sup")
            self._append(sup, node.exponent)
            script.append(sup)
        parent.append(script)

    def _matrix(self, parent: Any, rows: list[list[FormulaNode]]) -> None:
        matrix = OxmlElement("m:m")
        for values in rows:
            row = OxmlElement("m:mr")
            for value in values:
                cell = OxmlElement("m:e")
                self._append(cell, value)
                row.append(cell)
            matrix.append(row)
        parent.append(matrix)

    def _nary(
        self,
        parent: Any,
        symbol: str,
        body: FormulaNode,
        lower: FormulaNode | None,
        upper: FormulaNode | None,
    ) -> None:
        node = OxmlElement("m:nary")
        props = OxmlElement("m:naryPr")
        char = OxmlElement("m:chr")
        char.set(qn("m:val"), symbol)
        props.append(char)
        node.append(props)
        sub = OxmlElement("m:sub")
        sup = OxmlElement("m:sup")
        content = OxmlElement("m:e")
        if lower:
            self._append(sub, lower)
        if upper:
            self._append(sup, upper)
        self._append(content, body)
        node.extend((sub, sup, content))
        parent.append(node)

    @staticmethod
    def _run(parent: Any, value: str) -> None:
        if not value:
            return
        run = OxmlElement("m:r")
        text = OxmlElement("m:t")
        text.set(qn("xml:space"), "preserve")
        text.text = value
        run.append(text)
        parent.append(run)
