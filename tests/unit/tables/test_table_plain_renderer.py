from cleantext_studio.cleaners import clean_text


def test_text_mode_retains_normalized_markdown_table() -> None:
    result = clean_text("|模块|功能|\n|-|-|\n|识别|诊断|")
    assert "|模块|功能|" in result.text and "|识别|诊断|" in result.text
