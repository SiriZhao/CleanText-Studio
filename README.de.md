<p align="center">
  <img src="assets/icon.png" width="96" alt="CleanText Studio logo">
</p>

<h1 align="center">CleanText Studio</h1>

<p align="center"><strong>Lokale Textbereinigung, Wiederherstellung der Dokumentstruktur, formelbasierte Vorschau und ausgefeilter DOCX/TXT Export für kopierten und KI-generierten Text.</strong></p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.de.md">Deutsch</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.hi.md">हिन्दी</a>
</p>

<p align="center">
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.5.2"><img src="https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver" alt="Latest release"></a>
  <a href="https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml"><img src="https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Windows-x64-0078D4" alt="Windows x64">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2ea44f" alt="MIT License"></a>
</p>

> **Aktuelle Version: v1.5.2 · Windows x64 · standardmäßig lokal zuerst**

<p align="center">
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/CleanText-Studio-v1.5.2-Windows-x64-Setup.exe"><strong>Installationsprogramm herunterladen</strong></a> ·
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/CleanText-Studio-v1.5.2-Windows-x64-Portable.zip"><strong>Portable ZIP herunterladen</strong></a> ·
  <a href="https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/SHA256SUMS.txt">SHA256 Prüfsummen</a>
</p>

![CleanText Studio Englische Schnittstelle](assets/screenshots/v1.5.2/01-main-light.png)

CleanText Studio verwandelt unordentlichen kopierten Text in ein lesbares, bearbeitbares Dokument, ohne nützliche Strukturen als Rauschen zu behandeln. Es entfernt überflüssige Markdown und Verzierungen, stellt Überschriften, Listen, Tabellen und allgemeine mathematische Notationen wieder her und bietet Ihnen dann eine Textansicht, eine strukturierte Vorschau und einen DOCX- oder TXT-Export. Auf dem Gerät wird eine Grundreinigung durchgeführt; Die optionale KI-Optimierung verwendet nur einen API-Anbieter, den Sie selbst konfigurieren.

**Warum es nützlich ist**

- Behalten Sie die Bedeutung bei und entfernen Sie visuelle Rückstände von Webseiten, Chats, Notizen und generierten Entwürfen.
- Behalten Sie ein Dokumentmodell bei, damit Überschriften, Tabellen, Links und Formeln vor dem Export nicht unbemerkt reduziert werden.
- Überprüfen Sie das Ergebnis, bevor Sie eine native Word-Tabelle, eine bearbeitbare Gleichung oder eine UTF-8-Textdatei schreiben.
- Wechseln Sie zur Laufzeit die Sprache und das Design der Benutzeroberfläche, ohne die Quell-, Ergebnis- oder Bereinigungseinstellungen zu ändern.

## Herunterladen für Windows

CleanText Studio v1.5.2 ist für **Windows x64** veröffentlicht. Wählen Sie das Installationsprogramm für eine normale Installation pro Benutzer oder wählen Sie die tragbare ZIP-Datei, wenn Sie die Ausführung aus einem extrahierten Ordner bevorzugen. Für keines der Pakete ist eine separate Python-Installation erforderlich.

| Paket | Verwendungszweck | Herunterladen |
| --- | --- | --- |
| Einrichtung | Installation, Startmenüeintrag und Deinstallationsunterstützung | [CleanText-Studio-v1.5.2-Windows-x64-Setup.exe](https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/CleanText-Studio-v1.5.2-Windows-x64-Setup.exe) |
| Tragbar | Nach dem Extrahieren der ZIP-Datei ausführen; keine Installation | [CleanText-Studio-v1.5.2-Windows-x64-Portable.zip](https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/CleanText-Studio-v1.5.2-Windows-x64-Portable.zip) |
| Verifizierung | Überprüfen Sie das heruntergeladene Paket | [SHA256SUMS.txt](https://github.com/SiriZhao/CleanText-Studio/releases/download/v1.5.2/SHA256SUMS.txt) |

Die Release-Seite ist die Quelle der Wahrheit für verfügbare Dateien: [CleanText Studio v1.5.2](https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.5.2).

## Was CleanText Studio macht

### Entwickelt für die praktische Dokumentenbereinigung

Kopierte Inhalte werden häufig mit als Markierungen geschriebenen Überschriften, wiederholten Trennzeichen, dekorativen Emojis, unterbrochenen Zeilenumbrüchen, Tutorial-Beschriftungen, eingefügten Links oder Tabellen geliefert, die nur visuell tabellarisch sind. CleanText Studio macht diese Entscheidungen explizit, anstatt eine versteckte, einheitliche Umschreibung anzuwenden. Wählen Sie eine Voreinstellung, überprüfen Sie das Ergebnis und exportieren Sie es erst, wenn die Struktur richtig aussieht.

### Typische Szenarien- Normalisieren Sie Forschungsnotizen, Besprechungsnotizen, Wissensdatenbankauszüge und Webseitenkopien.
- Bereiten Sie KI-gestützte Entwürfe für die Bearbeitung und professionelle Dokumentenbereitstellung vor.
– Stellen Sie eine Markdown-Tabelle wieder her, bevor Sie sie als native Word-Tabelle senden.
- Behalten Sie einfache Inline- und Block-Mathematik bei und entfernen Sie gleichzeitig umgebendes Formatierungsrauschen.
– Erstellen Sie eine saubere TXT-Übergabe, wenn ein Word-Layout nicht erforderlich ist.

## Kernfunktionen

### Markdown und Formatierungsbereinigung

Die Bereinigungspipeline kann Markdown-Überschriftenmarkierungen, Hervorhebungsmarkierungen, Inline-Code-Markierungen, Bildsyntax, horizontale Regeln, kopierte HTML-Reste, dekorative Symbole, Emojis und fragmentierte Anweisungsbeschriftungen entfernen. Es behält normalen Text bei und macht Bereinigungsoptionen im Einstellungsfeld sichtbar.

### Wiederherstellung der Dokumentstruktur

Überschriften, Listen, Zitate, Codeblöcke, Absätze, Tabellen, Links und mathematische Blöcke werden als Dokumentstruktur dargestellt und nicht blind in einen Zeichenstrom zusammengefasst. Aus diesem Grund können Vorschau und Export dieselben strukturellen Entscheidungen treffen.

### Überschriften und Listen

Wählen Sie, ob Sie Markierungen erhalten, eine Struktur naturalisieren oder gegebenenfalls Markierungen entfernen möchten. Das Tool ist darauf ausgelegt, nützliche Hierarchien und Listensemantiken beizubehalten. Es ist kein allgemeiner Rewriter, der eine neue Gliederung erfindet.

### Absätze und Zeilenumbrüche

Drei Modi decken gängiges Quellmaterial ab:

| Modus | Verwenden Sie es, wenn |
| --- | --- |
| Kompakt | Sie möchten normale umbrochene Quellzeilen zu kompakten Absätzen zusammenfügen. |
| Intelligente Abschnitte | Sie möchten einen natürlichen Absatzabstand und gleichzeitig sinnvolle Abschnittsumbrüche. |
| Alles bewahren | Sie müssen die Grenzen des Quellabsatzes so genau wie möglich beibehalten. |

### Links und eigenständige URLs

Die Linkverarbeitung kann Markdown beibehalten, nur den Anzeigetext beibehalten oder den Anzeigetext zusammen mit seiner URL beibehalten. Eigenständige URLs können beibehalten, mit dem vorherigen Absatz zusammengeführt oder entfernt werden, wenn es sich nur um Reste des Tutorials handelt. URLs werden bewusst behandelt und verschwinden nicht als Nebeneffekt der Markdown-Bereinigung.

## Tabellen, Gleichungen und Vorschau

### Markdown-Tabellen und Word-Tabellen

Markdown Tabellen werden in strukturierte Tabellenblöcke analysiert. Im Vorschaumodus wird die Tabelle als Tabelle angezeigt, und der DOCX-Export erstellt eine native Word-Tabelle mit einer Kopfzeile, lesbarem Zelleninhalt, Rändern und Breiten, die aus dem Inhalt ausgewählt werden, und nicht mit einer festen, gleichen Aufteilung. Markdown Trennzeilen, verbleibende Hervorhebungsmarkierungen, bedeutungslose leere Spalten und versehentliche weiche Zeilenumbrüche werden vor dem Export bereinigt, wenn die aktiven Bereinigungseinstellungen dies zulassen.

![Strukturierte Tabellenvorschau](assets/screenshots/v1.5.2/05-table-export.png)

### Mathematische Formeln und bearbeitbare Word Gleichungen

Gängige Inline- und Anzeigetrennzeichen LaTeX, mathematische Unicode-Ausdrücke und einfache Gleichungen werden geschützt, während der umgebende Text bereinigt wird. Unterstützte Formeln werden als native Gleichungen Word OMML ausgegeben, sodass allgemeine Variablen und Ausdrücke weiterhin in Word bearbeitet werden können. Formelabstände, offensichtliche Trennzeichenprobleme und Formelnummerierung können entsprechend den ausgewählten Optionen normalisiert werden.

Komplexe benutzerdefinierte Makros werden nicht stillschweigend verworfen. Wenn eine Formel außerhalb des unterstützten Konvertierungsbereichs liegt, behält die Anwendung einen lesbaren Fallback bei und meldet dies in den Exportqualitätsinformationen.

![Formelbasierte Vorschau](assets/screenshots/v1.5.2/06-word-export.png)

### Textmodus und Vorschaumodus

Der Textmodus ist nützlich, um das normalisierte, einfache Ergebnis zu überprüfen. Im Vorschaumodus werden Überschriften, Listen, Tabellen, Links und Formeln in dokumentenorientierter Form angezeigt. Durch das Wechseln des Anzeigemodus wird die Bereinigung nicht erneut ausgeführt und Ihr Ergebnis wird nicht geändert.

## Vorher und NachherDas folgende kompakte Beispiel zeigt, welche Art von Rückständen die Anwendung reinigen soll, während nützliche Inhalte erhalten bleiben.

**Quelle**```markdown
### **Project notes** ✨
---
Read the **draft** first.

- Keep the main conclusion
- Remove decorative labels

| Item | Value |
| --- | --- |
| Formula | \( E = mc^2 \) |

https://example.com/reference
```**Ergebniskonzept**```text
Project notes

Read the draft first.

• Keep the main conclusion
• Remove decorative labels

The table and E = mc² formula remain structured in Preview and DOCX export.
`

![Quelle und bereinigtes Ergebnis](assets/screenshots/v1.5.2/03-before-after-light.png)

## Formate exportieren

### Exportieren Word

Wählen Sie den Word-Export, wenn das Ziel Überschriften, Listen, Tabellen und unterstützte Formeln als bearbeitbare Dokumentelemente benötigt. Der Exporter erstellt eine `.docx`-Datei; Es automatisiert keine lokal installierte Word-Anwendung. Vor dem Export kann die App eine Struktur- und Qualitätszusammenfassung anzeigen, sodass wiederherstellbare Formel-/Tabellenbeschränkungen sichtbar sind.

### Exportieren TXT

Wählen Sie TXT für ein portables UTF-8-Nur-Text-Ergebnis. Der TXT-Export behält den normalisierten Textinhalt bei, kann jedoch keine Word-nativen Tabellen oder bearbeitbaren OMML-Gleichungen als umfangreiche Dokumentobjekte darstellen.

| Eingabe | Ausgabe |
| --- | --- |
| TXT, Markdown, MD, DOCX | UTF-8 TXT und strukturiert DOCX |

## Sprachen, Themen und Zugänglichkeit

Die Desktop-Oberfläche bietet vereinfachtes Chinesisch, traditionelles Chinesisch, Englisch, Japanisch, Koreanisch, Spanisch, Französisch, Deutsch, brasilianisches Portugiesisch, Russisch, Arabisch und Hindi. Sprachänderungen werden zur Laufzeit angewendet und behalten Text, Ergebnisse, aktuelle Auswahlen und den Rückgängig-Verlauf bei. Arabisch verwendet eine Schnittstelle von rechts nach links, während technische Werte wie URLs, API-Schlüssel und Code von links nach rechts lesbar bleiben.

Helle und dunkle Themen haben das gleiche Panel, die gleiche Steuerung, den gleichen Fokus und das gleiche abgerundete Oberflächensystem. Die Anwendung verwendet, sofern verfügbar, Fallbacks für gesetzliche Systemschriften. Apple PingFang-Dateien werden **nicht** gebündelt.

![Dunkles Thema und abgerundete Oberflächen](assets/screenshots/v1.5.2/07-settings.png)

## Optionale KI-Optimierung (BYOK)

KI-Optimierung ist optional. Einfache Bereinigung, Vorschau, TXT-Export und DOCX-Export sind ohne Netzwerkverbindung verfügbar. Wenn Sie die KI-Optimierung bewusst aktivieren, wählen Sie einen unterstützten Anbieter, Endpunkt, Modell und Ihren eigenen API-Schlüssel. Die Anwendung stellt keinen gemeinsamen kostenlosen API-Schlüssel bereit und stellt keinen Proxy für Ihr Anbieterkonto bereit.

DeepSeek und andere Anbieter, die durch die installierte Anwendungskonfiguration verfügbar gemacht werden, können über den AI-Einstellungsdialog ausgewählt werden. Anbieter- und Modellkennungen bleiben von den übersetzten Anzeigebezeichnungen getrennt. Lesen Sie die Datenbedingungen des Anbieters, bevor Sie sensibles Material versenden.

![AI-Konfiguration](assets/screenshots/v1.5.2/07-settings.png)

## Schnellstart

1. Starten Sie CleanText Studio und fügen Sie Text ein oder öffnen Sie eine unterstützte Datei.
2. Wählen Sie eine Reinigungsvoreinstellung und passen Sie nur die für dieses Dokument erforderlichen Optionen an.
3. Klicken Sie auf **Bereinigen** und überprüfen Sie dann den Textmodus oder den Vorschaumodus.
4. Exportieren Sie nach Word für eine strukturierte Übermittlung oder nach TXT für eine normalisierte Klartextdatei.
5. Konfigurieren Sie bei Bedarf Ihren eigenen KI-Anbieter und entscheiden Sie bewusst, wann Sie Text an ihn senden möchten.

### Installationsprogramm oder tragbare Version

- **Installer:** Führen Sie die ausführbare Setup-Datei aus, folgen Sie dem Installationsprogramm und starten Sie CleanText Studio über das Startmenü. Verwenden Sie die Windows Apps-Einstellungen oder das Deinstallationsprogramm, um es zu entfernen.
- **Portabel:** Extrahieren Sie die ZIP-Datei in einen beschreibbaren Ordner und starten Sie die darin enthaltene ausführbare Datei. Halten Sie die extrahierten Dateien zusammen; Führen Sie es nicht direkt aus einem komprimierten Archiv aus.

### Vollständiger Arbeitsablauf

1. Geben Sie den Quelltext in das linke Feld ein.
2. Legen Sie im mittleren Bereich fest, wie mit Markdown, Links, Absätzen, Listen und Formeln umgegangen wird.
3. Überprüfen Sie das bereinigte Ergebnis rechts und verwenden Sie die Vorschau für Tabellen und Gleichungen.
4. Verwenden Sie die Ergebnissymbolleiste, um das neueste Ergebnis zu kopieren, rückgängig zu machen, wiederherzustellen, zu löschen, TXT zu exportieren oder Word zu exportieren.
5. Bewahren Sie eine Kopie der Originalquelle auf, wenn das Dokument rechtliche, archivarische oder publikationsrelevante Bedeutung hat.

## Datenschutz, Sicherheit und Datenfluss

### Local-First-GrundverarbeitungDie Grundbereinigung wird lokal ausgeführt. Die Anwendung verfügt über kein Kontosystem, keinen Werbedienst, keinen Telemetriedienst und keinen gemeinsamen öffentlichen Schlüssel API. Ihr Text wird nicht hochgeladen, nur weil er eingefügt, in der Vorschau angezeigt, bereinigt oder lokal exportiert wird.

### AI-Anfragen sind Opt-in

Nur eine explizite KI-Optimierungsaktion nutzt den von Ihnen konfigurierten Drittanbieter. Der Anbieter erhält das für diese Anfrage benötigte Material zu seinen eigenen Bedingungen. Verwenden Sie keine Anbieteranfrage für Material, zu dessen Weitergabe Sie nicht berechtigt sind.

### API Schlüsselverarbeitung

API-Schlüssel werden vom Benutzer bereitgestellt und nicht in die exportierte Dokumentkonfiguration geschrieben. Auf Windows verwendet die Anwendung ihren konfigurierten Speichermechanismus für Anmeldeinformationen, sofern verfügbar; Wenn kein sicherer Speicher für Anmeldeinformationen verfügbar ist, greift er sicher zurück, anstatt stillschweigend einen Klartextschlüssel zu exportieren. Behandeln Sie Ihr Betriebssystemkonto und Ihre Provider-Anmeldeinformationen als Sicherheitsgrenzen.

## Systemanforderungen

- Windows x64.
- Eine aktuell unterstützte Windows Desktop-Umgebung.
– Keine separat installierte Python-Laufzeit für Release-Pakete.
- Der Internetzugang ist optional und wird nur für GitHub-Downloads, optionale KI-Nutzung oder vom Benutzer geöffnete Links benötigt.

Windows SmartScreen kann eine Reputationswarnung für einen neuen, nicht signierten oder einen Build mit geringer Reputation anzeigen. Laden Sie es nur von der Repository-Release-Seite herunter, überprüfen Sie die Prüfsumme SHA256 und befolgen Sie die Softwareinstallationsrichtlinien Ihrer Organisation.

## Technischer Stack und Projektarchitektur

CleanText Studio ist eine Python Desktop-Anwendung, die PySide6 für die Schnittstelle, python-docx für DOCX zum Schreiben, PyInstaller für tragbare Paketierung, Inno Setup für das Windows-Installationsprogramm und pytest/Ruff/mypy für Qualitätsprüfungen verwendet. Das Bereinigungs- und Dokumentblockmodell befindet sich unterhalb der Präsentationsebene, sodass Text, Vorschau und Export dieselbe normalisierte Struktur nutzen können.```text
src/cleantext_studio/
├── app.py                 # desktop window and presentation wiring
├── cleaners/              # stable text-cleaning pipeline
├── math/                  # detection, parsing, preview, and OMML support
├── exporters/             # DOCX and TXT exporters
├── i18n/                  # locale catalogs and runtime translation service
├── ui/                    # cards, controls, and theme components
└── llm/                   # optional provider configuration and requests
assets/                    # icon, screenshots, and packaged resources
scripts/                   # validation, screenshot, and Windows-build helpers
tests/                     # unit, GUI, integration, and regression checks
```## Von der Quelle ausführen

Die folgenden Befehle entsprechen dem Entwicklungslayout des Repositorys auf PowerShell.```powershell
git clone https://github.com/SiriZhao/CleanText-Studio.git
cd CleanText-Studio
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```## Testen und erstellen```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\ruff check .
.\.venv\Scripts\mypy src/cleantext_studio
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python scripts/check_translations.py
.\.venv\Scripts\python scripts/check_readme_quality.py
.\.venv\Scripts\python scripts/check_screenshot_quality.py
.\.venv\Scripts\python scripts/verify_cleaning_freeze.py
.\scripts\build_windows.ps1
```Der Build Windows schreibt seine aktuellen Artefakte, Prüfsummen und Versionshinweise in `dist/`. Die Build-Ausgabe wird absichtlich nicht im Repository festgeschrieben.

## Artefakte freigeben und SHA256-Überprüfung durchführen

Jede Version enthält die ausführbare Setup-Datei, Portable ZIP, `SHA256SUMS.txt` und Versionshinweise, sofern verfügbar. Vergleichen Sie in PowerShell ein heruntergeladenes Artefakt mit der veröffentlichten Prüfsumme:```powershell
Get-FileHash .\CleanText-Studio-v1.5.2-Windows-x64-Setup.exe -Algorithm SHA256
Get-Content .\SHA256SUMS.txt
```## Internationalisierungs- und Übersetzungsbeiträge

Die offiziellen Gebietsschemakataloge sind `zh_CN`, `zh_TW`, `en_US`, `ja_JP`, `ko_KR`, `es_ES`, `fr_FR`, `de_DE`, `pt_BR`, `ru_RU`, `ar` und `hi_IN`. Lesen Sie [docs/TRANSLATION_GLOSSARY.md](docs/TRANSLATION_GLOSSARY.md) und [docs/README_TRANSLATION_STATUS.md](docs/README_TRANSLATION_STATUS.md), bevor Sie Terminologieänderungen vorschlagen. Eine Überprüfung der Community-Übersetzung ist willkommen. Dieses Repository erhebt keinen Anspruch darauf, dass jede Dokumentationsübersetzung von einem Muttersprachler überprüft wurde.

## Roadmap

Die aktuelle öffentliche Version ist Windows x64. Zukünftige Plattformarbeit, bessere Importtreue und eine breitere Formelabdeckung sind eher Roadmap-Themen als aktuelle Versandansprüche. Funktionsanfragen und Problemberichte sind willkommen, ein Roadmap-Eintrag ist jedoch keine Verpflichtung oder Veröffentlichungsankündigung.

## Bekannte Einschränkungen

– Komplexe benutzerdefinierte LaTeX-Makros erfordern möglicherweise einen lesbaren Fallback anstelle der nativen Word-Gleichungskonvertierung.
- Der DOCX-Import kann nicht jeden ursprünglichen Stil, jedes eingebettete Objekt oder jede Layoutfunktion aus beliebigen Word-Dateien beibehalten.
- TXT kann keine umfangreichen Word-nativen Tabellen oder bearbeitbaren Gleichungen codieren.
– Die optionale KI-Ausgabe wird von dem von Ihnen ausgewählten Drittanbieter erstellt und erfordert eine menschliche Überprüfung.
- Windows Verpackung ist die einzige hier genannte veröffentlichte Plattform; macOS, Linux, Android und iOS werden derzeit nicht als veröffentlichte Builds beworben.

## FAQ

### Muss ich online sein?

Nein. Lokale Bereinigung, Vorschau und lokaler Export funktionieren ohne Netzwerkverbindung. Der Netzwerkzugriff ist nur für Aktionen wie das Herunterladen von Veröffentlichungen, das Öffnen eines externen Links oder eine von Ihnen ausgewählte KI-Anfrage erforderlich.

### Wird die Anwendung meinen Text hochladen?

Nicht für die grundlegende lokale Verarbeitung. Eine Drittanfrage erfolgt nur, wenn Sie explizit die KI-Optimierung bei Ihrem eigenen konfigurierten Anbieter nutzen.

### Muss ich einen API-Schlüssel konfigurieren?

Nein. Ein API-Schlüssel wird nur für die optionale KI-Optimierung benötigt.

### Welche Dateien kann ich verwenden?

Die Anwendung akzeptiert die Eingaben TXT, Markdown/MD und DOCX und kann UTF-8 TXT oder strukturierte DOCX exportieren.

### Was ist der Unterschied zwischen dem Word- und dem TXT-Export?

Word kann umfangreiche Strukturen wie Überschriften, native Tabellen und unterstützte bearbeitbare Gleichungen beibehalten. TXT ist eine saubere Textübergabe UTF-8 ohne umfangreiche Dokumentobjekte.

### Warum wird der Word-Export für einige Dokumente empfohlen?

Es ist das Format, das die wiederhergestellte Dokumentstruktur am getreuesten wiedergeben kann, insbesondere Tabellen und unterstützte Formeln.

### Sind Formeln editierbar?

Unterstützte Formeln werden als native Gleichungen Word OMML exportiert. Komplexe, nicht unterstützte Makros verwenden möglicherweise einen lesbaren Fallback und sollten vor der Veröffentlichung überprüft werden.

### Werden Tabellen als Word-Tabellen exportiert?

Strukturierte Markdown-Tabellen werden als native Word-Tabellen exportiert, wenn der Word-Export ausgewählt ist.

### Wie ändere ich die Sprache oder das Thema?

Verwenden Sie die Sprach- und Designsteuerelemente in der Anwendungssymbolleiste/-einstellungen. Der Laufzeitschalter behält das aktive Dokument und die Bereinigungsauswahl bei.

### Wo ist mein API-Schlüssel gespeichert?

Die App verwendet ihren konfigurierten Anmeldeinformationsspeicherpfad Windows, sofern verfügbar, und schließt den Schlüssel nicht in die exportierte Konfiguration ein. Überprüfen Sie die Einstellungen des installierten Builds und Ihre Systemsicherheitsrichtlinie.

### Installer oder tragbares ZIP?

Wählen Sie das Installationsprogramm für die normale Windows-Integration und Deinstallationsunterstützung. Wählen Sie „Portabel“, wenn Sie einen extrahierten, eigenständigen Ordner wünschen.

### Wie melde ich ein Problem oder trage eine Übersetzung bei?Öffnen Sie ein Problem oder eine Pull-Anfrage in [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio), einschließlich eines nicht vertraulichen Beispiels und des erwarteten Ergebnisses, sofern möglich.

## Mitwirken

Bitte lesen Sie [CONTRIBUTING.md](CONTRIBUTING.md), bevor Sie eine Pull-Anfrage öffnen. Konzentrieren Sie sich auf Änderungen, fügen Sie Tests hinzu, wenn sich das Verhalten ändert, vermeiden Sie die Festschreibung von Build-Ausgaben oder Anmeldeinformationen und bewahren Sie den lokalen Datenschutzstatus des Projekts.

## Entwickler

Verwaltet von [SiriZhao](https://github.com/SiriZhao). Projekthomepage: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio).

## Lizenzen von Drittanbietern

Hinweise zu verteilten und Laufzeitabhängigkeiten finden Sie unter [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md). CleanText Studio packt keine Apple PingFang-Schriftartendateien.

## Lizenz

CleanText Studio ist unter der [MIT License](LIZENZ) verfügbar.

> Eine Überprüfung dieser README-Übersetzung durch die Community ist willkommen.
