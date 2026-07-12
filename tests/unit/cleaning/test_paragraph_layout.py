import pytest

from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import CleanOptions, ParagraphBreakMode


@pytest.mark.parametrize("mode", list(ParagraphBreakMode))
def test_layout_modes_bound_blank_lines_and_keep_heading(mode: ParagraphBreakMode) -> None:
    result = clean_text("# 标题\n\n\n\n第一段。\n\n第二段。", CleanOptions(paragraph_break_mode=mode))
    assert result.text.startswith("标题\n")
    assert "\n\n\n" not in result.text
