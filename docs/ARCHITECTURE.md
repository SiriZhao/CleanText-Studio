# 架构

管线依次执行 Unicode/HTML 修复、换行规范化、代码和表格保护、标题/列表/引用识别、Markdown/Emoji/分隔线清洗、碎片合并、残留检测和统计。`TextBlock` 保存类型、原位置和修改状态；`DocumentSession` 区分原文、本地结果、编辑结果和导出状态。GUI 仅调度 `QThread`，结果经 Signal 返回，工作线程不访问 UI。文件导入、清洗、模板验证和原子 DOCX 导出保持分层。

可选 AI 层位于 `llm/`：UI 只依赖 `LLMProvider`，Provider 负责 SDK 映射和统一异常；Prompt 使用资源文件，输出经 JSON/Pydantic 校验。发送前执行规模估算和敏感信息扫描，密钥由 CredentialStore 交给系统凭据库。AI Worker 与本地 Worker 分离，AI 建议必须经差异确认才写入编辑结果。

v1.1.1 使用 `ProviderPreset` 统一 Provider 默认地址和模型建议；`ParagraphLayoutEngine` 根据 TextBlock 连接正文；`BoilerplatePhraseCleaner` 从 JSON 资源加载首尾规则；`SystemThemeWatcher` 低频读取可替换的系统主题 reader；`FontManager` 只选择系统已安装字体；所有控件颜色、圆角和间距由 DesignToken 集中生成。
