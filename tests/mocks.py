"""Mocks for testing the sheetsql package."""

from sheetsql.connection import GoogleSheetsConnection
from sheetsql.spreadsheet import Spreadsheet
from sheetsql.worksheet import Worksheet


class MockGoogleSheetsConnection(GoogleSheetsConnection):
    """Mock GoogleSheetsConnections class.

    Args:
        spreadsheets (dict): test spreadsheets data
    """

    __slots__ = ("_spreadsheets",)

    def __init__(self, spreadsheets: dict) -> None:
        """Init method for MockGoogleSheetsConnection."""
        self._spreadsheets = spreadsheets


class MockSpreadsheet(Spreadsheet):
    """Mock Spreadsheet class.

    Args:
        worksheets (dict): test worksheets data
    """

    __slots__ = ("_worksheets",)

    def __init__(self, worksheets: dict) -> None:
        """Init method for MockSpreadsheet."""
        self._worksheets = worksheets


class MockWorksheet(Worksheet):
    """Mock Worksheet class."""

    __slots__ = ("_default_row_type",)

    def __init__(self) -> None:
        """Init method for MockWorksheet."""
        self._default_row_type = dict
