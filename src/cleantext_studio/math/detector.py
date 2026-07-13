from __future__ import annotations

import re
from dataclasses import dataclass

from cleantext_studio.models import MathDisplayMode, MathFormat

_INLINE = re.compile(r"(?<!\\)\$(?!\s*\d+(?:[.,]\d+)?(?:\s|$))(.+?)(?<!\\)\$")
_PAREN = re.compile(r"\\\((.+?)\\\)")
_UNICODE_MATH = re.compile(r"[²³⁰¹⁴⁵⁶⁷⁸⁹₀-₉α-ωΑ-Ω∑∫√∞≤≥≠≈×÷±]")
_PLAIN = re.compile(r"^\s*[A-Za-z](?:\([^)]+\))?\s*=\s*[^=]{1,180}$")
_ENV_START = re.compile(r"\\begin\{(equation\*?|align\*?|aligned|gather\*?|cases|[pb]?matrix)\}")
_ENV_END = re.compile(r"\\end\{([^}]+)\}")
_NUMBER = re.compile(r"(?:\s{2,}|\u3000+)([（(]\d+[)）])\s*$")


@dataclass(slots=True, frozen=True)
class MathRegion:
    start: int
    end: int
    source: str
    content: str
    math_format: MathFormat
    display_mode: MathDisplayMode
    confidence: float
    equation_number: str | None = None
    warning: str | None = None


class MathDetector:
    """Detect bounded math without treating currency, paths, code or versions as formulae."""

    def detect_inline(self, text: str) -> list[MathRegion]:
        regions: list[MathRegion] = []
        for pattern in (_INLINE, _PAREN):
            for match in pattern.finditer(text):
                content = match.group(1).strip()
                # Explicit, balanced LaTeX delimiters are intentional even for a
                # single variable such as \(O\) or \(\lambda\).
                if content and (pattern is _PAREN or self._math_score(content) >= 0.55):
                    regions.append(
                        MathRegion(
                            match.start(),
                            match.end(),
                            match.group(),
                            content,
                            MathFormat.LATEX,
                            MathDisplayMode.INLINE,
                            0.98,
                        )
                    )
        return sorted(regions, key=lambda item: item.start)

    def detect_line(self, text: str) -> MathRegion | None:
        stripped = text.strip()
        number_match = _NUMBER.search(stripped)
        number = number_match.group(1) if number_match else None
        candidate = stripped[: number_match.start()].rstrip() if number_match else stripped
        if candidate.startswith("$$") and candidate.endswith("$$") and len(candidate) > 4:
            return MathRegion(
                0,
                len(text),
                text,
                candidate[2:-2].strip(),
                MathFormat.LATEX,
                MathDisplayMode.BLOCK,
                1.0,
                number,
            )
        if candidate.startswith(r"\[") and candidate.endswith(r"\]"):
            return MathRegion(
                0,
                len(text),
                text,
                candidate[2:-2].strip(),
                MathFormat.LATEX,
                MathDisplayMode.BLOCK,
                1.0,
                number,
            )
        if _UNICODE_MATH.search(candidate) and (
            "=" in candidate or self._math_score(candidate) >= 0.7
        ):
            return MathRegion(
                0,
                len(text),
                text,
                candidate,
                MathFormat.UNICODE_MATH,
                MathDisplayMode.BLOCK,
                0.86,
                number,
            )
        if _PLAIN.match(candidate) and not self._looks_like_code(candidate):
            return MathRegion(
                0,
                len(text),
                text,
                candidate,
                MathFormat.PLAIN_EQUATION,
                MathDisplayMode.BLOCK,
                0.72,
                number,
            )
        return None

    @staticmethod
    def environment_start(text: str) -> str | None:
        match = _ENV_START.search(text)
        return match.group(1) if match else None

    @staticmethod
    def environment_ended(text: str, environment: str) -> bool:
        return any(match.group(1) == environment for match in _ENV_END.finditer(text))

    @staticmethod
    def _looks_like_code(text: str) -> bool:
        return any(token in text for token in (";", "==", "=>", "//", '"', "'")) or " * " in text

    @staticmethod
    def _math_score(text: str) -> float:
        if re.search(r"(?:https?://|[A-Z]:\\|\b(?:SELECT|echo|const|var)\b)", text, re.I):
            return 0.0
        score = 0.0
        score += 0.4 if re.search(r"[=<>+*/^_]", text) else 0
        score += (
            0.35
            if re.search(r"\\(?:frac|sqrt|sum|int|alpha|beta|gamma|pi|infty|ge|le|mid)\b", text)
            else 0
        )
        score += 0.25 if re.search(r"[A-Za-zα-ω]\s*(?:[=+\-*/^_]|\\)", text) else 0
        return min(1.0, score)
