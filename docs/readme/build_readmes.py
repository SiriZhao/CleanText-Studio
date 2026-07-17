"""Build ordinary localized README pages from the factual English master.

The generated Markdown is committed to the repository.  This helper protects
URLs, code, package names, and image paths before translating prose in bounded
chunks; it never runs as part of the application.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
MASTER = ROOT / "README.md"
TARGETS = {
    "zh-CN": "README.zh-CN.md", "zh-TW": "README.zh-TW.md",
    "ja": "README.ja.md", "ko": "README.ko.md", "es": "README.es.md",
    "fr": "README.fr.md", "de": "README.de.md", "pt": "README.pt-BR.md",
    "ru": "README.ru.md", "ar": "README.ar.md", "hi": "README.hi.md",
}
HERO_BY_LOCALE = {
    "zh-CN": "hero-main-zh-cn.png", "zh-TW": "main-zh-tw.png",
    "ja": "main-ja.png", "ko": "main-ko.png", "es": "main-es.png",
    "fr": "main-fr.png", "de": "main-de.png", "pt": "main-pt-br.png",
    "ru": "main-ru.png", "ar": "main-ar-rtl.png", "hi": "main-hi.png",
}
TECHNICAL_TERMS = (
    "CleanText Studio", "Windows", "Word", "TXT", "Markdown", "DOCX",
    "OMML", "LaTeX", "API", "API key", "DeepSeek", "GitHub", "PySide6",
    "PyInstaller", "Inno Setup", "Python", "PowerShell", "SHA256",
    "UTF-8", "SiriZhao", "MIT License", "BYOK", "RTL",
)
NAVIGATION = '''<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.de.md">Deutsch</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.hi.md">हिन्दी</a>
</p>'''
# HTML tags must remain byte-for-byte: translating ``align`` or ``</p>``
# produces invalid GitHub Markdown/HTML in several languages.
TOKEN_RE = re.compile(r"<[^>]+>|https?://[^\s)>]+|`[^`]+`|assets/[A-Za-z0-9_./-]+|CleanText Studio|MIT License|SiriZhao")


def protect(text: str) -> tuple[str, dict[str, str]]:
    values: dict[str, str] = {}

    def replace(match: re.Match[str]) -> str:
        token = f"__CTTOKEN{len(values)}__"
        values[token] = match.group(0)
        return token

    protected = TOKEN_RE.sub(replace, text)
    for term in TECHNICAL_TERMS:
        if term in protected:
            token = f"__CTTOKEN{len(values)}__"
            values[token] = term
            protected = protected.replace(term, token)
    return protected, values


def restore(text: str, values: dict[str, str]) -> str:
    for token, value in values.items():
        # Google Translate may normalize the casing of a token (CTTOKEN ->
        # CTToken). Tokens are internal markers, so case-insensitive recovery
        # is deliberate and keeps tags/links valid in every output language.
        text = re.sub(re.escape(token), value, text, flags=re.IGNORECASE)
    return text


def chunks(text: str, maximum: int = 3800) -> list[str]:
    """Split at paragraph boundaries to keep cloud translator requests safe."""
    parts = re.split(r"(\n\s*\n)", text)
    result: list[str] = []
    current = ""
    for part in parts:
        if len(current) + len(part) > maximum and current:
            result.append(current)
            current = ""
        current += part
    if current:
        result.append(current)
    return result


def translate_prose(target: str, text: str) -> str:
    from deep_translator import GoogleTranslator

    protected, values = protect(text)
    translator = GoogleTranslator(source="en", target=target)
    translated = "".join(translator.translate(part) for part in chunks(protected))
    return restore(translated, values)


def translate_document(target: str, text: str) -> str:
    """Translate prose blocks while retaining code fences byte-for-byte."""
    pieces = re.split(r"(```.*?```)", text, flags=re.DOTALL)
    rendered: list[str] = []
    for piece in pieces:
        rendered.append(piece if piece.startswith("```") else translate_prose(target, piece))
    result = "".join(rendered).rstrip() + "\n"
    # Keep language labels stable and readable. They are labels, not prose for
    # the selected locale, and machine translation can erase mixed-script names.
    result = re.sub(
        r'<p align="center">\s*<a href="README\.md">.*?</p>',
        NAVIGATION,
        result,
        count=1,
        flags=re.DOTALL,
    )
    result = result.replace(
        "assets/screenshots/v1.5.2/hero-main-en.png",
        f"assets/screenshots/v1.5.2/{HERO_BY_LOCALE[target]}",
        1,
    )
    if target == "ar":
        result = '<div dir="rtl">\n\n' + result + "\n</div>\n"
    review = {
        "zh-CN": "欢迎社区协助审校本 README 的中文表述。",
        "zh-TW": "歡迎社群協助校閱本 README 的中文表述。",
        "ja": "この README の翻訳レビューへのコミュニティ参加を歓迎します。",
        "ko": "이 README의 번역 검토에 대한 커뮤니티 참여를 환영합니다.",
        "es": "Agradecemos la revisión comunitaria de la traducción de este README.",
        "fr": "Les contributions de la communauté pour relire cette traduction sont bienvenues.",
        "de": "Eine Überprüfung dieser README-Übersetzung durch die Community ist willkommen.",
        "pt": "A revisão comunitária desta tradução do README é bem-vinda.",
        "ru": "Мы приветствуем помощь сообщества в проверке перевода этого README.",
        "ar": "نرحب بمراجعة المجتمع لترجمة ملف README هذا.",
        "hi": "इस README के अनुवाद की सामुदायिक समीक्षा का स्वागत है।",
    }[target]
    return result + f"\n> {review}\n"


def main() -> int:
    selected = set(sys.argv[1:]) or set(TARGETS)
    unknown = selected - set(TARGETS)
    if unknown:
        raise SystemExit(f"unknown locales: {sorted(unknown)}")
    master = MASTER.read_text(encoding="utf-8")
    for locale, filename in TARGETS.items():
        if locale in selected:
            (ROOT / filename).write_text(translate_document(locale, master), encoding="utf-8")
            print(filename)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
