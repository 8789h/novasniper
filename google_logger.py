import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# Setup Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON", "nova-sniper-26df1ca182f9.json"),
    scope
)
client = gspread.authorize(creds)
sheet = client.open_by_url(os.getenv("GOOGLE_SHEET_URL")).sheet1

def log_trade(data):
    row = [
        data.get("type", ""),
        data.get("token", ""),
        data.get("entry_price", ""),
        data.get("amount", ""),
        data.get("timestamp", ""),
        data.get("status", "OPEN"),
        data.get("sell_multiple", ""),
        data.get("pnl", ""),
        data.get("current_price", "")
    ]
    try:
        sheet.append_row(row)
        print("📄 Logged to Google Sheets")
    except Exception as e:
        print(f"⚠️ Failed to log to Sheets: {e}")

