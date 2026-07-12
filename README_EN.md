# CleanText Studio

CleanText Studio v1.1.1 is a local-first Windows desktop application for deterministic text cleanup, document structure normalization, and TXT/DOCX export.

Developer: **SiriZhao** · Repository: [github.com/SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio)

Offline cleanup requires no account or API. Optional BYOK optimization supports OpenAI, DeepSeek, Anthropic, OpenAI-compatible, and local-compatible endpoints. Provider presets update Base URLs and suggested models; DeepSeek defaults to `https://api.deepseek.com`. API keys use Windows Credential Manager or session memory.

v1.1.1 adds system/light/dark themes, three paragraph-break modes, offline boilerplate cleanup, a redesigned Chinese Provider dialog, centralized design tokens, and installed-font fallback. No commercial font is bundled. The software does not provide AI-detection or plagiarism circumvention features.

Run `python -m cleantext_studio.main`; package with `scripts/build_windows.ps1`. MIT licensed.
