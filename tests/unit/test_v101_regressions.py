import pytest

from cleantext_studio.cleaners import clean_text, detect_residuals
from cleantext_studio.models import CleanOptions, ListMode, TextBlockType


@pytest.mark.parametrize(
    "source",
    [
        "#标题",
        "# 标题",
        "##标题",
        "### 标题",
        "####标题",
        "#####标题",
        "###### 标题",
        "  ### 标题",
        "＃ 标题",
        "＃＃ 标题",
        "####　标题",
        "####\t标题",
        "####\u00a0标题",
        "####**标题**",
        "**#### 标题**",
        "####  **标题**",
    ],
)
def test_markdown_heading_variants(source: str) -> None:
    result = clean_text(source)
    assert result.text == "标题"
    assert result.blocks[0].type in {
        TextBlockType.HEADING_1,
        TextBlockType.HEADING_2,
        TextBlockType.HEADING_3,
    }


def test_numbered_markdown_headings_are_peers() -> None:
    source = "\n".join(
        [
            "#### 2.2.1 客户端拍照问诊",
            "#### 2.2.2 合作社端：田块管理",
            "#### 2.2.3 农服端：服务对接",
        ]
    )
    result = clean_text(source)
    assert "#" not in result.text
    assert [b.type for b in result.blocks] == [TextBlockType.HEADING_3] * 3


def test_separators_are_removed_without_hyphen_damage() -> None:
    source = "---\n- - -\n— — —\n2025-2026\nA-B\n-3\nx - y\n中文——破折号"
    result = clean_text(source).text
    assert "---" not in result
    for value in ("2025-2026", "A-B", "-3", "x - y", "中文——破折号"):
        assert value in result


@pytest.mark.parametrize("mode", list(ListMode))
def test_list_modes_keep_items_separate(mode: ListMode) -> None:
    result = clean_text("- 提高效率\n- 降低成本", CleanOptions(list_mode=mode))
    assert "提高效率" in result.text and "降低成本" in result.text
    assert len(result.text.splitlines()) == 2


def test_complete_steps_are_not_merged() -> None:
    source = "第一步，选择作物。\n第二步，上传照片。\n第三步，填写描述。"
    assert clean_text(source).text.splitlines() == source.splitlines()


def test_code_and_table_are_protected() -> None:
    source = '```python\nseparator = "---"\n# comment\n```\n\n| A | B |\n|---|---|'
    result = clean_text(source)
    assert 'separator = "---"\n# comment' in result.text
    assert "|---|---|" in result.text


def test_residual_detection_ignores_code_and_table() -> None:
    warnings = detect_residuals("正文 **残留**\n```\n# code\n```\n| # | ** |")
    assert len(warnings) == 1
    assert warnings[0].kind == "markdown_emphasis"


def test_agriculture_acceptance_is_idempotent() -> None:
    source = """2.2 服务及业务简介
本项目的核心产品不是“一个软件”，而是一套县域农业服务系统。
####2.2.1 客户端拍照问诊
农户打开微信小程序，完成三步操作：
第一步，选择作物，例如水稻、小麦、番茄、黄瓜、油菜。
第二步，上传叶片、茎秆、根部、田间整体照片。
第三步，填写简单描述，例如“叶片发黄”“有褐斑”。
####2.2.2 合作社端：田块管理
####2.2.3 农服端：服务对接"""
    once = clean_text(source)
    assert "####" not in once.text
    assert "**" not in once.text
    assert once.text == clean_text(once.text).text
    assert len([b for b in once.blocks if b.type == TextBlockType.HEADING_3]) == 3
