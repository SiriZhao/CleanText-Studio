from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import CleanOptions


def test_deep_cleaning_is_idempotent() -> None:
    options = CleanOptions(clean_instructional_labels=True)
    source = "### 标题\n\n---\n\n填写：\n\n账号\n\n**正文**"
    once = clean_text(source, options).text
    assert clean_text(once, options).text == once
