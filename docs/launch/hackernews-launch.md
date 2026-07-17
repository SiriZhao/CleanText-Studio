# Hacker News / Show HN

## Title

**Show HN: CleanText Studio – A local-first AI text cleanup and document formatting app**

## Submission text

I built CleanText Studio because copying drafts and reference material into
Word often turns structure into manual repair work: Markdown markers remain,
paragraphs fragment, tables flatten, and formulas become source text.

It is an MIT-licensed Windows desktop application written with Python and
PySide6. The ordinary cleanup, preview, and export path runs locally. It keeps
document blocks for headings, lists, links, and tables, and parses a supported
LaTeX subset into editable Word OMML equations. Optional AI refinement is BYOK
and explicitly initiated by the user.

The code, screenshots, release notes, tests, and Windows artifacts are here:
https://github.com/SiriZhao/CleanText-Studio

The parts I would most like feedback on are formula boundaries, the trade-offs
of a constrained LaTeX subset, DOCX interoperability, and the Windows desktop
packaging path.

## Reply guidance

- Answer implementation questions with links to code/tests, not marketing copy.
- State limitations plainly: unsupported custom LaTeX macros can fall back;
  macOS/Linux builds are not published.
- Do not ask for votes, Stars, or off-site amplification.
- Keep the discussion in the original submission rather than posting repeats.
