# API 配置

AI 智能优化是可选功能。打开“设置”，新增配置名称、提供商、Base URL、Model 和自己的 API Key。支持 OpenAI、DeepSeek、Anthropic Claude、OpenAI 兼容接口及本地兼容模型。模型名可手动输入，不依赖远程模型列表。

Provider 变化会联动默认 Base URL 和推荐模型：OpenAI 使用 `https://api.openai.com/v1`，DeepSeek 使用 `https://api.deepseek.com`，Anthropic 使用 `https://api.anthropic.com`，本地兼容接口使用 `http://localhost:11434/v1`。自定义地址会保留，可点击“恢复默认”。模型可编辑，也可异步获取；失败不影响手动输入。

API Key 默认保存到 Windows Credential Manager，也可选择仅本次会话使用。配置 JSON 不包含密钥。HTTP 仅允许 localhost/127.0.0.1/::1，本地以外端点必须使用 HTTPS。测试连接可能产生少量用量，实际 Token 和费用以提供商账单为准。
