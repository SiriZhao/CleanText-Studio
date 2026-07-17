# CleanText Studio v1.5.2

CleanText Studio v1.5.2 is a mathematics stability release. It recognises
bounded bare LaTeX embedded in prose, lists, and table cells, then converts the
whole formula through one safe AST into editable Word OMML.

## Highlights

- Adds native support for fractions, indexed roots, scripts, delimiters, math
  styles, accents, functions, n-ary operators, Greek symbols, and common
  matrix environments used by the complex formula index.
- Removes the partial-rendering path that could leave `\mathbf`, `\mathcal`,
  `\text`, `\hat`, or other supported commands as visible DOCX source.
- Separates Markdown ordered-list markers from Word's native numbering to
  prevent duplicate labels such as `1. 1.`.
- Uses the same AST for preview and DOCX rendering; the release verification
  document contains 15 native OMML runs and zero source fallback runs.

## Compatibility and privacy

- Non-math cleaning output remains protected by the v1.4.2 freeze baseline.
- Basic cleanup remains local. Optional AI optimization only calls a provider
  configured by the user.

## Windows packages

- **Setup** installs CleanText Studio for the current Windows user.
- **Portable** can be extracted and run without installation.

Verify a download with PowerShell:

```powershell
Get-FileHash .\CleanText-Studio-v1.5.2-Windows-x64-Portable.zip -Algorithm SHA256
```

## Known limits

- The supported LaTeX subset is deliberately safe. Unknown custom macros are
  preserved as a whole-formula fallback and are reported; v1.5.2's supported
  complex index has zero fallback formulae.
- This release provides Windows packages only. macOS, Linux, and Android
  packages are not currently published.
