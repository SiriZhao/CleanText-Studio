# Changelog

## 1.3.0 - 2026-07-13

### Added

- LaTeX inline, display, and common environment recognition and protection.
- Unicode math, plain-equation confidence detection, equation numbers, warnings, and statistics.
- Editable native Word OMML export for fractions, roots, scripts, Greek symbols, and simple matrices.
- Offline lightweight math preview and table-cell formula export.

### Fixed

- Prevent Markdown cleanup from damaging formula asterisks, underscores, and LaTeX commands.
- Preserve display-math boundaries across paragraph layout modes.
- Avoid treating dollar prices as unclosed math.
- Fall back to original LaTeX when conversion is unsupported instead of failing DOCX export.

### Changed

- Math regions are protected before Markdown, whitespace, and paragraph processing.
- Document blocks now carry a unified MathBlockData payload.

## 1.2.2 - 2026-07-13

### Added

- 深度 Markdown 结构解析、教程式操作标签清理和三种上下文感知独立 URL 策略。
- 块感知清洗残留检测、实际修改记录、表格畸形行提示和 Word 导出前结构摘要。
- 标题、列表、表格、引用和代码共用的统一文档块元数据。

### Fixed

- 修复 `#1`、C# 和正文话题井号被误判或误合并。
- 修复独立分隔线、粗体、链接、脚注定义和复杂标题偶发残留。
- 修复代码块残留误报、有序列表被当作标题以及表格导出数据源不同步。
- 修复默认清洗错误删除教程 URL；独立 URL 现在默认保留。

### Changed

- 重构本地清洗 Pipeline、段落布局、统计和残留警告模型。
- 结果预览、清洗文本与 Word 导出共享同一组结构化文档块。

## 1.2.1 - 2026-07-12

### Fixed

- 修复 Markdown 标题、分隔线、强调标记和列表符号残留。
- 修复 AI 模板标签、文档边界聊天语句和教程型 URL 残留，同时保护正文内容与普通网址。
- 修复代码块在段落格式化阶段可能被插入额外空行。

### Changed

- 将清洗流程拆分为 Normalize、Markdown Parser、Structure Cleaner、AI Pattern Cleaner、URL Cleaner 和 Paragraph Formatter 阶段。
- 统一标题、普通段落、连续列表、代码及表格的空行输出，并增加 Markdown、AI 模板和空行清理统计。

## 1.2.0 - 2026-07-12

### Added

- Markdown 表格增强解析、结构化预览和真实 Word 表格导出。
- Word 导出效果提示、结构检测和导出完成文件夹入口。

### Fixed

- 修复 Word 导出表格内容丢失和复杂 Markdown 表格解析失败。

### Improved

- AI 配置模型刷新与接口状态、控件箭头、顶栏尺寸、Tooltip 和导出流程。

### Removed

- 删除不稳定的聊天套话清理功能及其规则、统计和测试。

## 1.1.1 - 2026-07-12

### Added

- 系统主题自动跟随及浅色、深色固定模式。
- 三种明确的段落换行模式。
- Provider 默认 Base URL、推荐模型和恢复默认功能。
- 开发者、版权、隐私和项目主页信息完整的关于页面。
- 新版浅色、深色、Provider、段落模式、结果和关于截图。

### Fixed

- 修复 DeepSeek 错误显示 OpenAI Base URL、提供商切换不更新模型建议。
- 修复离线聊天式套话清理对 Emoji、Markdown、前导空行和组合句无效。
- 修复段落模式语义不明确、下拉框箭头区域圆角和弹窗主题不一致。

### Changed

- 重构 ProviderPreset、ParagraphLayoutEngine、主题 watcher、字体回退和 DesignToken。
- 改进 API 配置窗口、控件状态、间距、圆角和主界面视觉层级。

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
