# 发布

更新单一项目版本和 CHANGELOG，运行全部检查及 `scripts/build_windows.ps1`，检查 ZIP/Setup/SHA256，提交后创建并推送 `v1.0.0` 标签。Release workflow 在 Windows runner 安装 Inno Setup、重跑测试并发布附件。下载后应复核 SHA256 和无 Python 环境启动。
