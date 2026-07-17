# Math rendering audit — v1.5.2

## Reproduction

The supplied Word document exposed two independent defects:

1. The inline protector recognised only `$...$` and `\(...\)`.  Bare expressions such as `P(A\cap B)=P(A)P(B)` and Chinese-label-plus-LaTeX lines never became `MathRun` values, so the DOCX renderer wrote their source as ordinary text.
2. Ordered Markdown list markers could remain in `TextBlock.text` while the exporter also selected Word's `List Number` style.  Word consequently displayed duplicate markers such as `1. 1.`.

## Corrected pipeline

`input → MathDetector → MathProtector → MathRun/InlineRun → FormulaParser AST → WordOMMLRenderer → DOCX`

The detector now protects explicit delimiters first and detects bounded bare formula candidates only when they contain an equation/relation or recognised math command.  URLs, Windows paths, code-like text and currency continue to be rejected.  It emits separate text and math runs, preserving Chinese and English labels around the formula.

The parser constructs one AST for the full run.  It supports fractions, indexed roots, scripts, `\left...\right`, style commands, text/operator names, accents, Greek and relation symbols, integrals/sums/products/limits, and supported matrix environments.  Preview and Word conversion both use that AST.  A supported formula is emitted entirely as OMML; it is not partly converted and partly appended as raw source.

## Required index

The v1.5.2 fixture contains the thirteen reported formulae in a numbered list, an un-delimited Chinese prose line, and a table cell.  `scripts/generate_math_verification.py` produces the DOCX and XML report; `scripts/audit_docx_math.py` rejects source residues including `\frac`, `\mathbf`, `\mathcal`, `\text`, `\hat`, `\sqrt`, `\theta`, `\nabla`, `\varepsilon`, `\hbar`, and `\cap`.

## Fallback policy

The current safe subset produces native OMML.  Unsupported syntax follows a whole-formula fallback path and is counted by the export report; it is never combined with a partially rendered formula.  The v1.5.2 release fixture requires zero fallback formulae.
