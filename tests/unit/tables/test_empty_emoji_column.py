from cleantext_studio.cleaners.tables import TableWidthPlanner, parse_table


def test_empty_emoji_column_is_removed_after_cell_cleanup() -> None:
    data = parse_table(
        [
            "| 类别 | 描述 | Emoji |",
            "| --- | --- | --- |",
            "| 认知 | 事实核查 | 🧠➡️💡 |",
        ]
    )
    assert data is not None
    assert data.headers == ["类别", "描述"]
    assert data.rows == [["认知", "事实核查"]]


def test_width_planner_prefers_descriptive_column() -> None:
    data = parse_table(
        [
            "| 类别 | 描述 | 手段 |",
            "| --- | --- | --- |",
            "| 认知 | 信息茧房 | 批判性思维教育、事实核查、开源情报 |",
        ]
    )
    assert data is not None
    widths = TableWidthPlanner().proportions(data)
    assert widths[2] > widths[0]
