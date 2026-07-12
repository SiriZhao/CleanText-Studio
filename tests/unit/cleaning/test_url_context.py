from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import CleanOptions, IndependentURLMode


def test_default_preserves_and_explicit_mode_deletes_tutorial_url() -> None:
    source = "打开：\n\nhttps://example.com"
    keep = clean_text(source, CleanOptions(clean_instructional_labels=True))
    assert "https://example.com" in keep.text
    remove = clean_text(
        source,
        CleanOptions(
            clean_instructional_labels=True,
            independent_url_mode=IndependentURLMode.DELETE_TUTORIAL,
        ),
    )
    assert "https://example.com" not in remove.text


def test_merge_mode_attaches_standalone_url_to_previous_paragraph() -> None:
    result = clean_text(
        "项目主页\n\nhttps://example.com",
        CleanOptions(independent_url_mode=IndependentURLMode.MERGE_PREVIOUS),
    )
    assert result.text == "项目主页 https://example.com"
