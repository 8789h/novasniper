import os
import base64
from datetime import datetime
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Load .env (optional for local dev) ===
load_dotenv()

# === Decode base64 creds from Railway env ===
b64_creds = os.getenv("GOOGLE_SHEETS_JSON")
if b64_creds:
    creds_path = "/tmp/credentials.json"
    with open(creds_path, "wb") as f:
        f.write(base64.b64decode(b64_creds))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
else:
    raise ValueError("Missing GOOGLE_SHEETS_JSON env variable")

# === Setup Google Sheets client ===
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SHEET_ID = os.getenv("SHEET_ID")

creds = ServiceAccountCredentials.from_json_keyfile_name(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], SCOPES)
client = gspread.authorize(creds)
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

