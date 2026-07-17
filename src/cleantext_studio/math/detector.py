from __future__ import annotations

import re
from dataclasses import dataclass

from cleantext_studio.models import MathDisplayMode, MathFormat

_INLINE = re.compile(r"(?<!\\)\$(?!\s*\d+(?:[.,]\d+)?(?:\s|$))(.+?)(?<!\\)\$")
_PAREN = re.compile(r"\\\((.+?)\\\)")
_COMMAND = re.compile(r"\\(?:[A-Za-z]+|[,;:!])")
_EQUALITY = re.compile(r"(?<![=!<>])=(?!=)")
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
        regions = self._deduplicate(regions)
        regions.extend(self._detect_bare_inline(text, regions))
        return self._deduplicate(regions)

    def _detect_bare_inline(self, text: str, bounded: list[MathRegion]) -> list[MathRegion]:
        """Find un-delimited LaTeX/equations embedded in prose.

        This intentionally requires a mathematical command or relation and does
        not recognise arbitrary backslash text.  Explicit regions are handled
        first so Markdown code, URLs and Windows paths cannot be split into
        candidate runs.
        """
        protected = [(item.start, item.end) for item in bounded]
        triggers = sorted(
            {match.start() for match in _COMMAND.finditer(text)}
            | {match.start() for match in _EQUALITY.finditer(text)}
        )
        regions: list[MathRegion] = []
        for trigger in triggers:
            if any(start <= trigger < end for start, end in protected):
                continue
            start = self._candidate_start(text, trigger)
            end = self._candidate_end(text, trigger)
            source = text[start:end].strip()
            if not source or self._looks_like_code(source) or self._looks_like_path_or_url(source):
                continue
            if not self._is_bare_formula(source):
                continue
            leading = len(text[start:end]) - len(text[start:end].lstrip())
            trailing = len(text[start:end]) - len(text[start:end].rstrip())
            regions.append(
                MathRegion(
                    start + leading,
                    end - trailing,
                    source,
                    source,
                    MathFormat.LATEX,
                    MathDisplayMode.INLINE,
                    0.88,
                )
            )
        return self._deduplicate(regions)

    @staticmethod
    def _candidate_start(text: str, trigger: int) -> int:
        # A preceding label (Chinese or English) stays text.  Colons are the
        # strongest prose/math boundary; otherwise start after the last space.
        prefix = text[:trigger]
        separators = [prefix.rfind(mark) for mark in ("\n", "\r", "：", ":", "；", ";")]
        start = max(separators) + 1
        if start == 0:
            start = max(prefix.rfind(" ") + 1, prefix.rfind("\t") + 1)
        return start

    @staticmethod
    def _candidate_end(text: str, trigger: int) -> int:
        depth = 0
        for index in range(trigger, len(text)):
            char = text[index]
            if char in "{([":
                depth += 1
            elif char in "})]" and depth:
                depth -= 1
            if depth == 0 and char in "\r\n。；":
                return index
            if depth == 0 and "\u4e00" <= char <= "\u9fff":
                return index
            # A Chinese comma normally starts prose; commas inside formulae are
            # kept while parenthesised/braced (for example Attention(Q,K,V)).
            if depth == 0 and char == "，":
                return index
        return len(text)

    @staticmethod
    def _looks_like_path_or_url(text: str) -> bool:
        return bool(re.search(r"(?:https?://|\b[A-Za-z]:\\|\\\\[A-Za-z0-9_.-]+\\)", text))

    def _is_bare_formula(self, text: str) -> bool:
        command = _COMMAND.search(text)
        relation = _EQUALITY.search(text)
        if not command and not relation:
            return False
        if command and re.fullmatch(r"\\[A-Za-z]+", text):
            return False
        return self._math_score(text) >= 0.6 or (command is not None and relation is not None)

    @staticmethod
    def _deduplicate(regions: list[MathRegion]) -> list[MathRegion]:
        unique: list[MathRegion] = []
        for region in sorted(regions, key=lambda item: (item.start, -(item.end - item.start))):
            if any(item.start <= region.start and region.end <= item.end for item in unique):
                continue
            unique = [item for item in unique if not (region.start <= item.start and item.end <= region.end)]
            unique.append(region)
        return sorted(unique, key=lambda item: item.start)

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
            if re.search(
                r"\\(?:frac|sqrt|sum|prod|int|alpha|beta|gamma|pi|sigma|theta|eta|tau|"
                r"nabla|hbar|mathbf|mathcal|text|hat|left|right|top|cap|sim|ge|le|mid)\b",
                text,
            )
            else 0
        )
        score += 0.25 if re.search(r"[A-Za-zα-ω]\s*(?:[=+\-*/^_]|\\)", text) else 0
        return min(1.0, score)
