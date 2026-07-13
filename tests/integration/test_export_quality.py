from cleantext_studio.cleaners import clean_text
from cleantext_studio.exporters import DocxRenderer, evaluate_export_quality


def test_export_quality_reports_actual_native_formula_outcome() -> None:
    result = clean_text("正文 \\( O \\)。\n\n\\[\\frac{a}{b}\\]")
    renderer = DocxRenderer()
    renderer.render(result.blocks)
    quality = evaluate_export_quality(result.blocks, renderer)
    assert quality.native_formulas == 2
    assert quality.fallback_formulas == 0
    assert quality.level == "优秀"
