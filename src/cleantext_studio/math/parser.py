from __future__ import annotations

import re

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

GREEK = {
    "alpha": "\u03b1",
    "beta": "\u03b2",
    "gamma": "\u03b3",
    "delta": "\u03b4",
    "Delta": "\u0394",
    "epsilon": "\u03b5",
    "varepsilon": "\u03f5",
    "eta": "\u03b7",
    "lambda": "\u03bb",
    "mu": "\u03bc",
    "pi": "\u03c0",
    "sigma": "\u03c3",
    "Sigma": "\u03a3",
    "xi": "\u03be",
    "omega": "\u03c9",
    "Omega": "\u03a9",
    "theta": "\u03b8",
    "tau": "\u03c4",
    "nabla": "\u2207",
    "hbar": "\u210f",
    "infty": "\u221e",
}
OPERATORS = {
    "times": "\u00d7",
    "div": "\u00f7",
    "cdot": "\u00b7",
    "pm": "\u00b1",
    "mid": "|",
    "cap": "\u2229",
    "cup": "\u222a",
    "sim": "\u223c",
    "top": "\u22a4",
    "quad": " ",
    "qquad": "  ",
    ",": " ",
}
RELATIONS = {
    "le": "\u2264",
    "leq": "\u2264",
    "ge": "\u2265",
    "geq": "\u2265",
    "ne": "\u2260",
    "neq": "\u2260",
    "approx": "\u2248",
    "propto": "\u221d",
}
FUNCTIONS = {"ln", "log", "exp", "sin", "cos", "tan", "lim", "max", "min"}
FUNCTIONS.update({"softmax"})
STYLES = {
    "mathbf": "bold",
    "boldsymbol": "bold",
    "mathcal": "script",
    "mathrm": "roman",
    "mathit": "italic",
    "mathbb": "double-struck",
}
ACCENTS = {"hat": "hat", "bar": "bar", "vec": "vec", "dot": "dot", "tilde": "tilde"}
DELIMITER_COMMANDS = {
    ".": "",
    "lbrace": "{",
    "rbrace": "}",
    "langle": "\u27e8",
    "rangle": "\u27e9",
    "vert": "|",
}
ENVIRONMENT = re.compile(r"^\\begin\{([^}]+)\}([\s\S]*)\\end\{\1\}$")


class FormulaParseError(ValueError):
    pass


class FormulaParser:
    """Parse a bounded, non-executable LaTeX subset into a safe AST."""

    def parse(self, source: str) -> FormulaNode:
        source = source.strip()
        if not source:
            raise FormulaParseError("formula is empty")
        if len(source) > 20_000:
            raise FormulaParseError("formula exceeds the safe length limit")
        environment = ENVIRONMENT.fullmatch(source)
        if environment:
            return self._environment(environment.group(1), environment.group(2))
        self.source = source
        self.position = 0
        node = self._sequence()
        if self.position != len(self.source):
            raise FormulaParseError(f"unexpected formula input at {self.position}")
        return node

    def _sequence(self, stop: str | None = None, stop_command: str | None = None) -> FormulaNode:
        children: list[FormulaNode] = []
        while self.position < len(self.source):
            char = self.source[self.position]
            if stop and char == stop:
                break
            if stop_command and self.source.startswith(f"\\{stop_command}", self.position):
                break
            if char.isspace():
                self.position += 1
                continue
            atom = self._atom()
            subscript: FormulaNode | None = None
            exponent: FormulaNode | None = None
            while self.position < len(self.source) and self.source[self.position] in "_^":
                marker = self.source[self.position]
                self.position += 1
                script = self._script()
                if marker == "_":
                    subscript = script
                else:
                    exponent = script
            if subscript and exponent:
                atom = SubSuperscript(atom, subscript, exponent)
            elif subscript:
                atom = Subscript(atom, subscript)
            elif exponent:
                atom = Superscript(atom, exponent)
            children.append(atom)
        return children[0] if len(children) == 1 else Sequence(children)

    def _script(self) -> FormulaNode:
        if self.position >= len(self.source):
            raise FormulaParseError("missing script value")
        if self.source[self.position] == "{":
            return self._group()
        return self._atom()

    def _group(self) -> FormulaNode:
        self.position += 1
        content = self._sequence("}")
        if self.position >= len(self.source) or self.source[self.position] != "}":
            raise FormulaParseError("unclosed formula group")
        self.position += 1
        return Group(content)

    def _required_group(self) -> FormulaNode:
        self._skip_spaces()
        if self.position >= len(self.source) or self.source[self.position] != "{":
            raise FormulaParseError("command requires a group")
        return self._group()

    def _atom(self) -> FormulaNode:
        char = self.source[self.position]
        if char == "{":
            return self._group()
        if char == "\\":
            return self._command()
        number = re.match(r"\d+(?:\.\d+)?|\.\d+", self.source[self.position :])
        if number:
            self.position += len(number.group())
            return Number(number.group())
        if char.isalpha():
            end = self.position + 1
            while end < len(self.source) and self.source[end].isalpha():
                end += 1
            value = self.source[self.position : end]
            self.position = end
            return Identifier(value)
        if char in {"\u2211", "\u222b", "\u221e"}:
            self.position += 1
            return Identifier(char)
        self.position += 1
        if char in "=<>\u2264\u2265\u2260\u2248\u221d":
            return Relation(char)
        return Operator(char)

    def _command(self) -> FormulaNode:
        self.position += 1
        if self.position < len(self.source) and not self.source[self.position].isalpha():
            value = self.source[self.position]
            self.position += 1
            return Operator(OPERATORS.get(value, value))
        match = re.match(r"[A-Za-z]+", self.source[self.position :])
        if not match:
            raise FormulaParseError("invalid command")
        name = match.group()
        self.position += len(name)
        if name == "frac":
            return Fraction(self._required_group(), self._required_group())
        if name == "sqrt":
            degree = None
            self._skip_spaces()
            if self.position < len(self.source) and self.source[self.position] == "[":
                self.position += 1
                degree = self._sequence("]")
                if self.position >= len(self.source) or self.source[self.position] != "]":
                    raise FormulaParseError("unclosed root degree")
                self.position += 1
            return Root(self._required_group(), degree)
        if name in {"text", "operatorname"}:
            return Text(self._raw_group())
        if name in STYLES:
            return MathStyled(STYLES[name], self._required_group())
        if name in ACCENTS:
            return MathAccent(ACCENTS[name], self._required_group())
        if name in GREEK:
            return GreekLetter(name, GREEK[name])
        if name in OPERATORS:
            return Operator(OPERATORS[name])
        if name in RELATIONS:
            return Relation(RELATIONS[name])
        if name in FUNCTIONS:
            return Function(name)
        if name in {"sum", "int", "prod", "lim"}:
            symbol = {"sum": "\u2211", "int": "\u222b", "prod": "\u220f", "lim": "lim"}[name]
            return Nary(symbol, Sequence([]))
        if name == "left":
            begin = self._delimiter()
            content = self._sequence(stop_command="right")
            if not self.source.startswith("\\right", self.position):
                raise FormulaParseError("unclosed \\left delimiter")
            self.position += len("\\right")
            end = self._delimiter()
            return MathDelimiter(begin, content, end)
        if name == "right":
            raise FormulaParseError("unpaired \\right delimiter")
        raise FormulaParseError(f"unsupported command: {name}")

    def _delimiter(self) -> str:
        self._skip_spaces()
        if self.position >= len(self.source):
            raise FormulaParseError("missing delimiter")
        if self.source[self.position] != "\\":
            value = self.source[self.position]
            self.position += 1
            return value
        self.position += 1
        match = re.match(r"[A-Za-z]+", self.source[self.position :])
        if not match:
            value = self.source[self.position]
            self.position += 1
            return value
        name = match.group()
        self.position += len(name)
        return DELIMITER_COMMANDS.get(name, name)

    def _raw_group(self) -> str:
        self._skip_spaces()
        if self.position >= len(self.source) or self.source[self.position] != "{":
            raise FormulaParseError("text requires a group")
        start = self.position + 1
        depth = 1
        index = start
        while index < len(self.source) and depth:
            if self.source[index] == "{":
                depth += 1
            elif self.source[index] == "}":
                depth -= 1
            index += 1
        if depth:
            raise FormulaParseError("unclosed text group")
        self.position = index
        return self.source[start : index - 1]

    def _environment(self, name: str, body: str) -> FormulaNode:
        if name in {"equation", "equation*", "align", "align*", "aligned", "gather", "gather*"}:
            return self.parse(body.replace("&", ""))
        if name in {"matrix", "pmatrix", "bmatrix"}:
            delimiter = {"matrix": "", "pmatrix": "()", "bmatrix": "[]"}[name]
            return Matrix(self._rows(body), delimiter)
        if name == "cases":
            return Cases(self._rows(body))
        raise FormulaParseError(f"unsupported environment: {name}")

    def _rows(self, body: str) -> list[list[FormulaNode]]:
        return [
            [FormulaParser().parse(cell.strip()) for cell in row.split("&")]
            for row in re.split(r"\\\\", body.strip())
            if row.strip()
        ]

    def _skip_spaces(self) -> None:
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1
