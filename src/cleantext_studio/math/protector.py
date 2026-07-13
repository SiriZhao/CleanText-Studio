from __future__ import annotations

from dataclasses import dataclass

from cleantext_studio.models import MathBlockData, MathDisplayMode, MathFormat, MathOutputMode

from .delimiters import strip_formula_delimiters
from .detector import MathDetector
from .normalizer import MathNormalizer
from .parser import FormulaParseError, FormulaParser


@dataclass(slots=True)
class ProtectedMath:
    token: str
    data: MathBlockData


class MathProtector:
    """Replace math with inert tokens before Markdown and whitespace cleaners run."""

    def __init__(
        self, normalize: bool = True, output_mode: MathOutputMode = MathOutputMode.PRESERVE
    ) -> None:
        self.detector = MathDetector()
        self.normalizer = MathNormalizer()
        self.normalize = normalize
        self.output_mode = output_mode

    def protect_inline(self, text: str, offset: int = 0) -> tuple[str, list[ProtectedMath]]:
        regions = self.detector.detect_inline(text)
        protected: list[ProtectedMath] = []
        output: list[str] = []
        cursor = 0
        for index, region in enumerate(regions):
            token = f"CTSMATHINLINE{index}TOKEN"
            normalized = (
                self.normalizer.normalize(region.content) if self.normalize else region.content
            )
            delimited = strip_formula_delimiters(region.source)
            try:
                ast = FormulaParser().parse(delimited.expression_source)
            except FormulaParseError:
                ast = None
            data = MathBlockData(
                region.source,
                normalized,
                region.math_format,
                region.display_mode,
                region.equation_number,
                offset + region.start,
                offset + region.end,
                region.confidence,
                metadata={"ast": ast},
                raw_source=region.source,
                expression_source=delimited.expression_source,
                delimiter_type=delimited.delimiter_type,
                normalized_latex=normalized,
            )
            output.extend((text[cursor : region.start], token))
            cursor = region.end
            protected.append(ProtectedMath(token, data))
        output.append(text[cursor:])
        return "".join(output), protected

    @staticmethod
    def restore_inline(text: str, protected: list[ProtectedMath]) -> str:
        for item in protected:
            text = text.replace(item.token, item.data.source_text)
        return text

    def rendered_inline(self, data: MathBlockData) -> str:
        if self.output_mode == MathOutputMode.LATEX:
            return f"${self.normalizer.to_latex(data.normalized_text)}$"
        if self.output_mode == MathOutputMode.UNICODE:
            return self.normalizer.to_unicode(data.normalized_text)
        return data.source_text

    def restore(self, text: str, protected: list[ProtectedMath]) -> str:
        for item in protected:
            text = text.replace(item.token, self.rendered_inline(item.data))
        return text

    def display_data(
        self, source: str, content: str, start: int, end: int, equation_number: str | None = None
    ) -> MathBlockData:
        normalized = self.normalizer.normalize(content) if self.normalize else content.strip()
        delimited = strip_formula_delimiters(source)
        expression = content.strip()
        try:
            ast = FormulaParser().parse(expression)
        except FormulaParseError:
            ast = None
        return MathBlockData(
            source,
            normalized,
            MathFormat.LATEX,
            MathDisplayMode.BLOCK,
            equation_number,
            start,
            end,
            1.0,
            metadata={"ast": ast},
            raw_source=source,
            expression_source=expression,
            delimiter_type=delimited.delimiter_type,
            normalized_latex=normalized,
        )
