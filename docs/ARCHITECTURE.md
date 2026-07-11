# 架构

管线依次执行 Unicode/HTML 修复、换行规范化、代码和表格保护、块识别、Markdown/Emoji/空白清洗、碎片合并和统计。`TextBlock` 保存类型、原位置和修改状态。GUI 仅调度 `QThread`，结果经 Signal 返回，工作线程不访问 UI。文件导入、清洗、模板验证和原子 DOCX 导出保持分层。

