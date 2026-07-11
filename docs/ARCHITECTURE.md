# 架构

管线依次执行 Unicode/HTML 修复、换行规范化、代码和表格保护、标题/列表/引用识别、Markdown/Emoji/分隔线清洗、碎片合并、残留检测和统计。`TextBlock` 保存类型、原位置和修改状态；`DocumentSession` 区分原文、本地结果、编辑结果和导出状态。GUI 仅调度 `QThread`，结果经 Signal 返回，工作线程不访问 UI。文件导入、清洗、模板验证和原子 DOCX 导出保持分层。
