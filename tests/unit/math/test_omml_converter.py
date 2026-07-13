from lxml import etree

from cleantext_studio.math import OMMLConverter


def xml(expression: str) -> str:
    result = OMMLConverter().convert(expression, display=True)
    assert result.converted and result.element is not None
    return etree.tostring(result.element).decode()


def test_fraction_superscript_and_matrix() -> None:
    assert "m:f" in xml(r"\frac{a}{b}")
    assert "m:sSup" in xml("x^2")
    assert "m:m" in xml(r"\begin{pmatrix}1 &amp; 2 \\ 3 &amp; 4\end{pmatrix}".replace("&amp;", "&"))


def test_complexity_falls_back() -> None:
    result = OMMLConverter().convert("x" * 20001)
    assert not result.converted and result.fallback_text
    unknown = OMMLConverter().convert(r"\custommacro{x}")
    assert not unknown.converted and unknown.warning


def test_radical_subscript_greek_and_delimiters() -> None:
    assert "m:rad" in xml(r"\sqrt{x}")
    assert "m:sSub" in xml("x_1")
    assert "&#945;" in xml(r"\[\alpha + \beta\]")
