import json
import re
from importlib.resources import files

import emoji

from cleantext_studio.models import TextBlock


class BoilerplatePhraseCleaner:
    def __init__(self) -> None:
        data = json.loads(
            files("cleantext_studio")
            .joinpath("resources/boilerplate_phrases_zh.json")
            .read_text(encoding="utf-8")
        )
        self.start = [re.compile(rf"^(?:{pattern})") for pattern in data["start"]]
        self.end = [re.compile(rf"(?:{pattern})$") for pattern in data["end"]]

    @staticmethod
    def _plain(text: str) -> str:
        text = emoji.replace_emoji(text, replace="").strip(" \t\n\r#＃*_'\"“”‘’")
        return re.sub(r"\s+", "", text)

    def clean(self, blocks: list[TextBlock]) -> tuple[list[TextBlock], int]:
        nonempty = [i for i, block in enumerate(blocks) if block.text.strip()]
        removed = 0
        for index in nonempty[:1]:
            plain = self._plain(blocks[index].text)
            for pattern in self.start:
                match = pattern.match(plain)
                if match:
                    remainder = plain[match.end() :]
                    blocks[index].text = remainder
                    blocks[index].modified = True
                    blocks[index].reasons.append("boilerplate_start")
                    removed += 1
                    break
        for index in reversed(nonempty[-1:]):
            plain = self._plain(blocks[index].text)
            if any(pattern.fullmatch(plain) for pattern in self.end):
                blocks[index].text = ""
                blocks[index].modified = True
                blocks[index].reasons.append("boilerplate_end")
                removed += 1
        return blocks, removed
