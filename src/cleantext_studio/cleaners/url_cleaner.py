from __future__ import annotations

import re

from cleantext_studio.models import TextBlock

URL = re.compile(r"^https?://\S+$", re.I)
INSTRUCTION = re.compile(r"^(?:打开|访问|登录|点击)\s*[：:]?\s*$")


class URLCleaner:
    """Remove tutorial-only instruction URL pairs and retain ordinary URLs."""

    def clean(self, blocks: list[TextBlock]) -> int:
        meaningful = [i for i, block in enumerate(blocks) if block.text]
        removed = 0
        for left, right in zip(meaningful, meaningful[1:], strict=False):
            if INSTRUCTION.fullmatch(blocks[left].text) and URL.fullmatch(blocks[right].text):
                for index in (left, right):
                    blocks[index].text = ""
                    blocks[index].modified = True
                    blocks[index].reasons.append("tutorial_url")
                removed += 2
        return removed
