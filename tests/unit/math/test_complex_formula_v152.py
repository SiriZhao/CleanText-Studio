from __future__ import annotations

from lxml import etree

from cleantext_studio.cleaners import clean_text
from cleantext_studio.math import MathDetector, OMMLConverter, PreviewFormulaRenderer

FORMULAS = (
    r"\pi(x) \sim \frac{x}{\ln x}",
    r"e^{i\pi}+1=0",
    r"A=\pi r^2",
    r"\frac{d}{dx}e^x=e^x",
    r"P(A\cap B)=P(A)P(B)",
    r"y=\mathbf{w}^{\top}\mathbf{x}+b",
    r"\sigma(z)=\frac{1}{1+e^{-z}}",
    r"\mathcal{L}=-\sum_i y_i\log\hat{y}_i",
    r"\theta_{t+1}=\theta_t-\eta\nabla_\theta\mathcal{L}",
    r"(f*g)(t)=\int f(\tau)g(t-\tau)\,d\tau",
    r"\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V",
    r"\hat{x}=\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}",
    r"\alpha=\frac{e^2}{4\pi\varepsilon_0\hbar c}",
)


def test_complex_index_is_wholly_native_omml() -> None:
    converter = OMMLConverter()
    residues = (r"\frac", r"\mathbf", r"\mathcal", r"\text", r"\hat", r"\sqrt", r"\theta")
    for expression in FORMULAS:
        converted = converter.convert(expression)
        assert converted.converted, (expression, converted.warning)
        assert converted.element is not None
        xml = etree.tostring(converted.element, encoding="unicode")
        assert all(token not in xml for token in residues)


def test_bare_math_is_split_from_chinese_and_english_prose() -> None:
    detector = MathDetector()
    samples = (
        "梯度下降：\\theta_{t+1}=\\theta_t-\\eta\\nabla_\\theta\\mathcal{L}",
        "Sigmoid: \\sigma(z)=\\frac{1}{1+e^{-z}}",
        "模型使用 y=\\mathbf{w}^{\\top}\\mathbf{x}+b 进行预测。",
    )
    for sample in samples:
        regions = detector.detect_inline(sample)
        assert len(regions) == 1
        assert "\\" in regions[0].content
        assert not regions[0].content.startswith(("梯", "模", "Sigmoid"))


def test_bare_math_creates_text_and_math_runs_without_recleaning() -> None:
    result = clean_text("模型使用 y=\\mathbf{w}^{\\top}\\mathbf{x}+b 进行预测。")
    block = result.blocks[0]
    assert [run.type.value for run in block.runs] == ["text", "inline_math", "text"]
    math = block.runs[1].math
    assert math is not None
    converted = OMMLConverter().convert(math.expression_source)
    assert converted.converted
    assert PreviewFormulaRenderer().render(converted.ast)  # type: ignore[arg-type]
