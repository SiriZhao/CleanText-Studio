from importlib.resources import files

from .models import OptimizationMode

FILES = {
    OptimizationMode.STRUCTURE: "structure.txt",
    OptimizationMode.LINE_BREAKS: "line_breaks.txt",
    OptimizationMode.LIGHT_CLEANUP: "light_cleanup.txt",
    OptimizationMode.LIST_NATURALIZATION: "list_to_paragraph.txt",
    OptimizationMode.ACADEMIC_STRUCTURE: "academic_structure.txt",
}


def build_messages(text: str, mode: OptimizationMode, custom_task: str = "") -> tuple[str, str]:
    root = files("cleantext_studio.llm").joinpath("prompts")
    system = root.joinpath("system_zh.txt").read_text(encoding="utf-8")
    task = (
        custom_task
        if mode == OptimizationMode.CUSTOM
        else root.joinpath(FILES[mode]).read_text(encoding="utf-8")
    )
    user = f"{task}\n<document_to_process>\n{text}\n</document_to_process>\n返回 OptimizationResponse JSON。"
    return system, user
