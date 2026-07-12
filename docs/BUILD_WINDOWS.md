# Windows 构建

在 Windows 10/11、Python 3.12 PowerShell 中运行 `./scripts/build_windows.ps1`。脚本创建虚拟环境、检查代码、测试、用 PyInstaller onedir 构建、打包 ZIP、调用 Inno Setup 并生成 SHA256。v1.1.0 构建会收集 OpenAI、Anthropic、httpx、keyring Windows 后端、certifi 和 Prompt 资源。Qt 启动失败时检查 `platforms/qwindows.dll`；AI Prompt 应位于 `_internal/cleantext_studio/llm/prompts`。路径含中文和空格受支持。
