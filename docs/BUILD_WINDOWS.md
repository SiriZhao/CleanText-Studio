# Windows 构建

在 Windows 10/11、Python 3.12 PowerShell 中运行 `./scripts/build_windows.ps1`。脚本创建虚拟环境、检查代码、测试、用 PyInstaller onedir 构建、打包 ZIP、尝试调用 Inno Setup 并生成 SHA256。Qt 启动失败时检查 `platforms/qwindows.dll`。路径含中文和空格受支持，仍建议使用短构建路径减少旧工具长路径问题。

