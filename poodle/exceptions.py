"""
Exceptions for the Poodle Python SDK.
"""
from typing import Optional


class PoodleError(Exception):
    """Base exception for all Poodle-related errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        details: Optional[str] = None,
    ) -> None:
        """Initialize a PoodleError.

        Args:
            message: A human-readable error message.
            status_code: The HTTP status code from the API response.
            details: Additional error details from the API response's 'error' field.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details

    def __str__(self) -> str:
        """Return a string representation of the error."""
        base = self.message
        if self.status_code:
            base = f"[{self.status_code}] {base}"
        if self.details:
            base = f"{base} - Details: {self.details}"
        return base
