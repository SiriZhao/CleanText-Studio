# Contributing to CleanText Studio

Thank you for improving a privacy-first, local-first document tool.

## Before you start

- Search existing issues and pull requests first.
- Keep a change focused. Do not combine a UI adjustment with an unrelated cleanup-algorithm rewrite.
- Never commit API keys, private documents, generated build output, or locally exported files.
- Preserve the documented local-first privacy posture and avoid AI-bypass claims.

## Development workflow

```powershell
git fork https://github.com/SiriZhao/CleanText-Studio.git
git clone https://github.com/<your-account>/CleanText-Studio.git
cd CleanText-Studio
git checkout -b fix/short-description
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
```

Run the relevant checks before opening a pull request:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\ruff check .
.\.venv\Scripts\mypy src/cleantext_studio
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python scripts/check_translations.py
.\.venv\Scripts\python scripts/verify_cleaning_freeze.py
```

## Pull requests

1. Use an imperative commit subject such as `fix: preserve inline formula boundaries`.
2. Explain the user-visible impact and any compatibility consideration.
3. Add or update tests for behavior changes.
4. Include screenshots for visible UI changes and keep them free of private paths or credentials.
5. Do not change frozen cleanup baselines to conceal a regression.

## Finding a contribution

- Start with issues labeled [`good first issue`](https://github.com/SiriZhao/CleanText-Studio/labels/good%20first%20issue) for bounded, reviewed tasks.
- Use [`help wanted`](https://github.com/SiriZhao/CleanText-Studio/labels/help%20wanted) for work where maintainers are actively seeking assistance.
- Documentation, translation, test-fixture, accessibility, and packaging reviews are valuable contributions. See the recommended taxonomy in [.github/labels.md](.github/labels.md).

## Translations and documentation

Read [docs/TRANSLATION_GLOSSARY.md](docs/TRANSLATION_GLOSSARY.md). Preserve product names, API names, URLs, and license names. Community review of documentation translations is welcome.

## Code of conduct

Be respectful, assume good intent, and keep discussions focused on reproducible technical behavior.
