"""
Example script demonstrating how to use the Poodle Python SDK.
"""
import os
from poodle import PoodleClient, PoodleError

# Get API key from environment variable
api_key = os.getenv("POODLE_API_KEY")

# Initialize the client
client = PoodleClient(api_key)

# Example email content
html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { color: #333; font-size: 24px; }
        .content { margin: 20px 0; }
        .footer { color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">Welcome to Poodle!</div>
    <div class="content">
        <p>This is a test email sent using the Poodle Python SDK.</p>
        <p>Features:</p>
        <ul>
            <li>Easy to use</li>
            <li>Reliable delivery</li>
            <li>Great documentation</li>
        </ul>
    </div>
    <div class="footer">
        Sent via Poodle - The modern email sending platform
    </div>
</body>
</html>
"""

text_content = """
Welcome to Poodle!

This is a test email sent using the Poodle Python SDK.

Features:
- Easy to use
- Reliable delivery
- Great documentation

Sent via Poodle - The modern email sending platform
"""

try:
    # Send the email
    response = client.send_email(
        from_email="sender@yourdomain.com",  # Replace with your sender email
        to_email="recipient@example.com",  # Replace with recipient email
        subject="Welcome to Poodle!",
        html_content=html_content,
        text_content=text_content,
    )
    print(f"Success! {response['message']}")

except PoodleError as e:
    # Handle specific error cases
    print(f"An error occurred: {e.message}")
    if e.status_code:
        print(f"Status Code: {e.status_code}")
    if e.details:
        print(f"Error Details: {e.details}")

except Exception as e:
    print(f"Unexpected error: {e}")
