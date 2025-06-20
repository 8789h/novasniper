import os
import json
from datetime import datetime
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Load .env (optional for local dev) ===
load_dotenv()

# === Load Google Sheets credentials from raw JSON ===
raw_json = os.getenv("GOOGLE_SHEETS_JSON")
if not raw_json:
    raise ValueError("Missing GOOGLE_SHEETS_JSON env variable")

SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
info = json.loads(raw_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(info, SCOPES)
client = gspread.authorize(creds)

# === Setup target sheet ===
SHEET_ID = os.getenv("SHEET_ID")
sheet = client.open_by_key(SHEET_ID).sheet1

# === Log trade function ===
def log_trade(action, token, entry_price=None, current_price=None, pnl_pct=None, target=None, tx_id=None, token_address=None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [
        now,
        action,
        token,
        f"{entry_price:.2f}" if entry_price else "",
        f"{current_price:.2f}" if current_price else "",
        f"{pnl_pct:.2f}%" if pnl_pct else "",
        target or "",
        tx_id or "",
        token_address or ""
    ]

    sheet.append_row(row, value_input_option="USER_ENTERED")
    print(f"🧾 Logged trade: {row}")

