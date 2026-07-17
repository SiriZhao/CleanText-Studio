<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio logo"></p>

# 清洁文本工作室

**本地优先文本清理、文档结构恢复、公式感知预览以及复制的、AI 生成的和格式不良的文本的 DOCX/TXT 导出。**

[English](README.md) · [简体中文](README.zh-CN.md) · [繁体中文](README.zh-TW.md) · [日本语](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [德语](README.de.md) · [葡萄牙语](README.pt-BR.md) · [Русский](README.ru.md) · [हिन्दी](README.hi.md) · [हिन्दी](README.hi.md)

[![Latest release](https://img.shields.io/github/v/release/SiriZhao/CleanText-Studio?display_name=tag&sort=semver)](https://github.com/SiriZhao/CleanText-Studio/releases) [![CI](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml/badge.svg)](https://github.com/SiriZhao/CleanText-Studio/actions/workflows/ci.yml) ![Python 3.12](https://img.shields.io/badge/Python-3.12-blue) ![Windows](https://img.shields.io/badge/Windows-x64-0078d4) [![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<!-- section:download -->
## 下载 Windows 版

Current version: **v1.5.1**. Download the [Windows installer](https://github.com/SiriZhao/CleanText-Studio/releases/latest) for a per-user installation, or the **Portable ZIP** to run without installation. Packages are built for Windows x64 and do not require a separately installed Python runtime.

![CleanText Studio in English](assets/screenshots/v1.5.0/hero-main-en.png)

<!-- section:features -->
## v1.5.1 中的新增内容

- 完整的静态语言环境目录、本地帮助对话框以及表示层的原子语言环境验证。
- 将组合框标签与稳定的清洁值分开，因此更改语言永远不会改变预设或触发清洁。
- 通过共享设计令牌统一面板、控件、焦点、复选框和摘要卡舍入。
- 使用法律系统字体后备。此版本中未捆绑 PingFang、HarmonyOS Sans 或其他字体文件。
- 重新设计了旗舰文档并添加了自动自述文件、UI 语言和清理冻结检查。

## 它的作用

CleanText Studio 删除复制的格式残留，同时保留有用的文档结构。它可以识别标题、列表、引文、代码、Markdown 表格、链接和常见的数学公式。相同的结构化文档模型为文本编辑器、预览、TXT 导出和 DOCX 导出提供支持，因此表格或公式在导出时不会默默丢失。

### 清洁和结构恢复

- 干净的 Markdown 标题、强调、内联代码、链接、图像、分隔符、HTML 复制残留、表情符号和装饰字符。
- 检测标题、列表、引文、代码块和表格，而不是将它们压平到字符墙中。
- 选择紧凑的连接、智能的节间距或保留的段落边界。
- 默认保留独立 URL；可选的 URL 处理是显式的。

### 表格和Word导出

Markdown 表被解析为结构化表块。预览模式显示真实的表格，DOCX 导出会写入带有粗体标题、可见边框、自适应宽度和干净单元格文本的本机 Word 表格。长内容仍然可读，而不是变成一系列强制的短行。

### 数学

常见的内联和显示 LaTeX、Unicode 数学表达式和简单方程在 Markdown 清理之前受到保护。支持的公式导出为Word OMML本机方程；不受支持的构造会退回到可读文本而不是丢失变量。该应用程序不会计算、证明或更改数学含义。

### 可选的 BYOK AI 优化

本地清理工作完全离线进行。 AI 优化是可选的，仅在您配置自己的提供商、端点、模型和 API 密钥后运行。 CleanText Studio 不提供公钥、代理提供商或支付模型账单。请勿发送不适合第三方处理的材料。

<!-- section:privacy -->
## 隐私和安全

基本清理、预览、TXT 导出和 Word 导出在本地运行。该应用程序没有广告、遥测、帐户系统或公共人工智能密钥。它是一个格式化、文档结构和布局工具；它**不**提供人工智能检测规避、剽窃规避、冒充、学术不端行为或伪造引用。

## 快速启动

1. 启动应用程序，粘贴文本或打开 TXT、Markdown 或 DOCX。
2. 选择清洁预设和段落模式。
3. 单击 **清理** 并检查 **文本模式** 或 **预览模式**。
4. 将结构化内容导出到 TXT 或 Word。

```text
Before: ### Test account
        ---
        **No login required**

After:  Test account
        No login required
```

## 输入、输出和系统要求

输入：“.txt”、“.md”、“.markdown”和“.docx”。输出：UTF-8 `.txt` 和结构化的 `.docx`。 v1.5.1 是 Windows x64 桌面版本。 macOS、Linux 和 Android 未声明为已发布平台。

## 从源头

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m cleantext_studio.main
```

<!-- section:build -->
## 测试和构建

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

Windows 版本会在“dist/”下生成一个 onedir 应用程序、一个便携式 ZIP、一个 Inno Setup 安装程序、SHA256 校验和以及发行说明。

## 本地化、贡献和限制

界面提供简体中文、繁体中文、英语、日语、韩语、西班牙语、法语、德语、巴西葡萄牙语、俄语、阿拉伯语（RTL）和印地语。欢迎翻译审校；请参阅[翻译指南](docs/TRANSLATION_GUIDE.md)。复杂的自定义 LaTeX 宏可能会使用文本后备，并且 DOCX 导入不会保留每个源文档样式或嵌入图像。

Developer: [SiriZhao](https://github.com/SiriZhao) · Project: [SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio) · See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

<!-- section:license -->
## 执照

麻省理工学院许可证。请参阅 [许可证](许可证) 和 [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)。

> Translation review from the community is welcome.
