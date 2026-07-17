# CleanText Studio v1.5.0

CleanText Studio v1.5.0 focuses on a consistent local desktop experience: the
presentation layer now uses centralized localization, stable option values, a
local help dialog, and shared rounded-card theme primitives.

## Highlights

- Twelve interface locales are packaged as local JSON resources.
- Language changes are presentation-only: source text, cleaned results, stable
  options, and local processing are not re-run or cleared.
- Help, About, controls, placeholders, and dynamic status labels use the same
  localization service.
- Basic cleanup remains local. Optional AI optimization only uses a provider
  and key that you configure.

## Windows packages

- **Setup** installs CleanText Studio for the current Windows user.
- **Portable** can be extracted and run without installation.

Verify a download with PowerShell:

```powershell
Get-FileHash .\CleanText-Studio-v1.5.0-Windows-x64-Portable.zip -Algorithm SHA256
```

## Known limits

- Formula conversion supports a practical LaTeX subset; unusual macros remain
  readable fallback text rather than being altered.
- This release provides Windows packages only. It does not claim macOS,
  Linux, Android, AI-detection evasion, or plagiarism-evasion support.
