<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio logo"></p>

# クリーンテキスト スタジオ

**ローカルファーストのテキストクリーンアップ、文書構造の回復、数式対応プレビュー、コピーされたテキスト、AI 生成されたテキスト、およびフォーマットが不適切なテキストの DOCX/TXT エクスポート。**

[英語](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [スペイン語](README.es.md) · [フランス語](README.fr.md) · [ドイツ語](README.de.md) · [ポルトガル語](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md)

[![Latest release](https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver)](https://github.com/SiriZhao/CleanText-Studio/releases) [![CI](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg)](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml) ![Python 3.12](https://img.shields.io/badge/Python-3.12-blue) ![Windows](https://img.shields.io/badge/Windows-x64-0078d4) [![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<!-- section:download -->
## Windows 用のダウンロード

Current version: **v1.5.1**. Download the [Windows installer](https://github.com/SiriZhao/CleanText-Studio/releases/latest) for a per-user installation, or the **Portable ZIP** to run without installation. Packages are built for Windows x64 and do not require a separately installed Python runtime.

![CleanText Studio in English](assets/screenshots/v1.5.0/hero-main-en.png)

<!-- section:features -->
## v1.5.1の新機能

- 完全な静的ロケール カタログ、ローカル ヘルプ ダイアログ、およびプレゼンテーション レイヤーのアトミック ロケール検証。
- コンボボックスのラベルを安定したクリーニング値から切り離すため、言語を変更してもプリセットが変更されたり、クリーニングがトリガーされたりすることはありません。
- 共有デザイントークンによる統一されたパネル、コントロール、フォーカス、チェックボックス、概要カードの丸め。
- 合法的なシステムフォントのフォールバックを使用します。このリリースには、PingFang、HarmonyOS Sans、またはその他のフォント ファイルはバンドルされていません。
- 主力ドキュメントを改訂し、自動 README、UI 言語、およびクリーニング フリーズ チェックを追加しました。

## 何をするのか

CleanText Studio は、有用なドキュメント構造を維持しながら、コピーされた書式設定の残留物を削除します。見出し、リスト、引用符、コード、マークダウン テーブル、リンク、および一般的な数式を認識します。同じ構造化ドキュメント モデルがテキスト エディター、プレビュー、TXT エクスポート、および DOCX エクスポートにフィードされるため、エクスポート時にテーブルや数式が自動的に失われることはありません。

### 洗浄と構造の回復

- Markdown の見出し、強調、インライン コード、リンク、画像、区切り文字、HTML コピーの残り、絵文字、装飾文字をクリーンアップします。
- 見出し、リスト、引用、コード ブロック、表を文字の壁に平坦化するのではなく、検出します。
- コンパクトな結合、スマートなセクション間隔、または保持された段落境界を選択します。
- デフォルトではスタンドアロン URL を保持します。オプションの URL 処理は明示的です。

### 表と Word のエクスポート

マークダウン テーブルは構造化されたテーブル ブロックに解析されます。プレビュー モードでは実際の表が表示され、DOCX エクスポートでは、太字のヘッダー、表示される枠線、適応幅、およびクリーンなセル テキストを備えたネイティブ Word 表が書き込まれます。長いコンテンツは、強制的に短い行が連続するのではなく、読みやすいままになります。

### 数学

一般的なインラインおよびディスプレイ LaTeX、Unicode 数式、および単純な方程式は、Markdown クリーンアップの前に保護されます。サポートされている数式は、Word OMML ネイティブ数式としてエクスポートされます。サポートされていない構造は、変数を失うのではなく、読み取り可能なテキストに戻ります。このアプリケーションは、数学的意味を計算、証明、変更することはありません。

### オプションのBYOK AI最適化

ローカル クリーンアップは完全にオフラインで機能します。 AI の最適化はオプションであり、独自のプロバイダー、エンドポイント、モデル、API キーを構成した後にのみ実行されます。 CleanText Studio は、公開キー、プロキシ プロバイダー、または支払いモデルの料金を提供しません。第三者による処理に不適切な素材は送信しないでください。

<!-- section:privacy -->
## プライバシーと安全性

基本的なクリーンアップ、プレビュー、TXT エクスポート、および Word エクスポートはローカルで実行されます。このアプリには、広告、テレメトリ、アカウント システム、AI 公開キーはありません。これは、書式設定、文書構造、およびレイアウトのツールです。 AI 検出回避、盗作回避、なりすまし、学術的不正行為、引用の捏造は**提供されません**。

## クイックスタート

1. アプリケーションを起動し、テキストを貼り付けるか、TXT、Markdown、または DOCX を開きます。
2. クリーニング プリセットと段落モードを選択します。
3. [**クリーン**] をクリックし、**テキスト モード** または **プレビュー モード** を調べます。
4. 構造化コンテンツを TXT または Word にエクスポートします。

```text
Before: ### Test account
        ---
        **No login required**

After:  Test account
        No login required
```

## 入力、出力、およびシステム要件

入力: `.txt`、`.md`、`.markdown`、および `.docx`。出力: UTF-8 `.txt` および構造化された `.docx`。 v1.5.1 は Windows x64 デスクトップ リリースです。 macOS、Linux、および Android は、リリースされたプラットフォームとして主張されていません。

## ソースから

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```

<!-- section:build -->
## テストとビルド

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

Windows ビルドは、onedir アプリケーション、ポータブル ZIP、Inno Setup インストーラー、SHA256 チェックサム、およびリリース ノートを `dist/` の下に生成します。

## ローカリゼーション、貢献、および制限

このインターフェイスでは、簡体字中国語、繁体字中国語、英語、日本語、韓国語、スペイン語、フランス語、ドイツ語、ブラジル系ポルトガル語、ロシア語、アラビア語 (RTL)、およびヒンディー語が提供されます。翻訳レビューは歓迎です。 [翻訳ガイド](docs/TRANSLATION_GUIDE.md) を参照してください。複雑なカスタム LaTeX マクロではテキスト フォールバックが使用される場合があり、DOCX インポートではすべてのソース文書スタイルや埋め込み画像が保持されるわけではありません。

Developer: [SiriZhao](https://github.com/SiriZhao) · Project: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio) · See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

<!-- section:license -->
## ライセンス

MITライセンス。 [LICENSE](LICENSE) および [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) を参照してください。

> Translation review from the community is welcome.
