"""
Main client module for the Poodle Python SDK.
"""
from typing import Any, Dict, Optional
import requests

from poodle.exceptions import PoodleError
from poodle.version import __version__


class PoodleClient:
    """Client for interacting with the Poodle email sending API."""

    DEFAULT_BASE_URL = "https://api.usepoodle.com/v1"
    DEFAULT_TIMEOUT = 30.0  # seconds

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> None:
        """Initialize a new Poodle client.

        Args:
            api_key: Your Poodle API key.
            base_url: Optional custom API base URL. Defaults to production API.
            timeout: Optional custom timeout for API requests in seconds.
        """

        self.api_key = api_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout or self.DEFAULT_TIMEOUT

        # Create a session for connection pooling
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"poodle-python/{__version__}",
            }
        )

    def send_email(
        self,
        from_email: str,
        to_email: str,
        subject: str,
        html_content: Optional[str] = None,
        text_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send an email using the Poodle API.

        Args:
            from_email: The sender's email address.
            to_email: The recipient's email address.
            subject: The email subject line.
            html_content: Optional HTML content for the email.
            text_content: Optional plain text content for the email.

        Returns:
            Dict containing the API response with at least 'success' and
            'message' keys.

        Raises:
            PoodleError: If the API request fails or returns an error.
        """

        # Prepare request payload
        payload = {
            "from": from_email,
            "to": to_email,
            "subject": subject,
        }
        if html_content:
            payload["html"] = html_content
        if text_content:
            payload["text"] = text_content

        try:
            response = self.session.post(
                f"{self.base_url}/send-email",
                json=payload,
                timeout=self.timeout,
            )

            # Try to parse JSON response regardless of status code
            try:
                response_data = response.json()
            except requests.exceptions.JSONDecodeError:
                response_data = {}

            if not response.ok:
                # Ensure 'error' is treated as a string, or None if not present
                error_details = response_data.get("error")
                if not isinstance(error_details, (str, type(None))):
                    error_details = str(error_details)

                raise PoodleError(
                    message=response_data.get("message", "Unknown API error"),
                    status_code=response.status_code,
                    details=error_details,
                )

            return {
                "success": response_data.get("success", True),  # API returns this
                "message": response_data.get("message", "Email queued for sending"),
            }

        except requests.exceptions.Timeout:
            raise PoodleError(
                message="Request timed out",
                status_code=None,  # No HTTP status code for timeout
                details=None,  # Timeout doesn't have API error details
            )
        except requests.exceptions.RequestException:
            raise PoodleError(
                message="Network error",
                status_code=None,  # No HTTP status code for general network errors
                details=None,  # Network errors don't have API error details
            )

    def __enter__(self) -> "PoodleClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.session.close()
