"""
Tests for the Poodle client.
"""
import pytest
import requests
from poodle import PoodleClient, PoodleError


def test_client_initialization():
    """Test client initialization with valid and invalid API keys."""
    # Test valid initialization
    client = PoodleClient("test-api-key")
    assert client.api_key == "test-api-key"
    assert client.base_url == PoodleClient.DEFAULT_BASE_URL
    assert client.timeout == PoodleClient.DEFAULT_TIMEOUT

    # Test custom base URL
    client = PoodleClient("test-api-key", base_url="https://custom.api.com")
    assert client.base_url == "https://custom.api.com"

    # Test custom timeout
    client = PoodleClient("test-api-key", timeout=60.0)
    assert client.timeout == 60.0


def test_send_email_success(mocker):
    """Test successful email sending."""
    mock_response = mocker.Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "success": True,
        "message": "Email queued for sending",
    }

    mock_post = mocker.patch("requests.Session.post", return_value=mock_response)

    client = PoodleClient("test-api-key")
    result = client.send_email(
        "from@example.com", "to@example.com", "Test Subject", text_content="Test body"
    )

    assert result["success"] is True
    assert result["message"] == "Email queued for sending"
    mock_post.assert_called_once()


def test_send_email_api_error_with_string_details(mocker):
    """Test API error handling when 'error' is a string."""
    mock_response = mocker.Mock()
    mock_response.ok = False
    mock_response.status_code = 400
    mock_response.content = True  # Indicate content is present
    mock_response.json.return_value = {
        "success": False,
        "message": "Invalid email format",
        "error": "The provided 'to' email address is not valid.",
    }

    mocker.patch("requests.Session.post", return_value=mock_response)

    client = PoodleClient("test-api-key")
    with pytest.raises(PoodleError) as exc_info:
        client.send_email(
            "from@example.com",
            "invalid-email",
            "Test Subject",
            text_content="Test body",
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "Invalid email format"
    assert exc_info.value.details == "The provided 'to' email address is not valid."
    assert "Details: The provided 'to' email address is not valid." in str(
        exc_info.value
    )


def test_send_email_api_error_no_json_content(mocker):
    """Test API error handling when response is not valid JSON."""
    mock_response = mocker.Mock()
    mock_response.ok = False
    mock_response.status_code = 500
    mock_response.content = True  # but not valid JSON
    # Configure json() to raise an error
    mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
        "Error", "doc", 0
    )

    mocker.patch("requests.Session.post", return_value=mock_response)

    client = PoodleClient("test-api-key")
    with pytest.raises(PoodleError) as exc_info:
        client.send_email(
            "from@example.com",
            "to@example.com",
            "Test Subject",
            text_content="Test body",
        )

    assert exc_info.value.status_code == 500
    assert exc_info.value.message == "Unknown API error"  # Default message
    assert exc_info.value.details is None


def test_send_email_api_error_missing_message_in_json(mocker):
    """Test API error with JSON but missing 'message' field."""
    mock_response = mocker.Mock()
    mock_response.ok = False
    mock_response.status_code = 403
    mock_response.content = True
    mock_response.json.return_value = {
        "success": False,
        # "message": "Forbidden", # Message is missing
        "error": "Permission denied",
    }

    mocker.patch("requests.Session.post", return_value=mock_response)

    client = PoodleClient("test-api-key")
    with pytest.raises(PoodleError) as exc_info:
        client.send_email(
            "from@example.com",
            "to@example.com",
            "Test Subject",
            text_content="Test body",
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.message == "Unknown API error"  # Falls back to default
    assert exc_info.value.details == "Permission denied"


def test_send_email_timeout_error(mocker):
    """Test timeout error handling."""
    mocker.patch(
        "requests.Session.post",
        side_effect=requests.exceptions.Timeout("Request timed out"),
    )

    client = PoodleClient("test-api-key", timeout=0.1)
    with pytest.raises(PoodleError) as exc_info:
        client.send_email(
            "from@example.com",
            "to@example.com",
            "Test Subject",
            text_content="Test body",
        )
    assert "Request timed out" in str(exc_info.value)
    assert exc_info.value.status_code is None
    assert exc_info.value.details is None


def test_send_email_network_error(mocker):
    """Test network error handling."""
    mocker.patch(
        "requests.Session.post",
        side_effect=requests.exceptions.ConnectionError("Connection failed"),
    )

    client = PoodleClient("test-api-key")
    with pytest.raises(PoodleError) as exc_info:
        client.send_email(
            "from@example.com",
            "to@example.com",
            "Test Subject",
            text_content="Test body",
        )

    assert "Network error" in str(exc_info.value)
    assert exc_info.value.status_code is None
    assert exc_info.value.details is None


def test_context_manager():
    """Test client as context manager."""
    with PoodleClient("test-api-key") as client:
        assert isinstance(client, PoodleClient)
