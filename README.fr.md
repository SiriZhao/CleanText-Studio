<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio logo"></p>

# Studio CleanText

**Nettoyage du texte en local, récupération de la structure du document, aperçu tenant compte des formules et exportation DOCX/TXT pour le texte copié, généré par l'IA et mal formaté.**

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md)

[![Latest release](https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver)](https://github.com/SiriZhao/CleanText-Studio/releases) [![CI](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg)](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml) ![Python 3.12](https://img.shields.io/badge/Python-3.12-blue) ![Windows](https://img.shields.io/badge/Windows-x64-0078d4) [![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<!-- section:download -->
## Télécharger pour Windows

Current version: **v1.5.0**. Download the [Windows installer](https://github.com/SiriZhao/CleanText-Studio/releases/latest) for a per-user installation, or the **Portable ZIP** to run without installation. Packages are built for Windows x64 and do not require a separately installed Python runtime.

![CleanText Studio in English](assets/screenshots/v1.5.0/hero-main-en.png)

<!-- section:features -->
## Quoi de neuf dans la v1.5.0

- Catalogues de paramètres régionaux statiques complets, boîte de dialogue d'aide locale et validation atomique des paramètres régionaux pour la couche de présentation.
- Les étiquettes de la zone de liste déroulante sont conservées séparément des valeurs de nettoyage stables, de sorte que le changement de langue ne modifie jamais un préréglage ni ne déclenche le nettoyage.
- Panneau, contrôle, focus, case à cocher et carte récapitulative unifiés grâce à des jetons de conception partagés.
- Utilise des solutions de secours pour les polices du système légal. Aucun fichier de police PingFang, HarmonyOS Sans ou autre n'est fourni dans cette version.
- Refonte de la documentation phare et ajout de vérifications automatisées README, du langage de l'interface utilisateur et du nettoyage-gel.

## Ce que ça fait

CleanText Studio supprime les résidus de formatage copiés tout en préservant la structure utile du document. Il reconnaît les titres, les listes, les citations, le code, les tableaux Markdown, les liens et les formules mathématiques courantes. Le même modèle de document structuré alimente l'éditeur de texte, l'aperçu, l'exportation TXT et l'exportation DOCX afin qu'un tableau ou une formule ne soit pas perdu silencieusement lors de l'exportation.

### Nettoyage et récupération de structure

- Nettoyez les titres Markdown, l'emphase, le code en ligne, les liens, les images, les séparateurs, les résidus de copie HTML, les emoji et les caractères décoratifs.
- Détectez les titres, les listes, les citations, les blocs de code et les tableaux au lieu de les aplatir dans un mur de caractères.
- Choisissez une jointure compacte, un espacement intelligent des sections ou des limites de paragraphe préservées.
- Conservez les URL autonomes par défaut ; La gestion facultative des URL est explicite.

### Exportation de tableaux et Word

Les tableaux Markdown sont analysés en blocs de tableaux structurés. Le mode Aperçu affiche un vrai tableau et l'exportation DOCX écrit un tableau Word natif avec un en-tête en gras, des bordures visibles, des largeurs adaptatives et un texte de cellule propre. Le contenu long reste lisible au lieu de devenir une séquence de lignes courtes forcées.

### Mathématiques

Le LaTeX commun en ligne et à affichage, les expressions mathématiques Unicode et les équations simples sont protégés avant le nettoyage Markdown. Les formules prises en charge sont exportées sous forme d'équations natives Word OMML ; les constructions non prises en charge reviennent au texte lisible plutôt que de perdre des variables. L'application ne calcule, ne prouve ni ne modifie la signification mathématique.

### Optimisation facultative de BYOK AI

Le nettoyage local fonctionne complètement hors ligne. L'optimisation de l'IA est facultative et ne s'exécute qu'après avoir configuré votre propre fournisseur, point de terminaison, modèle et clé API. CleanText Studio ne fournit pas de clés publiques, de fournisseurs de proxy ou de modèles de factures payantes. N’envoyez pas de matériel qui ne convient pas au traitement par un tiers.

<!-- section:privacy -->
## Confidentialité et sécurité

Le nettoyage de base, l'aperçu, l'exportation TXT et l'exportation Word s'exécutent localement. L'application n'a pas de publicité, de télémétrie, de système de compte ou de clé d'IA publique. Il s'agit d'un outil de formatage, de structure de document et de mise en page ; il ne propose **pas** d'évasion de la détection de l'IA, d'évasion du plagiat, d'usurpation d'identité, de faute académique ou de citations fabriquées.

## Démarrage rapide

1. Démarrez l'application, collez du texte ou ouvrez TXT, Markdown ou DOCX.
2. Sélectionnez un préréglage de nettoyage et un mode de paragraphe.
3. Cliquez sur **Nettoyer** et inspectez le **Mode texte** ou le **Mode Aperçu**.
4. Exportez du contenu structuré vers TXT ou Word.

```text
Before: ### Test account
        ---
        **No login required**

After:  Test account
        No login required
```

## Configuration requise pour les entrées, les sorties et le système

Entrée : `.txt`, `.md`, `.markdown` et `.docx`. Sortie : UTF-8 `.txt` et `.docx` structuré. v1.5.0 est une version de bureau Windows x64. macOS, Linux et Android ne sont pas revendiqués comme plates-formes publiées.

## De la source

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```

<!-- section:build -->
## Tester et construire

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

La version Windows produit une application onedir, un ZIP portable, un programme d'installation Inno Setup, des sommes de contrôle SHA256 et des notes de version sous « dist/ ».

## Localisation, contributions et limites

L'interface propose le chinois simplifié, le chinois traditionnel, l'anglais, le japonais, le coréen, l'espagnol, le français, l'allemand, le portugais brésilien, le russe, l'arabe (RTL) et l'hindi. La révision de la traduction est la bienvenue ; voir [le guide de traduction](docs/TRANSLATION_GUIDE.md). Les macros LaTeX personnalisées complexes peuvent utiliser un texte de secours, et l'importation DOCX ne préserve pas tous les styles de document source ou images intégrées.

Developer: [SiriZhao](https://github.com/SiriZhao) · Project: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio) · See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

<!-- section:license -->
## Licence

Licence MIT. Voir [LICENSE](LICENSE) et [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

> Translation review from the community is welcome.
