import pytest

from cleantext_studio.cleaners import clean_text


@pytest.mark.parametrize("rule", ["---", "****", "___", "- - -", "* * *", "— — —", "———", "───"])
def test_horizontal_rule_is_removed(rule: str) -> None:
    assert clean_text(f"前文\n{rule}\n后文").stats.removed_separators == 1


@pytest.mark.parametrize("text", ["2025-2026", "A-B", "-3", "x - y", "a---b", "--help"])
def test_non_rules_are_retained(text: str) -> None:
    assert text in clean_text(text).text
