"""sheetsql package tests."""

from collections import OrderedDict

import mock
import pytest
from gspread.exceptions import GSpreadException

from sheetsql import connect
from sheetsql.exceptions import InvalidQueryException
from sheetsql.utils import handle_tq_response, parse_json_from_tq_response

from .mocks import MockGoogleSheetsConnection, MockWorksheet


class TestUtils:
    """Utility functions tests."""

    def test_parse_json_from_tq_response(self) -> None:
        """Tt parses the JSON for the table query response."""
        with open("tests/sample_response/valid_query_response.txt") as f:
            response_text = f.read()
            json_data = parse_json_from_tq_response(response_text)
            assert json_data == {
                "version": "0.6",
                "reqId": "0",
                "status": "ok",
                "sig": "1094779711",
                "table": {
                    "cols": [
                        {"id": "sum-A", "label": "sum test", "type": "number"},
                        {"id": "sum-B", "label": "sum test2", "type": "number"},
                    ],
                    "rows": [{"c": [{"v": 15.0}, {"v": 40.0}]}],
                    "parsedNumHeaders": 0,
                },
            }

    def test_valid_handle_tq_response(self) -> None:
        """It handles a valid table query response correctly."""
        response = mock.Mock()
        with open("tests/sample_response/valid_query_response.txt") as f:
            type(response).text = mock.PropertyMock(return_value=f.read())
        assert handle_tq_response(response) == {
            "cols": [
                {"id": "sum-A", "label": "sum test", "type": "number"},
                {"id": "sum-B", "label": "sum test2", "type": "number"},
            ],
            "rows": [{"c": [{"v": 15.0}, {"v": 40.0}]}],
            "parsedNumHeaders": 0,
        }

    def test_invalid_handle_tq_response(self) -> None:
        """It handles an invalid table query response correctly."""
        response = mock.Mock()
        with open("tests/sample_response/invalid_query_response.txt") as f:
            type(response).text = mock.PropertyMock(return_value=f.read())
        with pytest.raises(InvalidQueryException):
            handle_tq_response(response)


class TestGoogleSheetsConnection:
    """GoogleSpreadSheetsConnection class tests."""

    def test_spreadsheets_property(
        self, conn: MockGoogleSheetsConnection, spreadsheets: dict
    ) -> None:
        """It returns the available spreadsheets."""
        assert set(conn.spreadsheets) == set(spreadsheets.values())

    def test_get_spreadsheet(
        self, conn: MockGoogleSheetsConnection, spreadsheets: dict
    ) -> None:
        """It returns the correct spreadsheet."""
        assert conn.get_spreadsheet("spreadsheet_1") == spreadsheets["spreadsheet_1"]
        assert conn.get_spreadsheet("spreadsheet_2") == spreadsheets["spreadsheet_2"]
        with pytest.raises(KeyError):
            conn.get_spreadsheet("spreadsheet_3")

    def test_getitem_dunder(
        self, conn: MockGoogleSheetsConnection, spreadsheets: dict
    ) -> None:
        """It returns the correct spreadsheet via dictionary key access."""
        assert (
            conn["spreadsheet_1"]
            == conn.get_spreadsheet("spreadsheet_1")
            == spreadsheets["spreadsheet_1"]
        )
        assert (
            conn["spreadsheet_2"]
            == conn.get_spreadsheet("spreadsheet_2")
            == spreadsheets["spreadsheet_2"]
        )
        with pytest.raises(KeyError):
            conn["spreadsheet_3"]

    def test_len_dunder(
        self, conn: MockGoogleSheetsConnection, spreadsheets: dict
    ) -> None:
        """It returns the number of spreadsheets."""
        assert len(conn) == len(spreadsheets) == 2

    def test_conn_invalid_auth_type(self) -> None:
        """It raises an exception for invalid auth types."""
        with pytest.raises(GSpreadException):
            connect("unsupported_auth")

    @mock.patch("src.sheetsql.connection.gspread.oauth")
    @mock.patch("src.sheetsql.connection.gspread.service_account")
    def test_auth_called(
        self, mock_service_account: mock.Mock, mock_gspread_oauth: mock.Mock
    ) -> None:
        """It calls the gspread oauth and service_account methods."""
        mock_gspread_oauth.return_value = mock.MagicMock()
        mock_service_account.return_value = mock.MagicMock()
        connect("oauth")
        mock_gspread_oauth.assert_called_once()
        connect("service_account")
        mock_service_account.assert_called_once()


class TestSpreadsheet:
    """Spreadsheet class tests."""

    def test_worksheets_property(
        self,
        conn: MockGoogleSheetsConnection,
        spreadsheet_1_worksheets: dict,
        spreadsheet_2_worksheets: dict,
    ) -> None:
        """It returns the worksheets in a given spreadsheet."""
        assert conn["spreadsheet_1"].worksheets == list(spreadsheet_1_worksheets.keys())
        assert conn["spreadsheet_2"].worksheets == list(spreadsheet_2_worksheets.keys())

    def test_get_worksheet(
        self,
        conn: MockGoogleSheetsConnection,
        spreadsheet_1_worksheets: dict,
        spreadsheet_2_worksheets: dict,
    ) -> None:
        """It returns the correct worksheet."""
        assert (
            conn["spreadsheet_1"].get_worksheet("worksheet_1")
            == spreadsheet_1_worksheets["worksheet_1"]
        )
        assert (
            conn["spreadsheet_1"].get_worksheet("worksheet_2")
            == spreadsheet_1_worksheets["worksheet_2"]
        )
        assert (
            conn["spreadsheet_2"].get_worksheet("worksheet_1")
            == spreadsheet_2_worksheets["worksheet_1"]
        )
        assert (
            conn["spreadsheet_2"].get_worksheet("worksheet_2")
            == spreadsheet_2_worksheets["worksheet_2"]
        )
        assert (
            conn["spreadsheet_2"].get_worksheet("worksheet_3")
            == spreadsheet_2_worksheets["worksheet_3"]
        )
        with pytest.raises(KeyError):
            conn["spreadsheet_1"].get_worksheet("worksheet_3")

    def test_getitem_dunder(
        self,
        conn: MockGoogleSheetsConnection,
        spreadsheet_1_worksheets: dict,
        spreadsheet_2_worksheets: dict,
    ) -> None:
        """It returns the correct worksheet via dictionary key access."""
        assert (
            conn["spreadsheet_1"]["worksheet_1"]
            == spreadsheet_1_worksheets["worksheet_1"]
        )
        assert (
            conn["spreadsheet_1"]["worksheet_2"]
            == spreadsheet_1_worksheets["worksheet_2"]
        )
        assert (
            conn["spreadsheet_2"]["worksheet_1"]
            == spreadsheet_2_worksheets["worksheet_1"]
        )
        assert (
            conn["spreadsheet_2"]["worksheet_2"]
            == spreadsheet_2_worksheets["worksheet_2"]
        )
        assert (
            conn["spreadsheet_2"]["worksheet_3"]
            == spreadsheet_2_worksheets["worksheet_3"]
        )
        with pytest.raises(KeyError):
            conn["spreadsheet_1"]["worksheet_3"]

    def test_len_dunder(
        self,
        conn: MockGoogleSheetsConnection,
        spreadsheet_1_worksheets: dict,
        spreadsheet_2_worksheets: dict,
    ) -> None:
        """It returns the number of worksheets."""
        assert len(conn["spreadsheet_1"]) == len(spreadsheet_1_worksheets) == 2
        assert len(conn["spreadsheet_2"]) == len(spreadsheet_2_worksheets) == 3


class TestWorksheet:
    """Worksheet class tests."""

    @mock.patch("src.sheetsql.worksheet.GSpreadWorksheet.row_values")
    def test_columns_property(
        self, mock_row_values: mock.Mock, worksheet: MockWorksheet
    ) -> None:
        """It returns the columns in the worksheet."""
        mock_row_values.return_value = ["test1", "test2", "test3"]
        assert worksheet.columns == ["test1", "test2", "test3"]

    @mock.patch("src.sheetsql.worksheet.GSpreadWorksheet.row_values")
    def test_num_columns_property(
        self, mock_row_values: mock.Mock, worksheet: MockWorksheet
    ) -> None:
        """It returns the number of columns in the worksheet."""
        mock_row_values.return_value = ["test1", "test2", "test3"]
        assert worksheet.num_columns == 3

    def test_default_row_type_property(self, worksheet: MockWorksheet) -> None:
        """It returns the default row type property."""
        assert worksheet.default_row_type == dict
        worksheet.default_row_type = list
        assert worksheet.default_row_type == list
        worksheet.default_row_type = tuple
        assert worksheet.default_row_type == tuple

    @mock.patch("src.sheetsql.worksheet.GSpreadWorksheet.row_values")
    def test_column_label_id_map_property(
        self, mock_row_values: mock.Mock, worksheet: MockWorksheet
    ) -> None:
        """It maps the column labels to ids."""
        mock_row_values.return_value = ["test1", "test2", "test3"]
        assert worksheet.column_label_id_map == {
            "test1": "A",
            "test2": "B",
            "test3": "C",
        }

    @mock.patch("requests.get")
    def test_query(self, mock_request_get: mock.Mock, worksheet: MockWorksheet) -> None:
        """It queries the worksheet and returns results."""
        response = mock.MagicMock()
        worksheet.spreadsheet = mock.Mock()
        worksheet._properties = {"sheetId": "patched"}
        with open("tests/sample_response/valid_query_response.txt") as f:
            type(response).text = mock.PropertyMock(return_value=f.read())
        type(response).status_code = mock.PropertyMock(return_value=200)
        mock_request_get.return_value = response
        res = [row for row in worksheet.query("SELECT SUM(test), SUM(test3)")]
        assert res == [{"sum test": 15.0, "sum test2": 40.0}]
        mock_request_get.assert_called_once()
        worksheet.default_row_type = list
        res = [row for row in worksheet.query("SELECT SUM(test), SUM(test3)")]
        assert res == [[15.0, 40.0]]
        assert mock_request_get.call_count == 2
        worksheet.default_row_type = tuple
        res = [row for row in worksheet.query("SELECT SUM(test), SUM(test3)")]
        assert res == [(15.0, 40.0)]
        assert mock_request_get.call_count == 3
        worksheet.default_row_type = OrderedDict
        res = [row for row in worksheet.query("SELECT SUM(test), SUM(test3)")]
        print(res)
        assert res == [OrderedDict([("sum test", 15.0), ("sum test2", 40.0)])]
        assert mock_request_get.call_count == 4
