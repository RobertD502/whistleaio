""" Exceptions for Whistle Client """

from typing import Any

class WhistleAuthError(Exception):
    """ Authentication Error """

    def __init__(self, *args: Any) -> None:
        """Initialize the exception."""
        Exception.__init__(self, *args)