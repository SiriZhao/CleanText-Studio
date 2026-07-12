from cleantext_studio.cleaners.tables import parse_table


def test_alignment_and_malformed_rows() -> None:
    table = parse_table(["|左|中|右|", "|:--|:--:|--:|", "|1|2|", "|3|4|5|"])
    assert table is not None
    assert table.alignments == ["left", "center", "right"]
    assert table.column_count == 3 and table.malformed_rows == [3]
