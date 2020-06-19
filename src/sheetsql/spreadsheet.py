from gspread import Client
from gspread import Spreadsheet as GSpreadSpreadsheet

from .worksheet import Worksheet


class Spreadsheet(GSpreadSpreadsheet):
    def __init__(self, client: Client, properties: dict):
        super().__init__(client, properties)
        spreadsheet_metadata = self.fetch_sheet_metadata()
        self._worksheets = {
            worksheet["properties"]["title"]: Worksheet(self, worksheet["properties"])
            for worksheet in spreadsheet_metadata["sheets"]
        }

    def __len__(self):
        """Return number of worksheets"""
        return len(self._worksheets)

    @property
    def worksheets(self):
        """Lists the worksheets in the current spreadsheet"""
        return list(self._worksheets.keys())

    def __getitem__(self, worksheet_name):
        """Make worksheets subscriptable"""
        return self.get_worksheet(worksheet_name)

    def get_worksheet(self, worksheet_name):
        """Get specific worksheet by name"""
        if worksheet_name not in self._worksheets:
            self._worksheets[worksheet_name] = self.worksheet(worksheet_name)
        return self._worksheets[worksheet_name]
