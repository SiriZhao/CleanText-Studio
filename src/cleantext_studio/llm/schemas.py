from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class BlockType(StrEnum):
    TITLE = "title"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    QUOTE = "quote"
    CODE = "code"
    TABLE = "table"
    ABSTRACT = "abstract"
    KEYWORDS = "keywords"
    REFERENCES_HEADING = "references_heading"
    REFERENCE_ITEM = "reference_item"


class OptimizedBlock(BaseModel):
    block_id: str = Field(min_length=1, max_length=100)
    block_type: BlockType
    text: str = Field(max_length=200_000)
    list_level: int | None = Field(None, ge=0, le=10)
    list_marker: str | None = Field(None, max_length=20)
    source_block_ids: list[str] = Field(min_length=1, max_length=100)
    change_type: str = Field(max_length=80)
    change_reason: str = Field(max_length=500)
    confidence: float = Field(ge=0, le=1)


class OptimizationMetadata(BaseModel):
    language: str = Field(max_length=30)
    document_type: str = Field(max_length=80)
    warnings: list[str] = Field(default_factory=list, max_length=100)
    facts_added: bool = False
    facts_removed: bool = False
    references_changed: bool = False


class OptimizationResponse(BaseModel):
    schema_version: str = "1.0"
    blocks: list[OptimizedBlock] = Field(max_length=20_000)
    metadata: OptimizationMetadata

    @model_validator(mode="after")
    def unique_blocks(self) -> "OptimizationResponse":
        ids = [block.block_id for block in self.blocks]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate block_id")
        return self
