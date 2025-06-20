# sheets_logger.py

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime

# Constants
SPREADSHEET_ID = "1MC1-8FrGRAcxnkQIyVZbFdGehyLG8cL-XmvsYO-Yd_4"
SHEET_RANGE = "Sheet1!A1"
CREDS_FILE = "nova-sniper-26df1ca182f9.json"

async def log_to_google_sheets(token_address):
    creds = Credentials.from_service_account_file(
        CREDS_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    body = {
        "values": [[now, token_address]]
    }

    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_RANGE,
        valueInputOption="RAW",
        body=body
    ).execute()

    print(f"📄 Token logged to sheet: {token_address}")

