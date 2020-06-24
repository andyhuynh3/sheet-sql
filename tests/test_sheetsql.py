from collections import OrderedDict

import mock
import pytest
from gspread.exceptions import GSpreadException
from sheetsql import connect
from sheetsql.exceptions import InvalidQueryException
from sheetsql.utils import handle_tq_response, parse_json_from_tq_response


class TestUtils:
    def test_parse_json_from_tq_response(self):
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

    def test_valid_handle_tq_response(self):
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

    def test_invalid_handle_tq_response(self):
        response = mock.Mock()
        with open("tests/sample_response/invalid_query_response.txt") as f:
            type(response).text = mock.PropertyMock(return_value=f.read())
        with pytest.raises(InvalidQueryException):
            handle_tq_response(response)


class TestGoogleSheetsConnection:
    def test_spreadsheets_property(self, conn, spreadsheets):
        assert set(conn.spreadsheets) == set(spreadsheets.values())

    def test_get_spreadsheet(self, conn, spreadsheets):
        assert conn.get_spreadsheet("spreadsheet_1") == spreadsheets["spreadsheet_1"]
        assert conn.get_spreadsheet("spreadsheet_2") == spreadsheets["spreadsheet_2"]
        with pytest.raises(KeyError):
            conn.get_spreadsheet("spreadsheet_3")

    def test_getitem_dunder(self, conn, spreadsheets):
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

    def test_len_dunder(self, conn, spreadsheets):
        return len(conn) == len(spreadsheets) == 2

    def test_conn_invalid_auth_type(self):
        with pytest.raises(GSpreadException):
            connect("unsupported_auth")

    @mock.patch("src.sheetsql.connection.gspread.oauth")
    @mock.patch("src.sheetsql.connection.gspread.service_account")
    def test_auth_called(self, mock_service_account, mock_gspread_oauth):
        mock_gspread_oauth.return_value = mock.MagicMock()
        mock_service_account.return_value = mock.MagicMock()
        connect("oauth")
        mock_gspread_oauth.assert_called_once()
        connect("service_account")
        mock_service_account.assert_called_once()


class TestSpreadsheet:
    def test_worksheets_property(
        self, conn, spreadsheet_1_worksheets, spreadsheet_2_worksheets
    ):
        assert conn["spreadsheet_1"].worksheets == list(spreadsheet_1_worksheets.keys())
        assert conn["spreadsheet_2"].worksheets == list(spreadsheet_2_worksheets.keys())

    def test_get_worksheet(
        self, conn, spreadsheet_1_worksheets, spreadsheet_2_worksheets
    ):
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
        self, conn, spreadsheet_1_worksheets, spreadsheet_2_worksheets
    ):
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

    def test_len_dunder(self, conn, spreadsheet_1_worksheets, spreadsheet_2_worksheets):
        assert len(conn["spreadsheet_1"]) == len(spreadsheet_1_worksheets) == 2
        assert len(conn["spreadsheet_2"]) == len(spreadsheet_2_worksheets) == 3


class TestWorksheet:
    @mock.patch("src.sheetsql.worksheet.GSpreadWorksheet.row_values")
    def test_columns_property(self, mock_row_values, worksheet):
        mock_row_values.return_value = ["test1", "test2", "test3"]
        assert worksheet.columns == ["test1", "test2", "test3"]

    @mock.patch("src.sheetsql.worksheet.GSpreadWorksheet.row_values")
    def test_num_columns_property(self, mock_row_values, worksheet):
        mock_row_values.return_value = ["test1", "test2", "test3"]
        assert worksheet.num_columns == 3

    def test_default_row_type_property(self, worksheet):
        assert worksheet.default_row_type == dict
        worksheet.default_row_type = list
        assert worksheet.default_row_type == list
        worksheet.default_row_type = tuple
        assert worksheet.default_row_type == tuple

    @mock.patch("src.sheetsql.worksheet.GSpreadWorksheet.row_values")
    def test_column_label_id_map_property(self, mock_row_values, worksheet):
        mock_row_values.return_value = ["test1", "test2", "test3"]
        assert worksheet.column_label_id_map == {
            "test1": "A",
            "test2": "B",
            "test3": "C",
        }

    @mock.patch("requests.get")
    def test_query(self, mock_request_get, worksheet):
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
