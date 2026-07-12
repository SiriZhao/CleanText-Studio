# Changelog

## 1.1.0 - 2026-07-12

### Added

- 用户自带 API 的可选智能优化，支持 OpenAI、DeepSeek、Anthropic、OpenAI 兼容和本地兼容接口。
- Windows Credential Manager 密钥存储、结构化输出与 Schema 校验。
- 结构感知分块、请求规模估算、敏感信息发送前提醒、取消和统一错误模型。
- AI 发送前确认及本地结果/AI 建议差异确认。

### Changed

- 配置增加 Provider 元数据，配置文件和导出内容不包含 API Key。
- 主界面结果区增加独立 AI 智能优化步骤；本地清洗仍可完全离线使用。

### Security

- API Key 不以明文写入普通配置或日志。
- 模型输出必须通过 JSON 与 Pydantic Schema 校验，文档内指令仅视为数据。

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
