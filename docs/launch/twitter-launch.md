# X / Twitter launch thread

Use the repository URL in the final post. Adjust character count before
publishing if the platform changes its limits.

1. **The problem**
   Copying an AI-assisted draft into Word can turn a good document into a manual cleanup job: Markdown residue, uneven paragraphs, lists, tables, and formulas all need repair.

2. **Why existing workflows fail**
   Plain-text cleanup can erase structure. Cloud tools can add an unnecessary data boundary. A good handoff needs to preserve the parts that make a document editable.

3. **Introducing CleanText Studio**
   CleanText Studio is a privacy-first, local-first Windows app for cleaning copied and AI-assisted text into structured DOCX or TXT documents. Open source: https://github.com/SiriZhao/CleanText-Studio

4. **What it preserves**
   Headings, lists, links, Markdown tables, paragraph intent, and a supported LaTeX subset. Review in Text or Preview mode before exporting.

5. **Formula support**
   Supported LaTeX is detected as a structured run and can be exported as editable Word OMML—not just pasted as visible source.

6. **Privacy boundary**
   Normal cleanup and export run locally. AI refinement is optional and uses a provider/API key the user configures. There is no shared project key.

7. **Technical stack**
   Python + PySide6, structured document blocks, DOCX generation, regression tests, Ruff, MyPy, and a Windows CI pipeline.

8. **Screenshots**
   The repository includes real application captures and a short workflow GIF: source text → cleanup controls → structured result → export.

9. **Roadmap**
   v1.5 establishes multilingual UI, formula handling, and Word export. Future exploration includes additional desktop platforms, more providers, and plugin research—only when implemented and tested.

10. **Invitation**
    If a local document-cleanup workflow is useful to you, try it, report a reproducible edge case, review a translation, or contribute a focused test. A Star is appreciated, never expected.
