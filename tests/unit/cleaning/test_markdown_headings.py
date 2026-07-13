import pytest

from cleantext_studio.cleaners import clean_text


@pytest.mark.parametrize(
    "source", ["#标题", "## 标题", "＃＃ 标题", "####\t**标题**", "**#### 标题**"]
)
def test_heading_markers_removed_and_level_retained(source: str) -> None:
    result = clean_text(source)
    assert result.text == "标题"
    assert result.blocks[0].heading_level is not None


def test_legal_hash_content_is_retained() -> None:
    source = "C#\n#1\n话题#农业\n颜色值 #FFFFFF"
    assert clean_text(source).text.replace("\n\n", "\n") == source
