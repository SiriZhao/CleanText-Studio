from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import TextBlockType


def test_ai_markdown_residue_pipeline() -> None:
    source = """以下内容：

### 项目背景

---

**重要内容**

填写：
用户名

点击：
确认

打开：
https://tutorial.example.com/login

URL:
https://example.com/reference

* 第一项
* 第二项

***

感谢阅读：
"""
    result = clean_text(source)
    assert "#" not in result.text
    assert "---" not in result.text
    assert "***" not in result.text
    assert "填写：" not in result.text
    assert "点击：" not in result.text
    assert "tutorial.example.com" not in result.text
    assert "https://example.com/reference" in result.text
    assert result.stats.removed_ai_patterns >= 5
    assert "\n\n\n" not in result.text


def test_markdown_heading_and_list_structure_is_preserved() -> None:
    result = clean_text("# 总标题\n## 项目背景\n### 实施方案\n- 服务农户\n* 服务合作社")
    headings = [block for block in result.blocks if block.type.value.startswith("heading")]
    lists = [block for block in result.blocks if block.type == TextBlockType.LIST_ITEM]
    assert [block.heading_level for block in headings] == [1, 2, 3]
    assert [block.text for block in lists] == ["• 服务农户", "• 服务合作社"]


def test_chat_prefix_keeps_real_body_and_middle_phrase() -> None:
    result = clean_text("当然：人工智能正在发展。\n\n本文说明，希望：是项目名称的一部分。")
    assert result.text.startswith("人工智能正在发展。")
    assert "本文说明，希望:是项目名称的一部分。" in result.text


def test_ai_cleaning_is_idempotent() -> None:
    source = "### 标题\n\n填写：\n用户名\n\n- 内容\n\n---"
    once = clean_text(source).text
    assert clean_text(once).text == once


def test_field_label_is_kept_when_following_content_is_long() -> None:
    source = "注意：\n这是一段超过二十个字符并且包含实际业务事实的正文内容，不能删除提示标签。"
    assert clean_text(source).text.startswith("注意:")


def test_fieldgpt_business_plan_keeps_structure() -> None:
    source = """# 禾小二 FieldGPT 创业方案

## 项目概述
> 面向县域农业服务场景。

|模块|功能|
|-|-|
|AI病虫害识别|拍照识别病害、虫害、草害|
|农事处方生成|提供用药建议与风险提示|

### 服务对象
- 农户
- 合作社
"""
    result = clean_text(source)
    assert [block.heading_level for block in result.blocks if block.heading_level] == [1, 2, 3]
    assert any(block.type == TextBlockType.TABLE and block.table for block in result.blocks)
    assert any(block.type == TextBlockType.QUOTE for block in result.blocks)
    assert sum(block.type == TextBlockType.LIST_ITEM for block in result.blocks) == 2
    assert "#" not in result.text
