# Provider 开发

Provider 实现 `LLMProvider` 的连接测试、模型列表和文档优化接口。UI 不直接调用 SDK。所有异常转换为项目异常，认证和参数错误不重试，网络/超时/429/部分服务错误最多重试两次。响应必须经标准 JSON 解析和 `OptimizationResponse` 校验；禁止 `eval`、工具调用、Agent 循环或执行模型输出。

测试必须使用 `MockProvider` 或本地模拟 HTTP，不得在 CI 调用真实付费 API。新增 Provider 时补充请求映射、错误转换、取消、日志脱敏和配置导出测试。
