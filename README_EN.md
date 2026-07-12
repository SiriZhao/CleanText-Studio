# CleanText Studio

CleanText Studio v1.2.2 is a local-first Windows desktop application for deterministic text cleanup, document structure normalization, Markdown table preview, and native TXT/DOCX export.

Developer: **SiriZhao** · Repository: [github.com/SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio)

Offline cleanup requires no account or API. Optional BYOK optimization supports OpenAI, DeepSeek, Anthropic, OpenAI-compatible, and local-compatible endpoints. DeepSeek now suggests `deepseek-v4-flash` for new configurations; existing user-selected models remain unchanged.

v1.2.0 parses Markdown tables into structured blocks, displays them in preview mode, and exports native Word tables with headers, borders, wrapping, and Chinese font settings. It also improves Provider controls and removes the unstable boilerplate-cleaning feature.

v1.2.1 splits cleanup into explicit normalization, Markdown, structure, high-confidence AI pattern, URL, and paragraph-formatting stages. Tutorial URL instructions are removed while ordinary document URLs remain intact.

v1.2.2 adds opt-in instructional-label cleanup, three context-aware standalone URL modes, block-aware residual warnings, consistent modification records, and a Word export structure summary. Preview and DOCX export use the same structured block result.

Run `python -m cleantext_studio.main`; package with `scripts/build_windows.ps1`. MIT licensed.
