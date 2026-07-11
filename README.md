# 净文排版 CleanText Studio

CleanText Studio v1.0.0 是一款完全离线、本地优先的 Windows 文本格式清洗与 Word 排版工具。支持粘贴或导入 TXT、Markdown、DOCX，清理 Markdown、Emoji、装饰符号和碎片换行，并导出 TXT 或 DOCX。

> 本软件用于清理文本格式和规范文档排版，不提供规避 AI 检测、学术不端或绕过查重的功能。

## 功能

- 结构感知的中英文碎片换行合并，保护标题、列表、代码和表格
- Markdown、Emoji、空白和 Unicode 修复
- 可编辑结果、撤销恢复、修改统计、后台处理
- TXT 编码识别及 DOCX 导入；原子写入 DOCX，中文字体和页码字段
- 无账户、无网络请求、无遥测

## 开发与运行

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
.\.venv\Scripts\python -m cleantext_studio.main
pytest
```

Windows 构建见 [docs/BUILD_WINDOWS.md](docs/BUILD_WINDOWS.md)，用户说明见 [docs/USER_GUIDE.md](docs/USER_GUIDE.md)。截图需由真实构建运行后添加，仓库不使用虚假界面图。

## 已知限制

首版不处理 DOCX 图片或复杂原始样式；目录域需在 Word 中更新；超长文本差异视图仅提供修改日志与一键恢复。

MIT License。详见 [LICENSE](LICENSE)。英文说明见 [README_EN.md](README_EN.md)。

