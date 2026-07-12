from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import CleanOptions


def test_statistics_match_changes() -> None:
    result = clean_text("## 标题\n---\n填写：\n账号", CleanOptions(clean_instructional_labels=True))
    assert result.stats.removed_separators == 1
    assert result.stats.removed_ai_patterns == 1
    assert any(change.rule_id == "horizontal_rule" for change in result.change_records)
    assert result.stats.residual_count == len(result.residuals)
