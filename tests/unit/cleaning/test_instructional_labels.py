from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import CleanOptions


def test_labels_are_opt_in_and_body_is_protected() -> None:
    source = "填写：\n\n账号\n\n点击按钮可以开始上传。"
    assert "填写" in clean_text(source).text
    cleaned = clean_text(source, CleanOptions(clean_instructional_labels=True))
    assert "填写" not in cleaned.text
    assert "账号" in cleaned.text and "点击按钮可以开始上传。" in cleaned.text
