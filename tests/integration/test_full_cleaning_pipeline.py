from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import CleanOptions


def test_special_acceptance_text() -> None:
    source = """项目备注：

填写：

净文 v1.2.0

点击：

上传。

等待：

上传成功

---

# 第四步：进入微信公众号平台

打开：

https://mp.weixin.qq.com

### 测试账号

**无需登录**
"""
    options = CleanOptions(clean_instructional_labels=True)
    result = clean_text(source, options)
    assert all(
        value not in result.text
        for value in ("###", "---", "**", "填写:", "点击:", "等待:", "打开:")
    )
    assert "净文 v1.2.0" in result.text and "https://mp.weixin.qq.com" in result.text
    assert clean_text(result.text, options).text == result.text
