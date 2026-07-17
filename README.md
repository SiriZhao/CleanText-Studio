<p align="center"><img src="assets/icon.png" width="96" alt="CleanText Studio Logo"></p>

# CleanText Studio

Local-first Windows desktop app for cleaning text formatting and exporting polished TXT and Word documents.

**Languages:** [English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md)

本地优先的文本格式清洗、结构整理、数学公式排版与 Word/TXT 导出工具。

[![Version](https://img.shields.io/badge/version-v1.4.0-4f46e5)](https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.4.0) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![License](https://img.shields.io/badge/license-MIT-green)

## Windows 下载

Download the Windows x64 installer or portable ZIP from the [v1.4.0 release](https://github.com/SiriZhao/CleanText-Studio/releases/tag/v1.4.0). The installer is per-user; unpack the portable ZIP and run `CleanText Studio.exe`.

Current version: **v1.4.0** · Developer: **SiriZhao** · [Project home](https://github.com/SiriZhao/CleanText-Studio)

## v1.4.0: Global interface and usability

- Switch the interface at runtime between 12 supported locales; Arabic uses RTL layout.
- Clear SVG checkmarks make selected cleaning rules recognizable in light and dark themes.
- Cleaning option IDs are stable across translated interfaces and legacy labels can migrate safely.
- This release does **not** change the v1.3.2 local cleaning algorithm or its default output.

## v1.3.2 稳定性修复

- 修复中文正文中 `\( O \)`、`\( \lambda \)` 等行内公式的 Word 原生公式导出。
- 清除 Word 正文中的公式定界符和支持范围内 LaTeX 命令残留。
- 清理表格 Markdown、Emoji 空列和无意义单元格软换行，并按内容规划列宽。
- 预览与 Word 共享段落 runs、公式和表格结构，导出前后更一致。

## 新版界面和功能截图

| 行内公式 | 块级与行内公式 |
|---|---|
| ![行内公式](assets/screenshots/inline-math-v1.3.2.png) | ![公式混排](assets/screenshots/block-and-inline-math-v1.3.2.png) |

## 公式渲染展示

![表格清洗](assets/screenshots/table-clean-v1.3.2.png)

## Word 原生公式展示

![Word 表格导出](assets/screenshots/table-word-v1.3.2.png)

## 表格清洗与导出展示

![导出质量](assets/screenshots/export-quality-v1.3.2.png)

## 核心功能

- 清理 Markdown 标题、强调、链接、分隔线、Emoji、装饰符号与复制残留。
- 结构化识别标题、列表、引用、代码、表格与数学公式。
- 三种段落模式；TXT、DOCX 导入和导出；浅色、深色与跟随系统主题。
- 可选 BYOK AI：OpenAI、DeepSeek、Anthropic、OpenAI 兼容及本地兼容接口。

## 清洗前后示例

清洗前：`**公式：** \[S = k_B \ln \Omega\]`；清洗后预览为排版公式，Word 中为可编辑原生公式。普通 Markdown 示例 `### 测试账号` 与 `**无需登录**` 会清理为纯净标题和正文。

## 支持格式

导入 `.txt`、`.md`、`.markdown`、`.docx`；导出 UTF-8 TXT 与结构化 DOCX。

## 使用方法

粘贴或打开文本，选择清洗预设与段落模式，点击“开始清洗”，在文本/预览模式检查结果，再导出 TXT 或 Word。

## AI API 配置

AI 优化默认关闭。用户自行配置 Provider、Base URL、模型和 API Key；密钥保存至 Windows 凭据管理器或仅保留在本次会话。项目不提供公共密钥、不代付费用、不代理模型服务。

## 本地模式与隐私

基础清洗、预览、TXT 和 Word 导出完全离线，不收集遥测，不上传用户文本。第三方 API 的数据处理受相应提供商政策约束。

## Word 导出说明

标题、列表、表格和支持范围内公式使用 Word 原生结构。公式使用 Cambria Math/Word 默认数学字体，正文使用模板字体；自动目录域需在 Word 中更新。

## 数学公式支持范围

支持 `$...$`、`$$...$$`、`\(...\)`、`\[...\]`，常用 equation/align/matrix/cases 环境，上下标、分数、根号、求和、积分、关系符、函数、希腊字母及 `\text{...}`。程序不会计算、化简或改写数学含义。

## 已知限制

- 复杂自定义宏、特殊环境和超深嵌套可能回退为可读文本。
- 轻量预览覆盖常用结构，不是完整 TeX 排版引擎。
- DOCX 导入不保留图片与复杂原始样式；AI 差异仍以全文接受/放弃为主。

## 安装与便携版

Setup 版支持当前用户安装、开始菜单与可选桌面快捷方式；Portable 版不要求 Python，解压即可运行。

## 开发环境

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
.\.venv\Scripts\python -m cleantext_studio.main
```

## 测试

```powershell
.\.venv\Scripts\ruff check .
.\.venv\Scripts\mypy src/cleantext_studio
.\.venv\Scripts\pytest
```

## 构建

运行 `.\scripts\build_windows.ps1` 生成 onedir、Portable ZIP、Inno Setup 安装包和 SHA256。详见 [Windows 构建文档](docs/BUILD_WINDOWS.md)。

## 路线图

继续改进复杂公式兼容、模板管理、逐项差异恢复和无障碍体验。

## 贡献

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [开发文档](docs/DEVELOPMENT.md)。

## 开发者

SiriZhao · [github.com/SiriZhao/CleanText-Studio](https://github.com/SiriZhao/CleanText-Studio)

## 许可证

MIT License。Copyright © 2026 SiriZhao. All rights reserved.

> 本软件用于文本格式清理、结构整理和文档排版，不提供规避 AI 检测、绕过查重或实施学术不端的功能。
