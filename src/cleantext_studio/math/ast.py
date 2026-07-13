from __future__ import annotations

from dataclasses import dataclass, field


class FormulaNode:
    """Base type for the safe, non-executable formula AST."""


@dataclass(slots=True)
class Identifier(FormulaNode):
    value: str


@dataclass(slots=True)
class Number(FormulaNode):
    value: str


@dataclass(slots=True)
class Operator(FormulaNode):
    value: str


@dataclass(slots=True)
class Relation(FormulaNode):
    value: str


@dataclass(slots=True)
class Text(FormulaNode):
    value: str


@dataclass(slots=True)
class GreekLetter(FormulaNode):
    name: str
    value: str


@dataclass(slots=True)
class Sequence(FormulaNode):
    children: list[FormulaNode] = field(default_factory=list)


@dataclass(slots=True)
class Group(FormulaNode):
    content: FormulaNode


@dataclass(slots=True)
class Superscript(FormulaNode):
    base: FormulaNode
    exponent: FormulaNode


@dataclass(slots=True)
class Subscript(FormulaNode):
    base: FormulaNode
    subscript: FormulaNode


@dataclass(slots=True)
class SubSuperscript(FormulaNode):
    base: FormulaNode
    subscript: FormulaNode
    exponent: FormulaNode


@dataclass(slots=True)
class Fraction(FormulaNode):
    numerator: FormulaNode
    denominator: FormulaNode


@dataclass(slots=True)
class Root(FormulaNode):
    radicand: FormulaNode
    degree: FormulaNode | None = None


@dataclass(slots=True)
class Function(FormulaNode):
    name: str


@dataclass(slots=True)
class Nary(FormulaNode):
    symbol: str
    body: FormulaNode
    lower: FormulaNode | None = None
    upper: FormulaNode | None = None


@dataclass(slots=True)
class Matrix(FormulaNode):
    rows: list[list[FormulaNode]]
    delimiter: str = "()"


@dataclass(slots=True)
class Cases(FormulaNode):
    rows: list[list[FormulaNode]]
