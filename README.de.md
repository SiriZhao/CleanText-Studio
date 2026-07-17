<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio logo"></p>

# CleanText Studio

**Lokale Textbereinigung, Wiederherstellung der Dokumentstruktur, formelbasierte Vorschau und DOCX/TXT-Export für kopierten, KI-generierten und schlecht formatierten Text.**

[Englisch](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md)

[![Latest release](https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver)](https://github.com/SiriZhao/CleanText-Studio/releases) [![CI](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg)](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml) ![Python 3.12](https://img.shields.io/badge/Python-3.12-blue) ![Windows](https://img.shields.io/badge/Windows-x64-0078d4) [![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<!-- section:download -->
## Für Windows herunterladen

Current version: **v1.5.1**. Download the [Windows installer](https://github.com/SiriZhao/CleanText-Studio/releases/latest) for a per-user installation, or the **Portable ZIP** to run without installation. Packages are built for Windows x64 and do not require a separately installed Python runtime.

![CleanText Studio in English](assets/screenshots/v1.5.0/hero-main-en.png)

<!-- section:features -->
## Was ist neu in v1.5.1?

- Vollständige statische Gebietsschemakataloge, ein lokales Hilfedialogfeld und eine atomare Gebietsschemavalidierung für die Präsentationsebene.
- Die Bezeichnungen der Kombinationsfelder wurden von den stabilen Reinigungswerten getrennt gehalten, sodass durch eine Änderung der Sprache nie eine Voreinstellung geändert oder eine Reinigung ausgelöst wird.
- Einheitliches Panel, Steuerung, Fokus, Kontrollkästchen und Zusammenfassungskartenrundung durch gemeinsame Design-Tokens.
- Verwendet gesetzliche Systemschriftart-Fallbacks. In dieser Version sind keine PingFang-, HarmonyOS Sans- oder andere Schriftartdateien enthalten.
- Die Flaggschiff-Dokumentation wurde überarbeitet und automatisierte README-, UI-Sprach- und Reinigungs-Freeze-Prüfungen hinzugefügt.

## Was es bewirkt

CleanText Studio entfernt kopierte Formatierungsreste und behält gleichzeitig die nützliche Dokumentstruktur bei. Es erkennt Überschriften, Listen, Zitate, Code, Markdown-Tabellen, Links und gängige mathematische Formeln. Das gleiche strukturierte Dokumentmodell speist den Texteditor, die Vorschau, den TXT-Export und den DOCX-Export, sodass eine Tabelle oder Formel beim Export nicht stillschweigend verloren geht.

### Reinigung und Strukturwiederherstellung

- Bereinigen Sie Markdown-Überschriften, Hervorhebungen, Inline-Code, Links, Bilder, Trennzeichen, HTML-Kopierreste, Emojis und dekorative Zeichen.
- Erkennen Sie Überschriften, Listen, Zitate, Codeblöcke und Tabellen, anstatt sie zu einer Zeichenwand zusammenzufassen.
- Wählen Sie zwischen kompakter Verbindung, intelligentem Abschnittsabstand oder beibehaltenen Absatzgrenzen.
- Behalten Sie standardmäßig eigenständige URLs bei; Die optionale URL-Behandlung ist explizit.

### Tabellen- und Word-Export

Markdown-Tabellen werden in strukturierte Tabellenblöcke zerlegt. Im Vorschaumodus wird eine echte Tabelle angezeigt, und der DOCX-Export schreibt eine native Word-Tabelle mit einer fetten Kopfzeile, sichtbaren Rändern, adaptiven Breiten und sauberem Zellentext. Lange Inhalte bleiben lesbar und werden nicht zu einer Folge erzwungener kurzer Zeilen.

### Mathematik

Gängige Inline- und Anzeige-LaTeX-, Unicode-Mathematikausdrücke und einfache Gleichungen werden vor der Markdown-Bereinigung geschützt. Unterstützte Formeln werden als native Word-OMML-Gleichungen exportiert; Nicht unterstützte Konstrukte greifen auf lesbaren Text zurück, anstatt Variablen zu verlieren. Die Anwendung berechnet, beweist oder verändert die mathematische Bedeutung nicht.

### Optionale BYOK-KI-Optimierung

Die lokale Bereinigung funktioniert vollständig offline. Die KI-Optimierung ist optional und wird erst ausgeführt, nachdem Sie Ihren eigenen Anbieter, Endpunkt, Modell und API-Schlüssel konfiguriert haben. CleanText Studio stellt keine öffentlichen Schlüssel, Proxy-Anbieter oder Zahlungsmodellrechnungen zur Verfügung. Senden Sie kein Material, das für die Bearbeitung durch Dritte ungeeignet ist.

<!-- section:privacy -->
## Privatsphäre und Sicherheit

Grundlegende Bereinigung, Vorschau, TXT-Export und Word-Export werden lokal ausgeführt. Die App verfügt über keine Werbung, Telemetrie, Kontosystem oder öffentlichen KI-Schlüssel. Es ist ein Formatierungs-, Dokumentstruktur- und Layout-Tool. Es bietet **keine** Möglichkeit zur Umgehung der KI-Erkennung, zur Umgehung von Plagiaten, zum Identitätswechsel, zu akademischem Fehlverhalten oder zu erfundenen Zitaten.

## Schnellstart

1. Starten Sie die Anwendung, fügen Sie Text ein oder öffnen Sie TXT, Markdown oder DOCX.
2. Wählen Sie eine Reinigungsvoreinstellung und einen Absatzmodus.
3. Klicken Sie auf **Bereinigen** und überprüfen Sie den **Textmodus** oder **Vorschaumodus**.
4. Exportieren Sie strukturierte Inhalte nach TXT oder Word.

```text
Before: ### Test account
        ---
        **No login required**

After:  Test account
        No login required
```

## Eingabe-, Ausgabe- und Systemanforderungen

Eingabe: „.txt“, „.md“, „.markdown“ und „.docx“. Ausgabe: UTF-8 „.txt“ und strukturiertes „.docx“. v1.5.1 ist eine Windows x64-Desktopversion. macOS, Linux und Android werden nicht als veröffentlichte Plattformen beansprucht.

## Aus der Quelle

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```

<!-- section:build -->
## Testen und bauen

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

Der Windows-Build erzeugt eine Onedir-Anwendung, eine portable ZIP-Datei, ein Inno Setup-Installationsprogramm, SHA256-Prüfsummen und Versionshinweise unter „dist/“.

## Lokalisierung, Beiträge und Einschränkungen

Die Schnittstelle bietet vereinfachtes Chinesisch, traditionelles Chinesisch, Englisch, Japanisch, Koreanisch, Spanisch, Französisch, Deutsch, brasilianisches Portugiesisch, Russisch, Arabisch (RTL) und Hindi. Eine Überprüfung der Übersetzung ist willkommen; siehe [den Übersetzungsleitfaden](docs/TRANSLATION_GUIDE.md). Komplexe benutzerdefinierte LaTeX-Makros verwenden möglicherweise einen Text-Fallback, und der DOCX-Import behält nicht jeden Stil des Quelldokuments oder jedes eingebettete Bild bei.

Developer: [SiriZhao](https://github.com/SiriZhao) · Project: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio) · See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

<!-- section:license -->
## Lizenz

MIT-Lizenz. Siehe [LICENSE](LICENSE) und [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

> Translation review from the community is welcome.
