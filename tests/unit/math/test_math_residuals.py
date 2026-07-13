from cleantext_studio.math import detect_math_warnings


def test_unclosed_delimiters_and_currency() -> None:
    assert any(w.warning_type == "unclosed_inline_dollar" for w in detect_math_warnings("$x+1"))
    assert detect_math_warnings("价格 $199") == []
    assert any(w.warning_type == "unbalanced_braces" for w in detect_math_warnings(r"\frac{a{b}"))
    assert any(
        w.warning_type == "unbalanced_environment"
        for w in detect_math_warnings(r"\begin{align}x=1")
    )
    assert any(w.warning_type == "incomplete_fraction" for w in detect_math_warnings(r"\frac{a}"))
