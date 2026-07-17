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
    MathAccent,
    MathDelimiter,
    MathStyled,
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
        if isinstance(node, MathStyled):
            return self.render(node.content)
        if isinstance(node, MathAccent):
            marks = {"hat": "ˆ", "bar": "¯", "vec": "⃗", "dot": "˙", "tilde": "˜"}
            return f"{marks[node.kind]}({self.render(node.content)})"
        if isinstance(node, MathDelimiter):
            return f"{node.begin}{self.render(node.content)}{node.end}"
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
        if isinstance(node, MathStyled):
            styles = {
                "bold": "font-weight:bold",
                "italic": "font-style:italic",
                "roman": "font-style:normal",
                "script": "font-family:'Cambria Math',serif",
                "double-struck": "font-family:'Cambria Math',serif",
            }
            return f'<span style="{styles[node.style]}">{self._node(node.content)}</span>'
        if isinstance(node, MathAccent):
            marks = {"hat": "ˆ", "bar": "¯", "vec": "⃗", "dot": "˙", "tilde": "˜"}
            return f'<span style="text-decoration:overline">{html.escape(marks[node.kind])}{self._node(node.content)}</span>'
        if isinstance(node, MathDelimiter):
            return html.escape(node.begin) + self._node(node.content) + html.escape(node.end)
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
        elif isinstance(node, MathStyled):
            self._styled(parent, node)
        elif isinstance(node, MathAccent):
            self._accent(parent, node)
        elif isinstance(node, MathDelimiter):
            self._delimiter(parent, node)
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

    def _styled(self, parent: Any, node: MathStyled) -> None:
        # Office Math applies character styling on m:r.  Complex styled content
        # remains structurally native; leaf runs receive the requested style.
        if isinstance(node.content, Sequence):
            for child in node.content.children:
                self._styled(parent, MathStyled(node.style, child))
            return
        if isinstance(node.content, (Identifier, Number, Operator, Relation, Text, GreekLetter, Function)):
            value = node.content.name if isinstance(node.content, Function) else node.content.value
            self._run(parent, value, node.style)
            return
        self._append(parent, node.content)

    def _accent(self, parent: Any, node: MathAccent) -> None:
        accent = OxmlElement("m:acc")
        props = OxmlElement("m:accPr")
        char = OxmlElement("m:chr")
        char.set(qn("m:val"), {"hat": "ˆ", "bar": "¯", "vec": "⃗", "dot": "˙", "tilde": "˜"}[node.kind])
        props.append(char)
        content = OxmlElement("m:e")
        self._append(content, node.content)
        accent.extend((props, content))
        parent.append(accent)

    def _delimiter(self, parent: Any, node: MathDelimiter) -> None:
        delimiter = OxmlElement("m:d")
        props = OxmlElement("m:dPr")
        for tag, value in (("m:begChr", node.begin), ("m:endChr", node.end)):
            if value:
                char = OxmlElement(tag)
                char.set(qn("m:val"), value)
                props.append(char)
        delimiter.append(props)
        content = OxmlElement("m:e")
        self._append(content, node.content)
        delimiter.append(content)
        parent.append(delimiter)

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
    def _run(parent: Any, value: str, style: str | None = None) -> None:
        if not value:
            return
        run = OxmlElement("m:r")
        if style:
            props = OxmlElement("m:rPr")
            if style == "bold":
                element = OxmlElement("m:sty")
                element.set(qn("m:val"), "b")
                props.append(element)
            elif style == "italic":
                element = OxmlElement("m:sty")
                element.set(qn("m:val"), "i")
                props.append(element)
            elif style == "roman":
                element = OxmlElement("m:sty")
                element.set(qn("m:val"), "p")
                props.append(element)
            elif style in {"script", "double-struck"}:
                element = OxmlElement("m:scr")
                element.set(qn("m:val"), "script" if style == "script" else "double-struck")
                props.append(element)
            run.append(props)
        text = OxmlElement("m:t")
        text.set(qn("xml:space"), "preserve")
        text.text = value
        run.append(text)
        parent.append(run)
