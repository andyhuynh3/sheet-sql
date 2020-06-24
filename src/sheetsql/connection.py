import gspread
from gspread.exceptions import GSpreadException

from .spreadsheet import Spreadsheet


class GoogleSheetsConnection:
    def __init__(self, auth_type: str = "service_account", **kwargs) -> None:

        auth = {"oauth": gspread.oauth, "service_account": gspread.service_account}

        if auth_type not in auth:
            raise GSpreadException(
                f"{auth_type} is not a supported authentication type "
                f"(supported types are: {auth.keys()}"
            )
        self._gc = auth[auth_type](**kwargs)
        self._spreadsheets = {
            spreadsheet["id"]: Spreadsheet(self._gc, {"id": spreadsheet["id"]})
            for spreadsheet in self._gc.list_spreadsheet_files()
        }

    @property
    def spreadsheets(self) -> list:
        """Lists the spreadsheets the authorized user has access to"""
        return list(self._spreadsheets.values())

    def get_spreadsheet(self, spreadsheet_id: str) -> Spreadsheet:
        """Get a specific spreadsheet by its ID"""
        return self._spreadsheets[spreadsheet_id]

    def __getitem__(self, spreadsheet_id: str) -> Spreadsheet:
        """Make spreadsheets subscriptable"""
        return self.get_spreadsheet(spreadsheet_id)

    def __len__(self):
        return len(self._spreadsheets)
