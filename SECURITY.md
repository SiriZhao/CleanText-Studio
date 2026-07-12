# Security

Please report vulnerabilities privately through GitHub Security Advisories. Do not include private documents. The application makes no network requests, stores no telemetry, limits selected imports, and never logs full user text.

Optional BYOK AI requests are user initiated. Credentials use the operating-system credential store, authentication headers and full request/response bodies are excluded from logs, endpoints require HTTPS except loopback hosts, and model output is treated as untrusted data validated by Pydantic. The application exposes no shell, filesystem, browser, tool-calling, or agent loop to models.
