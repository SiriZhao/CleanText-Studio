# 发布

更新 `src/cleantext_studio/version.py` 和 CHANGELOG，运行全部检查及 `scripts/build_windows.ps1`，检查 ZIP/Setup/SHA256，提交后创建并推送对应 `v*` 标签。Release workflow 校验并在 Windows runner 安装 Inno Setup、重跑测试、构建和发布附件。下载后应复核 SHA256 和无 Python 环境启动。
