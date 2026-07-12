from __future__ import annotations

import re

from cleantext_studio.models import TextBlock, TextBlockType

FIELD_LABEL = re.compile(
    r"^(?:填写|输入|点击|打开|进入|选择|上传|等待|确认|保存|提交|复制|粘贴|访问|登录|注册|"
    r"下载|安装|运行|设置|注意|提示|说明|示例|操作|步骤)\s*[：:]\s*$"
)
START_PREFIX = re.compile(r"^(?:以下内容|下面内容|我将|根据你的要求|好的|当然)\s*[：:，,!！。]*\s*")
END_PHRASE = re.compile(r"^(?:希望|如果需要|欢迎|感谢阅读)(?:[：:].*)?[。.!！]?$" )


class AIPatternCleaner:
    """Remove high-confidence AI scaffolding without touching body statements."""

    def clean(self, blocks: list[TextBlock]) -> int:
        removed = 0
        meaningful = [i for i, block in enumerate(blocks) if block.text]
        for offset, index in enumerate(meaningful):
            block = blocks[index]
            if FIELD_LABEL.fullmatch(block.text):
                next_text = blocks[meaningful[offset + 1]].text if offset + 1 < len(meaningful) else ""
                if 0 < len(next_text) < 20 or next_text.startswith(("http://", "https://")):
                    block.text = ""
                    block.modified = True
                    block.reasons.append("ai_template_label")
                    removed += 1
        meaningful = [i for i, block in enumerate(blocks) if block.text]
        for index in meaningful[:3]:
            block = blocks[index]
            changed = START_PREFIX.sub("", block.text, count=1).strip()
            if changed != block.text:
                block.text = changed
                block.modified = True
                block.reasons.append("ai_chat_opener")
                removed += 1
                break
        meaningful = [i for i, block in enumerate(blocks) if block.text]
        for index in reversed(meaningful[-3:]):
            block = blocks[index]
            if block.type == TextBlockType.PARAGRAPH and END_PHRASE.fullmatch(block.text):
                block.text = ""
                block.modified = True
                block.reasons.append("ai_chat_closer")
                removed += 1
                break
        return removed
