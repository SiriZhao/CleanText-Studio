<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio logo"></p>

# 清潔文字工作室

**本地優先文字清理、文件結構恢復、公式感知預覽以及複製的、AI 生成的和格式不良的文本的 DOCX/TXT 導出。 **

[English](README.md) · [簡體中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本文](README.ja.md) · [한국어](README.ko.md) . [Français](README.fr.md) · [德語](README.de.md) · [葡萄牙語](README.pt-BR.md) · [Русский](README.ru.md) · [हिनскиФ](README.ru.md) · [हिनскиदी](md [हिन्दी](README.hi.md)

[![Latest release](https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver)](https://github.com/SiriZhao/CleanText-Studio/releases) [![CI](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg)](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml) ![Python 3.12](https://img.shields.io/badge/Python-3.12-blue) ![Windows](https://img.shields.io/badge/Windows-x64-0078d4) [![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<!-- section:download -->
## 下載 Windows 版

Current version: **v1.5.1**. Download the [Windows installer](https://github.com/SiriZhao/CleanText-Studio/releases/latest) for a per-user installation, or the **Portable ZIP** to run without installation. Packages are built for Windows x64 and do not require a separately installed Python runtime.

![CleanText Studio in English](assets/screenshots/v1.5.0/hero-main-en.png)

<!-- section:features -->
## v1.5.1 中的新增內容

- 完整的靜態語言環境目錄、本地幫助對話框以及表示層的原子語言環境驗證。
- 將組合框標籤與穩定的清潔值分開，因此更改語言永遠不會改變預設或觸發清潔。
- 透過共享設計令牌統一面板、控制項、焦點、複選框和摘要卡舍入。
- 使用法律系統字型後備。此版本中未捆綁 PingFang、HarmonyOS Sans 或其他字型檔案。
- 重新設計了旗艦文件並添加了自動自述文件、UI 語言和清理凍結檢查。

## 它的作用

CleanText Studio 刪除複製的格式殘留，同時保留有用的文件結構。它可以識別標題、清單、引文、程式碼、Markdown 表格、連結和常見的數學公式。相同的結構化文件模型為文字編輯器、預覽、TXT 匯出和 DOCX 匯出提供支持，因此表格或公式在匯出時不會默默遺失。

### 清潔和結構恢復

- 乾淨的 Markdown 標題、強調、內聯代碼、連結、圖像、分隔符號、HTML 複製殘留、表情符號和裝飾字元。
- 偵測標題、清單、引文、程式碼區塊和表格，而不是將它們壓平到字元牆中。
- 選擇緊湊的連接、智慧的節間距或保留的段落邊界。
- 預設保留獨立 URL；可選的 URL 處理是明確的。

### 表格和Word匯出

Markdown 表解析為結構化表塊。預覽模式顯示真實的表格，DOCX 匯出會寫入帶有粗體標題、可見邊框、自適應寬度和乾淨儲存格文字的本機 Word 表格。長內容仍然可讀，而不是變成一系列強制的短行。

### 數學

常見的內聯和顯示 LaTeX、Unicode 數學表達式和簡單方程式在 Markdown 清理之前受到保護。支援的公式匯出為Word OMML本機方程式；不受支援的構造會退回到可讀文字而不是遺失變數。該應用程式不會計算、證明或更改數學含義。

### 可選的 BYOK AI 優化

本地清理工作完全離線進行。 AI 最佳化是可選的，僅在您配置自己的提供者、端點、模型和 API 金鑰後執行。 CleanText Studio 不提供公鑰、代理商提供者或支付模型帳單。請勿發送不適合第三方處理的材料。

<!-- section:privacy -->
## 隱私和安全

基本清理、預覽、TXT 匯出和 Word 匯出在本地運行。該應用程式沒有廣告、遙測、帳戶系統或公共人工智慧金鑰。它是一個格式化、文件結構和佈局工具；它**不**提供人工智慧檢測規避、剽竊規避、冒充、學術不端行為或偽造引用。

## 快速啟動

1. 啟動應用程序，貼上文字或開啟 TXT、Markdown 或 DOCX。
2. 選擇清潔預設和段落模式。
3. 按一下 **清理** 並檢查 **文字模式** 或 **預覽模式**。
4. 將結構化內容匯出到 TXT 或 Word。

```text
Before: ### Test account
        ---
        **No login required**

After:  Test account
        No login required
```

## 輸入、輸出和系統需求

輸入：「.txt」、「.md」、「.markdown」和「.docx」。輸出：UTF-8 `.txt` 和結構化的 `.docx`。 v1.5.1 是 Windows x64 桌面版本。 macOS、Linux 和 Android 未聲明為已發布平台。

## 從源頭

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```

<!-- section:build -->
## 測試和建構

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

Windows 版本會在「dist/」下產生一個 onedir 應用程式、一個便攜式 ZIP、一個 Inno Setup 安裝程式、SHA256 校驗和以及發行說明。

## 本地化、貢獻和限制

介面提供簡體中文、繁體中文、英文、日語、韓語、西班牙語、法語、德語、巴西葡萄牙語、俄語、阿拉伯語（RTL）和印地語。歡迎翻譯審校；請參閱[翻譯指南](docs/TRANSLATION_GUIDE.md)。複雜的自訂 LaTeX 巨集可能會使用文字後備，且 DOCX 匯入不會保留每個來源文件樣式或嵌入圖像。

Developer: [SiriZhao](https://github.com/SiriZhao) · Project: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio) · See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

<!-- section:license -->
## 執照

麻省理工學院許可證。請參閱 [許可證](許可證) 和 [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)。

> Translation review from the community is welcome.
