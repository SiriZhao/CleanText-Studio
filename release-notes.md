# CleanText Studio v1.5.1

CleanText Studio v1.5.1 is a focused maintenance release for the localized
About dialog. Product identity, developer information, licensing facts, and
the project address are now rendered as immutable facts rather than natural
language translations.

## Highlights

- Twelve interface locales keep CleanText Studio, SiriZhao, MIT License,
  v1.5.1, and the GitHub URL unchanged.
- The About dialog now displays the repository MIT LICENSE text directly.
- Basic cleanup remains local. Optional AI optimization only uses a provider
  and key that you configure.

## Windows packages

- **Setup** installs CleanText Studio for the current Windows user.
- **Portable** can be extracted and run without installation.

Verify a download with PowerShell:

```powershell
Get-FileHash .\CleanText-Studio-v1.5.1-Windows-x64-Portable.zip -Algorithm SHA256
```

## Known limits

- Formula conversion supports a practical LaTeX subset; unusual macros remain
  readable fallback text rather than being altered.
- This release provides Windows packages only. It does not claim macOS,
  Linux, Android, AI-detection evasion, or plagiarism-evasion support.
