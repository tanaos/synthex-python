from typing import Optional


class SynthexError(Exception):
    """Base exception for all errors raised by the API wrapper."""
    
    def __init__(
        self, message: str, status_code: Optional[int] = None, 
        endpoint: Optional[str] = None, details: Optional[str] = None
    ):
        self.message = message
        self.status_code = status_code
        self.endpoint = endpoint
        self.details = details
        super().__init__(self.__str__())

    def __str__(self):
        parts = [f"[{self.status_code}] {self.message}"]
        if self.endpoint:
            parts.append(f"(Endpoint: {self.endpoint})")
        if self.details:
            parts.append(f"Details: {self.details}")
        return " ".join(parts)


class AuthenticationError(SynthexError):
    """Raised when authentication fails (e.g., invalid API key)."""
    pass


class RateLimitError(SynthexError):
    """Raised when the API rate limit is exceeded."""
    pass


class NotFoundError(SynthexError):
    """Raised when the requested resource is not found."""
    pass


class ServerError(SynthexError):
    """Raised when the API server returns a 5xx error."""
    pass

class ValidationError(SynthexError):
    """Raised when the API returns a validation error."""
    pass

class ConfigurationError(SynthexError):
    """Raised when the configuration, or parts of it, is missing or malformed."""
    pass
