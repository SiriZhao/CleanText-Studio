from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZipFile

LATEX_RESIDUES = (
    r"\frac",
    r"\mathbf",
    r"\mathcal",
    r"\text",
    r"\hat",
    r"\sqrt",
    r"\theta",
    r"\nabla",
    r"\varepsilon",
    r"\hbar",
    r"\cap",
)


def audit(path: Path) -> dict[str, object]:
    with ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    residues = [token for token in LATEX_RESIDUES if token in xml]
    return {
        "document": str(path),
        "native_math_nodes": xml.count("<m:oMath"),
        "fractions": xml.count("<m:f"),
        "radicals": xml.count("<m:rad"),
        "superscripts": xml.count("<m:sSup"),
        "subscripts": xml.count("<m:sSub"),
        "accents": xml.count("<m:acc"),
        "nary": xml.count("<m:nary"),
        "latex_residues": residues,
        "passed": not residues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit native Office Math XML in a DOCX file.")
    parser.add_argument("document", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit(args.document)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
