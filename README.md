# poodle-python

Python SDK for Poodle's email sending API.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Installation

```bash
pip install poodle-python
```

## Quick Start

```python
from poodle import PoodleClient

# Initialize the client
client = PoodleClient("your-api-key")

# Send an email
try:
    response = client.send_email(
        from_email="sender@example.com",
        to_email="recipient@example.com",
        subject="Hello from Poodle!",
        html_content="<h1>Hello World</h1>",
        text_content="Hello World"  # Optional plain text version
    )
    print(f"Success: {response['message']}")
except PoodleError as e:
    print(f"Error: {e.message}")
    if e.status_code:
        print(f"Status Code: {e.status_code}")
    if e.details:
        print(f"Details: {e.details}")
```

## Features

- **Intuitive API**: Get started in minutes.
- **Detailed Errors**: Understand and debug issues quickly with PoodleError objects.
- **Flexible Content**: Send rich HTML or plain text emails easily.
- **Connection Pooling**: Optimize performance with connection pooling.
- **Type Hints**: Better IDE support with type hints.
- **Context Manager**: Proper resource cleanup with context manager.

## Examples

### Initialize with Custom Options

```python
client = PoodleClient(
    api_key="your-api-key",
    base_url="https://custom.api.url",  # Optional custom API URL
    timeout=60.0  # Optional custom timeout in seconds
)
```

### Send HTML-only Email

```python
response = client.send_email(
    from_email="sender@example.com",
    to_email="recipient@example.com",
    subject="HTML Email",
    html_content="<h1>Hello</h1><p>This is an HTML email</p>"
)
```

### Send Plain Text Email

```python
response = client.send_email(
    from_email="sender@example.com",
    to_email="recipient@example.com",
    subject="Plain Text Email",
    text_content="Hello! This is a plain text email."
)
```

### Using as Context Manager

```python
with PoodleClient("your-api-key") as client:
    response = client.send_email(
        from_email="sender@example.com",
        to_email="recipient@example.com",
        subject="Test Email",
        text_content="Hello World"
    )
```

### Error Handling

```python
try:
    response = client.send_email(...)
except PoodleError as e:
    print(f"An API Error occurred: {e.message}")
    if e.status_code == 429:  # Rate limit exceeded
        # The PoodleError __str__ method will format this nicely.
        # e.details will contain the specific error string from the API.
        print(str(e))
        if e.details:
            print(f"Rate limit details: {e.details}")
    elif e.status_code == 400:  # Validation error
        print(f"Validation error: {e.message}")
        if e.details:
            print(f"Validation details: {e.details}")
    elif e.status_code:
        print(f"Status Code: {e.status_code}")
        if e.details:
            print(f"Error details: {e.details}")
    else:
        # Network error or other non-HTTP error (e.details will be None)
        print(f"Error: {e}")
```

## API Reference

### PoodleClient

#### Constructor

```python
PoodleClient(
    api_key: str,
    base_url: Optional[str] = None,
    timeout: Optional[float] = None
)
```

- `api_key`: Your Poodle API key (required)
- `base_url`: Optional custom API base URL
- `timeout`: Optional custom timeout for API requests in seconds

#### Methods

##### send_email

```python
send_email(
    from_email: str,
    to_email: str,
    subject: str,
    html_content: Optional[str] = None,
    text_content: Optional[str] = None
) -> Dict[str, Any]
```

Sends an email using the Poodle API.

**Parameters:**

- `from_email`: The sender's email address
- `to_email`: The recipient's email address
- `subject`: The email subject line
- `html_content`: Optional HTML content for the email
- `text_content`: Optional plain text content for the email

**Returns:**
A dictionary containing at least:

- `success`: Boolean indicating success
- `message`: Success message from the API

**Raises:**

- `PoodleError`: If the API request fails or returns an error

### PoodleError

Custom exception class for Poodle-related errors.

**Attributes:**

- `message`: Human-readable error message (from API `message` field)
- `status_code`: HTTP status code from the API (if applicable)
- `details`: Optional string containing additional error details from the API (from API `error` field, or `None`)

## Development

### Setup Development Environment

1. Clone the repository:

```bash
git clone https://github.com/usepoodle/poodle-python.git
cd poodle-python
```

2. Install development dependencies:

```bash
pip install poetry
poetry install
```

### Running Tests

```bash
poetry run pytest
```

### Code Style

This project uses:

- Black for code formatting
- Flake8 for linting
- MyPy for type checking

To check code style:

```bash
poetry run black .
poetry run flake8
poetry run mypy poodle
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on the process for submitting pull requests and our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
