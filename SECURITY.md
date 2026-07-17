# Security policy

## Reporting a vulnerability

Please use [GitHub Security Advisories](https://github.com/SiriZhao/CleanText-Studio/security/advisories/new) for a private report. Do not include private documents, API keys, or credentials in a public issue.

Include a minimal reproduction, affected version, impact, and any safe mitigation you found. We will acknowledge a valid report and coordinate disclosure before publishing details.

## Security boundaries

- Basic cleanup and export run locally.
- Optional BYOK AI requests are explicitly user initiated.
- Credentials use the configured operating-system credential store when available and are not exported with document configuration.
- Provider responses are treated as untrusted data; the application does not expose shell, browser, tool-calling, or agent-loop access to them.

This project makes no absolute security guarantee. Keep your operating system, dependencies, and provider credentials up to date.
