class LLMError(Exception):
    """Base error safe to display without provider secrets."""


class AuthenticationError(LLMError):
    pass


class PermissionDeniedError(LLMError):
    pass


class ModelNotFoundError(LLMError):
    pass


class RateLimitError(LLMError):
    pass


class RequestTimeoutError(LLMError):
    pass


class NetworkError(LLMError):
    pass


class ProviderServerError(LLMError):
    pass


class InvalidResponseError(LLMError):
    pass


class SchemaValidationError(LLMError):
    pass


class ContentRejectedError(LLMError):
    pass


class UserCancelledError(LLMError):
    pass
