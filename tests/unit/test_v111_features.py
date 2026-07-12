import pytest

from cleantext_studio.cleaners import clean_text
from cleantext_studio.llm.presets import get_preset
from cleantext_studio.models import CleanOptions, ParagraphBreakMode


@pytest.mark.parametrize(
    ("provider", "url"),
    [
        ("openai", "https://api.openai.com/v1"),
        ("deepseek", "https://api.deepseek.com"),
        ("anthropic", "https://api.anthropic.com"),
        ("local", "http://localhost:11434/v1"),
    ],
)
def test_provider_default_urls(provider: str, url: str) -> None:
    assert get_preset(provider).default_base_url == url


def test_provider_models_and_key_requirements() -> None:
    assert get_preset("deepseek").default_models
    assert get_preset("deepseek").api_key_required
    assert not get_preset("local").api_key_required


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


def test_paragraph_modes_protect_heading_list_code_table() -> None:
    source = "## 标题\n\n正文。\n\n- 列表\n\n```\nline1\nline2\n```\n\n| A | B |"
    result = clean_text(source, CleanOptions(paragraph_break_mode=ParagraphBreakMode.COMPACT)).text
    assert result.startswith("标题\n") and "• 列表" in result
    assert "line1\nline2" in result and "| A | B |" in result


@pytest.mark.parametrize(
    "phrase",
    [
        "当然可以，以下是整理后的内容：",
        "好的，下面为你整理：",
        "✅ 当然可以！以下为优化后的版本：",
        "根据你的要求，我整理如下：",
    ],
)
def test_start_boilerplate_removed(phrase: str) -> None:
    result = clean_text(f"{phrase}\n\n正文内容。", CleanOptions(remove_template_phrases=True))
    assert result.text == "正文内容。"
    assert any("聊天套话" in change for change in result.changes)


@pytest.mark.parametrize(
    "phrase",
    [
        "希望以上内容对你有所帮助。",
        "如有需要，我可以继续修改。",
        "如果还有其他问题，欢迎继续提问。",
        "以上就是完整内容。",
    ],
)
def test_end_boilerplate_removed(phrase: str) -> None:
    assert (
        clean_text(f"正文内容。\n\n{phrase}", CleanOptions(remove_template_phrases=True)).text
        == "正文内容。"
    )


def test_inline_start_boilerplate_keeps_real_content() -> None:
    source = "当然可以，以下是整理后的内容：人工智能正在快速发展。"
    assert (
        clean_text(source, CleanOptions(remove_template_phrases=True)).text
        == "人工智能正在快速发展。"
    )


def test_middle_phrase_is_protected() -> None:
    source = "第一段。\n\n希望以上内容对你有所帮助。\n\n最后一段。"
    assert "希望以上内容" in clean_text(source, CleanOptions(remove_template_phrases=True)).text


def test_disabled_boilerplate_cleaner_preserves_text() -> None:
    source = "当然可以，以下是整理后的内容：\n\n正文。"
    assert "当然可以" in clean_text(source).text
