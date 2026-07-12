import pytest

from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import CleanOptions, ParagraphBreakMode


@pytest.mark.parametrize("mode", list(ParagraphBreakMode))
def test_paragraph_modes_are_idempotent(mode: ParagraphBreakMode) -> None:
    source = "第一段内容。\n\n第二段内容。\n\n第三段内容。"
    once = clean_text(source, CleanOptions(paragraph_break_mode=mode)).text
    assert clean_text(once, CleanOptions(paragraph_break_mode=mode)).text == once


def test_compact_and_preserve_paragraph_modes() -> None:
    source = "第一段内容。\n\n第二段内容。\n\n第三段内容。"
    compact = clean_text(source, CleanOptions(paragraph_break_mode=ParagraphBreakMode.COMPACT)).text
    preserve = clean_text(
        source, CleanOptions(paragraph_break_mode=ParagraphBreakMode.PRESERVE_ALL)
    ).text
    assert compact == "第一段内容。第二段内容。第三段内容。"
    assert preserve == source


def test_paragraph_modes_protect_structures() -> None:
    source = "## 标题\n\n正文。\n\n- 列表\n\n```\nline1\nline2\n```\n\n| A | B |"
    result = clean_text(source, CleanOptions(paragraph_break_mode=ParagraphBreakMode.COMPACT)).text
    assert result.startswith("标题\n") and "• 列表" in result
    assert "line1\nline2" in result and "| A | B |" in result
