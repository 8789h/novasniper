import os
import json
import datetime
import base58
import gspread
from dotenv import load_dotenv
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.publickey import PublicKey
from solana.keypair import Keypair
from google.oauth2.service_account import Credentials

# === Load Google Sheets credentials from raw JSON env var ===
raw_json = os.getenv("GOOGLE_SHEETS_JSON")
if not raw_json:
    raise ValueError("Missing GOOGLE_SHEETS_JSON env variable")

info = json.loads(raw_json)
creds = Credentials.from_service_account_info(info)
gc = gspread.authorize(creds)

# === Load env vars ===
load_dotenv()
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PHANTOM_PUBLIC_KEY = os.getenv("PHANTOM_PUBLIC_KEY")
SHEET_ID = os.getenv("SHEET_ID")

# === Setup Solana client and wallet ===
client = Client(RPC_URL)
keypair = Keypair.from_secret_key(base58.b58decode(PRIVATE_KEY))
phantom_pubkey = PublicKey(PHANTOM_PUBLIC_KEY)

# === Google Sheets setup ===
sheet = gc.open_by_key(SHEET_ID).sheet1

# === SELL FUNCTION using market cap logic ===
def sell_fn(token_symbol, token_address, entry_marketcap, wallet_total_sol, initial_sol_amount):
    from get_market_cap import get_market_cap

    try:
        current_marketcap = get_market_cap(token_address)
        if not current_marketcap or not entry_marketcap:
            print(f"❌ Missing market cap data for {token_symbol}")
            return None

        ratio = current_marketcap / entry_marketcap
        targets_hit = []

        if ratio >= 2:
            targets_hit.append(("2x", 0.5))
        if ratio >= 3:
            targets_hit.append(("3x", 0.3))
        if ratio >= 5:
            targets_hit.append(("5x", 0.2))

        for label, percent in targets_hit:
            sell_amount = initial_sol_amount * percent
            lamports = int(sell_amount * 1_000_000_000)

            txn = Transaction().add(
                transfer(
                    TransferParams(
                        from_pubkey=keypair.public_key,
                        to_pubkey=phantom_pubkey,
                        lamports=lamports
                    )
                )
            )

            try:
                response = client.send_transaction(txn, keypair)
                txid = response["result"]
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # ✅ Log to Google Sheets
                sheet.append_row([
                    now, "SELL", token_symbol,
                    entry_marketcap, current_marketcap,
                    f"{ratio:.2f}x", label, txid, token_address
                ], value_input_option="USER_ENTERED")

                print(f"✅ Auto-sold {sell_amount:.4f} SOL @ {label} | TxID: {txid}")
                return txid

            except Exception as e:
                print(f"❌ Error selling {label}: {e}")
                continue

    except Exception as e:
        print(f"❌ Sell logic error: {e}")

    return None

