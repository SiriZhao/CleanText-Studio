from dataclasses import dataclass

from cleantext_studio.models import TextBlock, TextBlockType


@dataclass(slots=True, frozen=True)
class DocumentChunk:
    chunk_id: str
    text: str
    block_ids: tuple[str, ...]
    heading_context: str = ""


def chunk_blocks(
    blocks: list[TextBlock], target_size: int = 12_000, maximum: int = 50
) -> list[DocumentChunk]:
    """Split at block boundaries without cutting code, tables, URLs, or words."""
    if target_size < 500:
        raise ValueError("target_size must be at least 500")
    chunks: list[DocumentChunk] = []
    texts: list[str] = []
    ids: list[str] = []
    size = 0
    heading = ""
    for index, block in enumerate(blocks):
        block_id = f"b{block.position}-{index}"
        if block.type in {
            TextBlockType.HEADING_1,
            TextBlockType.HEADING_2,
            TextBlockType.HEADING_3,
        }:
            heading = block.text
        addition = len(block.text) + 1
        if texts and size + addition > target_size:
            chunks.append(DocumentChunk(f"c{len(chunks)}", "\n".join(texts), tuple(ids), heading))
            texts, ids, size = [], [], 0
        texts.append(block.text)
        ids.append(block_id)
        size += addition
        if len(chunks) >= maximum:
            raise ValueError("Document exceeds maximum chunk count")
    if texts:
        chunks.append(DocumentChunk(f"c{len(chunks)}", "\n".join(texts), tuple(ids), heading))
    return chunks
