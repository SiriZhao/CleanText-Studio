<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio logo"></p>

# Студия чистого текста

**Локальная очистка текста, восстановление структуры документа, предварительный просмотр с учетом формул и экспорт DOCX/TXT для скопированного, созданного искусственным интеллектом и плохо отформатированного текста.**

[Английский](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Испанский](README.es.md) · [Французский](README.fr.md) · [Немецкий](README.de.md) · [Португальский](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md)

[![Latest release](https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver)](https://github.com/SiriZhao/CleanText-Studio/releases) [![CI](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg)](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml) ![Python 3.12](https://img.shields.io/badge/Python-3.12-blue) ![Windows](https://img.shields.io/badge/Windows-x64-0078d4) [![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<!-- section:download -->
## Скачать для Windows

Current version: **v1.5.1**. Download the [Windows installer](https://github.com/SiriZhao/CleanText-Studio/releases/latest) for a per-user installation, or the **Portable ZIP** to run without installation. Packages are built for Windows x64 and do not require a separately installed Python runtime.

![CleanText Studio in English](assets/screenshots/v1.5.0/hero-main-en.png)

<!-- section:features -->
## Что нового в версии 1.5.0

- Полные каталоги статических языковых стандартов, локальное диалоговое окно справки и атомарная проверка языковых стандартов для уровня представления.
- Ярлыки полей со списком сохранены отдельно от стабильных значений очистки, поэтому смена языка никогда не меняет предустановку и не запускает очистку.
- Унифицированная панель, элементы управления, фокус, флажок и округление сводной карточки с помощью общих токенов дизайна.
- Использует легальные резервные системные шрифты. В этот выпуск не включены PingFang, HarmonyOS Sans или другие файлы шрифтов.
- Переработана основная документация и добавлены автоматические проверки README, языка пользовательского интерфейса и очистки при заморозке.

## Что он делает

CleanText Studio удаляет скопированные остатки форматирования, сохраняя при этом полезную структуру документа. Он распознает заголовки, списки, цитаты, код, таблицы Markdown, ссылки и общие математические формулы. Одна и та же модель структурированного документа используется в текстовом редакторе, предварительном просмотре, экспорте TXT и экспорте DOCX, поэтому таблица или формула не теряются при экспорте.

### Очистка и восстановление структуры

- Очистите заголовки Markdown, выделение, встроенный код, ссылки, изображения, разделители, остатки копирования HTML, смайлики и декоративные символы.
- Обнаруживайте заголовки, списки, цитаты, блоки кода и таблицы, а не объединяйте их в стену символов.
- Выбирайте компактное соединение, интеллектуальный интервал между разделами или сохранение границ абзаца.
- Сохраняйте отдельные URL-адреса по умолчанию; необязательная обработка URL-адресов является явной.

### Экспорт таблиц и Word

Таблицы Markdown разбираются на структурированные блоки таблиц. В режиме предварительного просмотра отображается реальная таблица, а при экспорте DOCX записывается собственная таблица Word с полужирным заголовком, видимыми границами, адаптивной шириной и чистым текстом ячеек. Длинный контент остается читабельным, а не превращается в последовательность вынужденных коротких строк.

### Математика

Общие встроенные и отображаемые математические выражения LaTeX, Unicode и простые уравнения защищены до очистки Markdown. Поддерживаемые формулы экспортируются как собственные уравнения Word OMML; неподдерживаемые конструкции возвращаются к читаемому тексту, а не теряют переменные. Приложение не рассчитывает, не доказывает и не меняет математический смысл.

### Дополнительная оптимизация BYOK AI

Локальная очистка работает полностью в автономном режиме. Оптимизация ИИ не является обязательной и запускается только после настройки собственного поставщика, конечной точки, модели и ключа API. CleanText Studio не предоставляет открытые ключи, поставщиков прокси-серверов и не оплачивает счета за модели. Не отправляйте материалы, непригодные для обработки третьей стороной.

<!-- section:privacy -->
## Конфиденциальность и безопасность

Базовая очистка, предварительный просмотр, экспорт TXT и экспорт Word выполняются локально. В приложении нет рекламы, телеметрии, системы учетных записей или открытого ключа искусственного интеллекта. Это инструмент форматирования, структуры и макета документа; он **не** не обеспечивает уклонения от обнаружения ИИ, плагиата, выдачи себя за другое лицо, академических нарушений или сфабрикованных цитат.

## Быстрый старт

1. Запустите приложение, вставьте текст или откройте TXT, Markdown или DOCX.
2. Выберите предустановку очистки и режим абзацев.
3. Нажмите **Очистить** и проверьте **Текстовый режим** или **Режим предварительного просмотра**.
4. Экспортируйте структурированный контент в TXT или Word.

```text
Before: ### Test account
        ---
        **No login required**

After:  Test account
        No login required
```

## Входные, выходные и системные требования

Ввод: `.txt`, `.md`, `.markdown` и `.docx`. Вывод: UTF-8 `.txt` и структурированный `.docx`. v1.5.1 — это версия Windows x64 для настольных компьютеров. macOS, Linux и Android не заявлены как выпущенные платформы.

## Из источника

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```

<!-- section:build -->
## Тестируйте и собирайте

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\ruff check .
.\.venv\Scripts\mypy src/cleantext_studio
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python scripts/check_translations.py
.\.venv\Scripts\python scripts/check_ui_language_consistency.py
.\.venv\Scripts\python scripts/check_readme_quality.py
.\.venv\Scripts\python scripts/verify_cleaning_freeze.py
.\scripts\build_windows.ps1
```

Сборка Windows создает приложение onedir, портативный ZIP-файл, установщик Inno Setup, контрольные суммы SHA256 и примечания к выпуску в разделе `dist/`.

## Локализация, вклад и ограничения

Интерфейс поддерживает упрощенный китайский, традиционный китайский, английский, японский, корейский, испанский, французский, немецкий, бразильский португальский, русский, арабский (RTL) и хинди. Рецензия на перевод приветствуется; см. [руководство по переводу](docs/TRANSLATION_GUIDE.md). Сложные пользовательские макросы LaTeX могут использовать резервный текст, а импорт DOCX не сохраняет каждый стиль исходного документа или встроенное изображение.

Developer: [SiriZhao](https://github.com/SiriZhao) · Project: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio) · See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

<!-- section:license -->
## Лицензия

Лицензия МТИ. См. [ЛИЦЕНЗИЯ](ЛИЦЕНЗИЯ) и [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

> Translation review from the community is welcome.
