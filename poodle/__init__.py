"""
Poodle Python SDK - A client library for the Poodle email sending API.
"""

from poodle.client import PoodleClient
from poodle.exceptions import PoodleError
from poodle.version import __version__

__all__ = ["PoodleClient", "PoodleError", "__version__"]
