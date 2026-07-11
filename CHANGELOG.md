# Changelog

## 1.0.1 - 2026-07-12

### Fixed

- 修复四级至六级、无空格、Tab、全角空格和全角井号 Markdown 标题残留。
- 修复标题与粗体标记嵌套、独立分隔线、列表符号和正文连接号混淆。
- 修复完整步骤句可能被错误合并及重复清洗继续改变文本。

### Changed

- 主界面重构为输入、清洗设置和结果三个区域，操作按钮归属对应面板。
- 改进浅色/深色主题、高 DPI 布局、列表处理方式、统计和错误状态。

### Added

- 清洗预设、三种列表处理模式、残留检测、结果过期及手动编辑状态。
- 会话状态模型和可折叠设置栏。

## 1.0.0 - 2026-07-11

- Initial local-first text cleaning, TXT/DOCX import and export, Windows GUI and packaging workflows.
