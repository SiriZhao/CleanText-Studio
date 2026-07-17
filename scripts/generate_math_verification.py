from __future__ import annotations

import json
from pathlib import Path

from audit_docx_math import audit

from cleantext_studio.cleaners import clean_text
from cleantext_studio.exporters.files import DocxRenderer

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "math" / "math-index-v1.5.2.md"
OUTPUT = ROOT / "dist" / "verification" / "math-v1.5.2"


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source = FIXTURE.read_text(encoding="utf-8")
    result = clean_text(source)
    renderer = DocxRenderer()
    document = renderer.render(result.blocks)
    target = OUTPUT / "math-index-cleaned.docx"
    document.save(target)
    (OUTPUT / "math-index-input.md").write_text(source, encoding="utf-8")
    audit_report = audit(target)
    report = {
        "formulas_detected": result.stats.formulas_detected,
        "native_omml": renderer.formulas_as_omml,
        "image_fallback": 0,
        "unicode_fallback": renderer.formulas_as_text,
        "source_fallback": 0,
        "docx_audit": audit_report,
    }
    (OUTPUT / "formula-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUTPUT / "document-xml-audit.txt").write_text(
        json.dumps(audit_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if audit_report["passed"] and renderer.formulas_as_text == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
