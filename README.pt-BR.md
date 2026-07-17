<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio logo"></p>

# Estúdio CleanText

**Limpeza de texto local, recuperação de estrutura de documento, visualização com reconhecimento de fórmula e exportação DOCX/TXT para texto copiado, gerado por IA e mal formatado.**

[Inglês](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md)

[![Latest release](https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver)](https://github.com/SiriZhao/CleanText-Studio/releases) [![CI](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg)](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml) ![Python 3.12](https://img.shields.io/badge/Python-3.12-blue) ![Windows](https://img.shields.io/badge/Windows-x64-0078d4) [![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<!-- section:download -->
## Baixar para Windows

Current version: **v1.5.0**. Download the [Windows installer](https://github.com/SiriZhao/CleanText-Studio/releases/latest) for a per-user installation, or the **Portable ZIP** to run without installation. Packages are built for Windows x64 and do not require a separately installed Python runtime.

![CleanText Studio in English](assets/screenshots/v1.5.0/hero-main-en.png)

<!-- section:features -->
## O que há de novo na v1.5.0

- Catálogos de localidade estáticos completos, uma caixa de diálogo de Ajuda local e validação de localidade atômica para a camada de apresentação.
- Mantive os rótulos da caixa de combinação separados dos valores de limpeza estáveis, para que a alteração do idioma nunca altere uma predefinição ou acione a limpeza.
- Painel unificado, controle, foco, caixa de seleção e arredondamento de cartão de resumo por meio de tokens de design compartilhados.
- Usa substitutos de fonte do sistema legal. Nenhum PingFang, HarmonyOS Sans ou outro arquivo de fonte está incluído nesta versão.
- Reformulação da documentação principal e adição de verificações automatizadas de README, linguagem de UI e congelamento de limpeza.

## O que isso faz

CleanText Studio remove resíduos de formatação copiados enquanto preserva a estrutura útil do documento. Ele reconhece títulos, listas, citações, códigos, tabelas Markdown, links e fórmulas matemáticas comuns. O mesmo modelo de documento estruturado alimenta o editor de texto, a visualização, a exportação TXT e a exportação DOCX para que uma tabela ou fórmula não seja perdida silenciosamente na exportação.

### Limpeza e recuperação de estrutura

- Limpe títulos de Markdown, ênfase, código embutido, links, imagens, separadores, resíduos de cópia HTML, emoji e caracteres decorativos.
- Detecte títulos, listas, citações, blocos de código e tabelas em vez de nivelá-los em uma parede de caracteres.
- Escolha união compacta, espaçamento de seção inteligente ou limites de parágrafo preservados.
- Mantenha URLs independentes por padrão; o tratamento opcional de URL é explícito.

### Exportação de tabelas e Word

As tabelas Markdown são analisadas em blocos de tabelas estruturados. O modo de visualização exibe uma tabela real e a exportação DOCX grava uma tabela nativa do Word com cabeçalho em negrito, bordas visíveis, larguras adaptáveis ​​​​e texto de célula limpo. O conteúdo longo permanece legível em vez de se tornar uma sequência de linhas curtas forçadas.

### Matemática

LaTeX comum em linha e de exibição, expressões matemáticas Unicode e equações simples são protegidas antes da limpeza do Markdown. As fórmulas suportadas são exportadas como equações nativas do Word OMML; construções não suportadas voltam para texto legível em vez de perder variáveis. O aplicativo não calcula, prova ou altera o significado matemático.

### Otimização opcional de IA BYOK

A limpeza local funciona totalmente offline. A otimização de IA é opcional e só é executada depois que você configura seu próprio provedor, endpoint, modelo e chave de API. CleanText Studio não fornece chaves públicas, provedores de proxy ou pagamento de contas modelo. Não envie material que não seja adequado para processamento por terceiros.

<!-- section:privacy -->
## Privacidade e segurança

Limpeza básica, visualização, exportação TXT e exportação Word são executadas localmente. O aplicativo não possui publicidade, telemetria, sistema de conta ou chave pública de IA. É uma ferramenta de formatação, estrutura de documentos e layout; **não** oferece evasão de detecção de IA, evasão de plágio, falsificação de identidade, má conduta acadêmica ou citações fabricadas.

## Início rápido

1. Inicie o aplicativo, cole o texto ou abra TXT, Markdown ou DOCX.
2. Selecione uma predefinição de limpeza e um modo de parágrafo.
3. Clique em **Limpar** e inspecione **Modo de texto** ou **Modo de visualização**.
4. Exporte conteúdo estruturado para TXT ou Word.

```text
Before: ### Test account
        ---
        **No login required**

After:  Test account
        No login required
```

## Requisitos de entrada, saída e sistema

Entrada: `.txt`, `.md`, `.markdown` e `.docx`. Saída: UTF-8 `.txt` e `.docx` estruturado. v1.5.0 é uma versão para desktop do Windows x64. macOS, Linux e Android não são considerados plataformas lançadas.

## Da fonte

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```

<!-- section:build -->
## Testar e construir

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

A compilação do Windows produz um aplicativo onedir, um ZIP portátil, um instalador Inno Setup, somas de verificação SHA256 e notas de versão em `dist/`.

## Localização, contribuições e limitações

A interface oferece chinês simplificado, chinês tradicional, inglês, japonês, coreano, espanhol, francês, alemão, português brasileiro, russo, árabe (RTL) e hindi. A revisão da tradução é bem-vinda; consulte [o guia de tradução](docs/TRANSLATION_GUIDE.md). Macros LaTeX personalizadas complexas podem usar um substituto de texto, e a importação DOCX não preserva todos os estilos de documentos de origem ou imagens incorporadas.

Developer: [SiriZhao](https://github.com/SiriZhao) · Project: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio) · See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

<!-- section:license -->
## Licença

Licença MIT. Consulte [LICENSE](LICENSE) e [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

> Translation review from the community is welcome.
