from cleantext_studio.math import MathNormalizer


def test_conservative_spacing() -> None:
    normalize = MathNormalizer().normalize
    assert normalize("  x ^ 2+y _ 1  ") == "x^2 + y_1"
    assert normalize(r"\frac { a } { b }") == r"\frac{a}{b}"


def test_idempotent() -> None:
    normalizer = MathNormalizer()
    once = normalizer.normalize(r"x ^ 2 + \frac {a}{b}")
    assert normalizer.normalize(once) == once


def test_unicode_latex_conversion_modes() -> None:
    normalizer = MathNormalizer()
    latex = normalizer.to_latex("α × β ≤ ∞")
    assert r"\alpha" in latex and r"\times" in latex and r"\le" in latex
    unicode = normalizer.to_unicode(r"\alpha + x^2 \ge \beta")
    assert "α" in unicode and "²" in unicode and "≥" in unicode
