"""Report likely user-facing literals that bypass the translation service."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).parents[1]
METHODS = {"setText", "setWindowTitle", "setPlaceholderText", "setToolTip", "addItem", "addAction"}
ALLOW = {"UTF-8", "TXT", "Word", "Markdown", "LaTeX", "API", "Base URL", "Temperature", "MIT License"}


def _audit(path: Path) -> list[str]:
    findings: list[str] = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        return [f"{path}: syntax error: {exc.msg}"]
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr not in METHODS or not node.args:
            continue
        literal = node.args[0]
        if (
            isinstance(literal, ast.Constant)
            and isinstance(literal.value, str)
            and literal.value.strip()
            and literal.value not in ALLOW
        ):
            findings.append(f"{path.relative_to(ROOT)}:{node.lineno}: {node.func.attr}({literal.value!r})")
    return findings


def main() -> int:
    findings = [item for path in (ROOT / "src").rglob("*.py") for item in _audit(path)]
    report = ROOT / "dist" / "verification" / "user-visible-string-audit.txt"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(findings) + ("\n" if findings else ""), encoding="utf-8")
    if findings:
        print(f"user-visible literal audit: {len(findings)} finding(s); see {report}")
        return 1
    print("user-visible literal audit OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
