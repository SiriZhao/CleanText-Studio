from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .ast import FormulaNode
from .delimiters import strip_formula_delimiters
from .parser import FormulaParseError, FormulaParser
from .renderers import UnicodeFormulaRenderer, WordOMMLRenderer


@dataclass(slots=True)
class OMMLConversionResult:
    element: Any | None
    converted: bool
    fallback_text: str
    warning: str | None = None
    ast: FormulaNode | None = None


class FormulaIntegrityChecker:
    """Reject OMML that loses any AST leaf value."""

    def validate(self, ast: FormulaNode, element: Any) -> bool:
        expected = "".join(UnicodeFormulaRenderer().render(ast).split())
        attribute_values = "".join(
            str(value) for child in element.iter() for value in child.attrib.values()
        )
        actual = "".join(("".join(element.itertext()) + attribute_values).split())
        # Structural punctuation differs, so require all meaningful identifiers/numbers/symbols.
        tokens = [
            char
            for char in expected
            if char.isalnum() or char in "αβγδελμπσξωΩΔ∞∑∫≤≥≠≈∝×÷±"
        ]
        return all(token in actual for token in tokens)


class OMMLConverter:
    """Parse formula source and recursively generate native editable Office Math."""

    def __init__(self) -> None:
        self.parser = FormulaParser()
        self.renderer = WordOMMLRenderer()
        self.integrity = FormulaIntegrityChecker()
        self.fallback = UnicodeFormulaRenderer()

    def convert(self, expression: str, display: bool = False) -> OMMLConversionResult:
        delimited = strip_formula_delimiters(expression)
        source = delimited.expression_source
        if len(source) > 20000:
            return OMMLConversionResult(None, False, source, "公式超过安全长度限制")
        try:
            ast = self.parser.parse(source)
            element = self.renderer.render(ast, display or delimited.display)
            if not self.integrity.validate(ast, element):
                return OMMLConversionResult(None, False, self.fallback.render(ast), "公式完整性校验失败", ast)
            return OMMLConversionResult(element, True, self.fallback.render(ast), ast=ast)
        except (FormulaParseError, ValueError, TypeError, RecursionError) as exc:
            return OMMLConversionResult(None, False, source, str(exc))
