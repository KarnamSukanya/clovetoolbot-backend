import gspread
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials


# -----------------------------------
# Google Sheets Authentication
# -----------------------------------

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "google_credentials.json",
    scope
)

client = gspread.authorize(credentials)


# -----------------------------------
# Load Google Sheet
# -----------------------------------

SHEET_URL = "https://docs.google.com/spreadsheets/d/1c3su-6-atPtpjCQhQvKRq5nyzrTCxFM7t4LVLhyIOsM/edit#gid=0"


def load_tools_sheet():

    sheet = client.open_by_url(
        SHEET_URL
    )

    worksheet = sheet.sheet1

    records = worksheet.get_all_records()

    df = pd.DataFrame(records)

    return df