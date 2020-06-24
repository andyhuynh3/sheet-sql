from sheetsql.connection import GoogleSheetsConnection
from sheetsql.spreadsheet import Spreadsheet
from sheetsql.worksheet import Worksheet


class MockGoogleSheetsConnection(GoogleSheetsConnection):
    def __init__(self, spreadsheets):
        self._spreadsheets = spreadsheets


class MockSpreadsheet(Spreadsheet):
    def __init__(self, worksheets):
        self._worksheets = worksheets


class MockWorksheet(Worksheet):
    def __init__(self):
        self._default_row_type = dict
