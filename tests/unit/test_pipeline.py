import pytest

from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import CleanOptions


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("## 标题", "标题"),
        ("**粗体** 和 *斜体*", "粗体 和 斜体"),
        ("[链接](https://example.com)", "链接"),
        ("---\n正文", "正文"),
        ("✅ 内容", "内容"),
        ("◆ 内容", "内容"),
        (
            "人工智能正在快速发展，\n并逐渐应用于教育、\n医疗领域。",
            "人工智能正在快速发展，并逐渐应用于教育、医疗领域。",
        ),
        (
            "Artificial intelligence is changing\nthe way students learn.",
            "Artificial intelligence is changing the way students learn.",
        ),
        ("一、标题\n这是正文。", "一、标题\n这是正文。"),
        ("1. A\n2. B", "1. A\n2. B"),
        ("```python\nprint('x')\n```", "print('x')"),
        ("| A | B |\n|---|---|", "| A | B |\n|---|---|"),
        ("ＡＢＣ", "ABC"),
        ("a   b  ", "a b"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_clean(source: str, expected: str) -> None:
    assert clean_text(source).text == expected


def test_template_phrase_is_opt_in() -> None:
    source = "正文。\n\n希望以上内容对你有所帮助。"
    assert "希望" in clean_text(source).text
    assert clean_text(source, CleanOptions(remove_template_phrases=True)).text == "正文。"


def test_idempotent() -> None:
    once = clean_text("## 标题\n\n✅ 文本，\n继续。").text
    assert clean_text(once).text == once
