from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import CleanOptions, LinkMode


def test_inline_markers_and_images() -> None:
    result = clean_text("***粗斜体*** **粗体** *斜体* `代码` ![说明](x.png)")
    assert result.text == "粗斜体 粗体 斜体 代码 [图片：说明]"


def test_link_modes() -> None:
    source = "[官网](https://example.com)"
    assert clean_text(source).text == "官网"
    assert "https://example.com" in clean_text(
        source, CleanOptions(link_mode=LinkMode.TEXT_AND_URL)
    ).text
    assert clean_text(source, CleanOptions(link_mode=LinkMode.KEEP_MARKDOWN)).text == source
