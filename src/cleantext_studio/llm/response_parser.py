import json
import re

from pydantic import ValidationError

from .exceptions import InvalidResponseError, SchemaValidationError
from .schemas import OptimizationResponse


def parse_response(value: str) -> OptimizationResponse:
    """Parse strict JSON, fenced JSON, or the first bounded JSON object without eval."""
    if not value or len(value) > 10_000_000:
        raise InvalidResponseError("Empty or oversized provider response")
    cleaned = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", value, flags=re.I)
    candidates = [cleaned]
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start >= 0 and end > start:
        candidates.append(cleaned[start : end + 1])
    data = None
    for candidate in candidates:
        try:
            data = json.loads(candidate)
            break
        except json.JSONDecodeError:
            continue
    if data is None:
        raise InvalidResponseError("Provider did not return valid JSON")
    try:
        return OptimizationResponse.model_validate(data)
    except ValidationError as exc:
        raise SchemaValidationError("Provider JSON did not match the required schema") from exc
