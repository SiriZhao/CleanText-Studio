from __future__ import annotations

import re

from cleantext_studio.models import IndependentURLMode, TextBlock

URL = re.compile(r"^https?://\S+$", re.I)
INSTRUCTION = re.compile(r"^(?:打开|访问|登录|点击)\s*[：:]?\s*$")


class URLCleaner:
    """Remove tutorial-only instruction URL pairs and retain ordinary URLs."""

    def clean(self, blocks: list[TextBlock], mode: IndependentURLMode) -> int:
        if mode == IndependentURLMode.PRESERVE:
            return 0
        removed = 0
        for right, block in enumerate(blocks):
            if not URL.fullmatch(block.text):
                continue
            if mode == IndependentURLMode.MERGE_PREVIOUS:
                target = right - 1
                while target >= 0 and not blocks[target].text:
                    target -= 1
                if target >= 0:
                    blocks[target].text = f"{blocks[target].text} {block.text}"
                    blocks[target].modified = True
                    blocks[target].reasons.append("merge_standalone_url")
                    block.text = ""
                    block.modified = True
                    block.reasons.append("merge_standalone_url")
                    removed += 1
                continue
            left = right - 1
            while left >= 0 and blocks[left].type.value == "blank":
                left -= 1
            if left < 0:
                continue
            instruction = INSTRUCTION.fullmatch(blocks[left].text) or (
                not blocks[left].text and "ai_template_label" in blocks[left].reasons
            )
            if instruction and mode == IndependentURLMode.DELETE_TUTORIAL:
                block.text = ""
                block.modified = True
                block.reasons.append("tutorial_url")
                removed += 1
        return removed
