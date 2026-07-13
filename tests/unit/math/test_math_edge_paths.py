import pytest
from lxml import etree

from cleantext_studio.math import (
    MathDetector,
    MathNormalizer,
    PreviewFormulaRenderer,
    UnicodeFormulaRenderer,
    WordOMMLRenderer,
)
from cleantext_studio.math.ast import Cases, Identifier, Nary, Root, SubSuperscript
from cleantext_studio.math.parser import FormulaParseError, FormulaParser
from cleantext_studio.math.protector import MathProtector
from cleantext_studio.models import MathOutputMode


@pytest.mark.parametrize(
    "source, expected",
    [
        ("$199", []),
        (r"C:\\Users\\Test", []),
        (r"这里有 \( O \) 和 $x^2$", ["O", "x^2"]),
    ],
)
def test_inline_detector_handles_currency_paths_and_balanced_delimiters(source, expected) -> None:
    assert [region.content for region in MathDetector().detect_inline(source)] == expected


def test_detector_line_and_environment_paths() -> None:
    detector = MathDetector()
    assert detector.detect_line("y = ax + b") is not None
    assert detector.detect_line("value = a * b") is None
    assert detector.environment_start(r"\begin{align}") == "align"
    assert detector.environment_ended(r"\end{align}", "align")


def test_protector_restores_all_output_modes() -> None:
    protected, values = MathProtector().protect_inline(r"A \(x_1\) B")
    assert "CTSMATHINLINE0TOKEN" in protected
    assert MathProtector().restore_inline(protected, values) == r"A \(x_1\) B"
    latex = MathProtector(output_mode=MathOutputMode.LATEX)
    _, values = latex.protect_inline(r"$x^2$")
    assert latex.rendered_inline(values[0].data).startswith("$")
    unicode = MathProtector(output_mode=MathOutputMode.UNICODE)
    _, values = unicode.protect_inline(r"$x^2$")
    assert "x" in unicode.rendered_inline(values[0].data)


@pytest.mark.parametrize(
    "source",
    [
        r"\begin{aligned}a&=b\\c&=d\end{aligned}",
        r"\begin{bmatrix}1&2\\3&4\end{bmatrix}",
        r"\begin{cases}x,&x>0\\-x,&x<0\end{cases}",
    ],
)
def test_parser_supported_environments_render_safely(source: str) -> None:
    node = FormulaParser().parse(source)
    assert UnicodeFormulaRenderer().render(node)
    assert PreviewFormulaRenderer().render(node)


@pytest.mark.parametrize("source", ["", "{", r"\text{", r"\notreal", "x_"])
def test_parser_reports_invalid_input(source: str) -> None:
    with pytest.raises(FormulaParseError):
        FormulaParser().parse(source)


def test_math_normalizer_handles_latex_and_unicode() -> None:
    normalizer = MathNormalizer()
    assert normalizer.normalize(r"\frac { a } { b }") == r"\frac{a}{b}"
    assert "α" in normalizer.to_unicode(r"\alpha")


def test_word_renderer_covers_degree_cases_and_nary_scripts() -> None:
    renderer = WordOMMLRenderer()
    root = renderer.render(Root(Identifier("x"), Identifier("3")), display=True)
    assert "m:rad" in etree.tostring(root, encoding="unicode")
    cases = renderer.render(Cases([[Identifier("x"), Identifier("y")]]))
    assert "m:d" in etree.tostring(cases, encoding="unicode")
    nary = renderer.render(
        SubSuperscript(Nary("∑", Identifier("x")), Identifier("i"), Identifier("n"))
    )
    assert "m:nary" in etree.tostring(nary, encoding="unicode")


def test_preview_renderer_handles_function_nary_and_cases() -> None:
    renderer = PreviewFormulaRenderer()
    assert "font-style" in renderer.render(FormulaParser().parse(r"\log(x)"))
    assert "∑" in renderer.render(Nary("∑", Identifier("x")))
    assert "<table" in renderer.render(Cases([[Identifier("x")]]))
