print("✅ NovaSniper booting up...")

import os
import base64
import time
import asyncio
import threading

# ✅ Load Railway Google Sheets JSON and set up env
b64_creds = os.getenv("GOOGLE_SHEETS_JSON")
if b64_creds:
    creds_path = "/tmp/credentials.json"
    with open(creds_path, "wb") as f:
        f.write(base64.b64decode(b64_creds))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
else:
    raise ValueError("Missing GOOGLE_SHEETS_JSON env variable")

# ✅ Safe to import now
from telegram_listener import start_telegram_listener
from buy_token import buy_token
from sell_ladder import sell_fn
from price_feed import get_token_price
from pumpfun_price import fetch_price
from logger import log_trade
from get_market_cap import get_market_cap

# === STATE ===
active_trades = {}
entry_amount_sol = 0.001

# === CALLBACK ===
def on_new_token(token_address, token_label):
    if token_address in active_trades:
        print(f"⚠️ Already tracking {token_label} ({token_address}) — skipping.")
        return

    print(f"📩 New token detected: {token_label} ({token_address})")
    success = buy_token(token_address)
    if success:
        print(f"✅ Buy successful.")
        entry_marketcap = get_market_cap(token_address)
        if entry_marketcap:
            active_trades[token_address] = {
                "symbol": token_label,
                "entry_cap": entry_marketcap,
                "sol_amount": entry_amount_sol,
                "targets_hit": {
                    "2x": False, "3x": False, "5x": False
                }
            }
            log_trade(
                action="BUY",
                token=token_label,
                entry_price=entry_marketcap,
                tx_id="",
                token_address=token_address
            )
            threading.Thread(target=monitor_trade_loop, args=(token_address,), daemon=True).start()
        else:
            print(f"❌ Couldn't fetch market cap for {token_label}")
    else:
        print("❌ Buy failed.")

# === MONITOR LOOP ===
def monitor_trade_loop(token_address):
    while token_address in active_trades:
        trade = active_trades[token_address]
        try:
            current_cap = get_market_cap(token_address)
            if not current_cap:
                print(f"⚠️ Market cap fetch failed for {trade['symbol']}")
                time.sleep(10)
                continue

            entry_cap = trade["entry_cap"]
            ratio = current_cap / entry_cap
            print(f"📊 {trade['symbol']} — Cap: {current_cap:.2f} | Entry: {entry_cap:.2f} | x{ratio:.2f}")

            for x, percent, key in [(2, 0.5, "2x"), (3, 0.3, "3x"), (5, 0.2, "5x")]:
                if not trade["targets_hit"][key] and ratio >= x:
                    tx_id = sell_fn(
                        token_symbol=trade["symbol"],
                        token_address=token_address,
                        entry_marketcap=entry_cap,
                        wallet_total_sol="$540.00",
                        initial_sol_amount=trade["sol_amount"] * percent
                    )
                    if tx_id:
                        print(f"💸 {trade['symbol']}: Sold {int(percent * 100)}% at {key}")
                        trade["targets_hit"][key] = True
                        log_trade(
                            action="SELL",
                            token=trade["symbol"],
                            entry_price=entry_cap,
                            current_price=current_cap,
                            pnl_pct=(ratio - 1) * 100,
                            target=key.upper(),
                            tx_id=tx_id,
                            token_address=token_address
                        )

            if all(trade["targets_hit"].values()):
                print(f"✅ {trade['symbol']} completed all targets. Closing trade.")
                del active_trades[token_address]

        except Exception as e:
            print(f"❌ Error in monitor loop for {trade['symbol']}: {e}")
        time.sleep(10)

# === MAIN ===
async def main():
    await start_telegram_listener(on_new_token)

    # ✅ Keep Railway container alive
    while True:
        await asyncio.sleep(3600)

# === Start FastAPI server + bot ===
import uvicorn

def run_web():
    uvicorn.run("keep_alive:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    try:
        print("🚀 NovaSniper V3 Multi-Trade Live")
        print("📡 Listening to Telegram and tracking profit targets...")

        # Launch web server in background
        threading.Thread(target=run_web, daemon=True).start()

        # Run bot
        asyncio.run(main())

    except Exception as e:
        print(f"❌ Uncaught top-level error: {e}")

