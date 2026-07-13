from cleantext_studio.math import MathDetector
from cleantext_studio.models import MathFormat


def test_inline_delimiters_and_currency_guard() -> None:
    detector = MathDetector()
    assert detector.detect_inline("能量为 $E = mc^2$。")
    assert detector.detect_inline(r"满足 \(x_1 + y_1 = 2\)。")
    assert detector.detect_inline("价格为 $199。") == []


def test_unicode_and_plain_equations() -> None:
    detector = MathDetector()
    assert detector.detect_line("α + β = γ").math_format == MathFormat.UNICODE_MATH  # type: ignore[union-attr]
    assert detector.detect_line("f(x) = x² + 2x + 1") is not None
    assert detector.detect_line("value = a * b") is None


def test_false_positives() -> None:
    detector = MathDetector()
    for value in (r"C:\Users\name", r"\d+\w+", "v1.3.0", "2026-07-13", "https://x.test?a=1"):
        assert detector.detect_line(value) is None


def test_environment_helpers() -> None:
    detector = MathDetector()
    assert detector.environment_start(r"\begin{align}") == "align"
    assert detector.environment_ended(r"\end{align}", "align")
