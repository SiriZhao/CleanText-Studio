import pytest
from lxml import etree

from cleantext_studio.math import (
    FormulaParser,
    OMMLConverter,
    PreviewFormulaRenderer,
    UnicodeFormulaRenderer,
)
from cleantext_studio.math.ast import Cases, Matrix
from cleantext_studio.math.parser import FormulaParseError


def test_preview_renders_structure_without_latex_commands() -> None:
    ast = FormulaParser().parse(r"P(A\mid B)=\frac{P(AB)}{P(B)}")
    rendered = PreviewFormulaRenderer().render(ast)
    assert "border-bottom" in rendered
    assert r"\frac" not in rendered
    assert r"\mid" not in rendered


def test_supported_formula_subset_is_native_omml() -> None:
    cases = {
        r"S = k_B \ln \Omega": "m:sSub",
        r"mc^2": "m:sSup",
        r"\frac{a}{b}": "m:f",
        r"\sqrt{x}": "m:rad",
        r"\sum_{i=1}^{n}x_i": "m:nary",
        r"\int_0^1x^2\,dx": "m:nary",
        r"\begin{pmatrix}1 & 2 \\ 3 & 4\end{pmatrix}": "m:m",
    }
    for source, expected_tag in cases.items():
        result = OMMLConverter().convert(source, display=True)
        assert result.converted and result.element is not None, source
        xml = etree.tostring(result.element, encoding="unicode")
        assert expected_tag in xml
        assert r"\frac" not in xml
        assert r"\sqrt" not in xml


def test_outer_delimiters_never_reach_omml_or_fallback() -> None:
    for source in (r"\(E=mc^2\)", r"\[\frac{a}{b}\]"):
        result = OMMLConverter().convert(source, display=True)
        assert result.converted and result.element is not None
        serialized = etree.tostring(result.element, encoding="unicode")
        assert r"\(" not in serialized and r"\[" not in serialized
        assert r"\)" not in serialized and r"\]" not in serialized


@pytest.mark.parametrize(
    "source, expected",
    [
        (r"x_1^2", "_(1)^(2)"),
        (r"\sqrt{x}", "√(x)"),
        (r"\alpha+\beta", "α+β"),
        (r"\begin{pmatrix}1&2\\3&4\end{pmatrix}", "[1, 2; 3, 4]"),
        (r"\begin{cases}x^2&x\geq0\\-x&x<0\end{cases}", "{ "),
    ],
)
def test_unicode_fallback_preserves_formula_content(source: str, expected: str) -> None:
    rendered = UnicodeFormulaRenderer().render(FormulaParser().parse(source))
    assert expected in rendered


def test_preview_supports_root_scripts_matrix_and_cases() -> None:
    renderer = PreviewFormulaRenderer()
    assert "border-top" in renderer.render(FormulaParser().parse(r"\sqrt{x}"))
    assert "<sub>" in renderer.render(FormulaParser().parse("x_1"))
    assert "<sup>" in renderer.render(FormulaParser().parse("x^2"))
    assert "<table" in renderer.render(Matrix([[FormulaParser().parse("1")]]))
    assert "{" in renderer.render(Cases([[FormulaParser().parse("x")]]))


@pytest.mark.parametrize(
    "source",
    ["x_", "{x", r"\frac{x}", r"\text x", r"\unknown{x}", r"\begin{foo}x\end{foo}"],
)
def test_invalid_or_unsupported_formula_is_safely_rejected(source: str) -> None:
    with pytest.raises(FormulaParseError):
        FormulaParser().parse(source)
