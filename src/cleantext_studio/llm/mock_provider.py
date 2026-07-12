from .base import LLMProvider
from .models import OptimizationMode
from .schemas import BlockType, OptimizationMetadata, OptimizationResponse, OptimizedBlock


class MockProvider(LLMProvider):
    def test_connection(self) -> None:
        return None

    def list_models(self) -> list[str]:
        return ["mock-model"]

    def optimize_document(
        self, text: str, mode: OptimizationMode, custom_task: str = ""
    ) -> OptimizationResponse:
        return OptimizationResponse(
            blocks=[
                OptimizedBlock(
                    block_id="b0",
                    block_type=BlockType.PARAGRAPH,
                    text=text,
                    list_level=None,
                    list_marker=None,
                    source_block_ids=["b0"],
                    change_type="unchanged",
                    change_reason="mock",
                    confidence=1,
                )
            ],
            metadata=OptimizationMetadata(language="zh", document_type="document"),
        )
