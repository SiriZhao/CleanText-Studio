# Reddit launch plan

Read the current subreddit rules immediately before posting. Do not cross-post
verbatim, vote-manipulate, or post where self-promotion is disallowed. In
particular, r/programming has historically not accepted project promotion;
prefer a technical discussion only when its current rules allow it.

## r/opensource

**Title:** I built CleanText Studio, a local-first Windows app for turning messy copied text into structured DOCX/TXT

**Body:**

I maintain CleanText Studio, an MIT-licensed PySide6 desktop app for cleaning
copied and AI-assisted text without sending normal cleanup jobs to a server. It
tries to preserve headings, lists, links, Markdown tables, and a supported
LaTeX subset while exporting native Word tables and editable OMML equations.

The useful problem is document recovery: turning notes, copied pages, and
drafts into a document that can be edited instead of rebuilt by hand.

The repo includes a portable Windows build, installer, tests, and screenshots:
https://github.com/SiriZhao/CleanText-Studio

I would especially value feedback on the formula boundary cases, DOCX export,
and the contributor experience.

**First comment:**

The core path is local. AI refinement is optional and uses a provider/API key
the user chooses; there is no shared project key. I will keep the issue tracker
focused on reproducible examples and welcome small test cases.

## r/LocalLLaMA

**Title:** Local-first cleanup for AI-assisted drafts: CleanText Studio (open source, Windows)

**Body:**

When an LLM draft is copied into a document, the practical problem is often
formatting rather than generation: extra Markdown, broken paragraphs, list
markers, tables, and formulas. CleanText Studio is an open-source Windows app
that performs those cleanup/export steps locally. Optional AI refinement is
BYOK; standard cleanup does not require a model call.

It handles document structure, DOCX/TXT export, and a supported LaTeX-to-OMML
path for editable Word equations. Repository and source: https://github.com/SiriZhao/CleanText-Studio

I am posting this for technical feedback, not as a claim that it runs an LLM
locally or bypasses AI detection. What formula or document-boundary examples
would you use to test it?

**First comment:**

The implementation is Python/PySide6. A useful contribution is a small,
non-sensitive fixture that shows a formula, table, or paragraph edge case.

## r/artificial

**Title:** Open-source local-first document cleanup for AI-assisted text

**Body:**

CleanText Studio focuses on the handoff after an AI draft is produced: local
cleanup of formatting residue, recovery of headings/lists/tables, and DOCX/TXT
export. Optional AI improvement uses a user-configured provider; the normal
cleanup pipeline stays on-device.

The source, screenshots, and Windows builds are available at:
https://github.com/SiriZhao/CleanText-Studio

**First comment:**

Feedback on transparency, data handling language, and practical formatting
workflows is more useful than generic feature requests.

## r/Python

**Title:** CleanText Studio: an open-source PySide6 app for structured text cleanup and DOCX export

**Body:**

I am sharing a PySide6/Python desktop project for a familiar document problem:
copied text may contain Markdown residue, inconsistent paragraphs, tables, and
LaTeX that must survive a Word export. CleanText Studio uses a structured block
pipeline and a tested LaTeX subset that can emit native OMML equations.

Repo: https://github.com/SiriZhao/CleanText-Studio

The repository has Ruff, MyPy, pytest, localization checks, and regression
fixtures. I would welcome review of the packaging, Qt architecture, or tests.

**First comment:**

Please check r/Python's current showcase/self-promotion policy first. If a
project post is not permitted, share a narrowly scoped technical question or
contribute through the issue tracker instead.

## r/Productivity

**Title:** A local desktop workflow for cleaning copied text before exporting to Word

**Body:**

CleanText Studio is a privacy-first Windows tool for turning copied and
AI-assisted text into a clean document. Paste text, choose cleanup rules,
review the result, then export DOCX or TXT. It preserves useful headings,
lists, tables, links, and supported equations instead of stripping everything.

Normal cleanup is local; AI enhancement is optional and user-configured.
Source and releases: https://github.com/SiriZhao/CleanText-Studio

**First comment:**

The best feedback is about repeatable daily workflows: which copied-text mess
costs you the most time, and what should a local tool preserve?

## r/programming

Do **not** use a project announcement unless the current rules explicitly
permit it. A safer route is to participate in relevant technical threads and
share the repository only when it directly answers the question.
