"""SQL for Google Sheets."""

__version__ = "0.1.0"

from typing import Any

from .connection import GoogleSheetsConnection


def connect(auth_type: str, **kwargs: Any) -> GoogleSheetsConnection:
    """Connect to Google Sheets via gspread oauth or service_account."""
    return GoogleSheetsConnection(auth_type, **kwargs)
