"""Test setup."""

import pytest

from .mocks import MockGoogleSheetsConnection, MockSpreadsheet, MockWorksheet

spreadsheet_1_worksheets_data = {
    "worksheet_1": MockWorksheet(),
    "worksheet_2": MockWorksheet(),
}

spreadsheet_2_worksheets_data = {
    "worksheet_1": MockWorksheet(),
    "worksheet_2": MockWorksheet(),
    "worksheet_3": MockWorksheet(),
}

spreadsheets_data = {
    "spreadsheet_1": MockSpreadsheet(worksheets=spreadsheet_1_worksheets_data),
    "spreadsheet_2": MockSpreadsheet(worksheets=spreadsheet_2_worksheets_data),
}


@pytest.fixture
def worksheet() -> MockWorksheet:
    """Fixture for a mock Worksheet."""
    return MockWorksheet()


@pytest.fixture
def spreadsheet_1_worksheets() -> dict:
    """Fixture for spreadsheet_1_worksheets_data."""
    return spreadsheet_1_worksheets_data


@pytest.fixture
def spreadsheet_2_worksheets() -> dict:
    """Fixture for spreadsheet_2_worksheets_data."""
    return spreadsheet_2_worksheets_data


@pytest.fixture
def spreadsheets() -> dict:
    """Fixture for spreadsheets_data."""
    return spreadsheets_data


@pytest.fixture
def conn() -> MockGoogleSheetsConnection:
    """Fixture for mock GoogleSheetsConnection."""
    return MockGoogleSheetsConnection(spreadsheets=spreadsheets_data)
