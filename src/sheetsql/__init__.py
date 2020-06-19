from .connection import GoogleSheetsConnection


def connect(auth_type: str, **kwargs):
    """Connect to Google Sheets via gspread by specifying either
    oauth or service_account as the auth_type.
    """
    return GoogleSheetsConnection(auth_type, **kwargs)
