import csv
import os
from datetime import datetime

LOG_FILE = "trades_log.csv"

def log_trade(action, token, entry_price, current_price=None, pnl_pct=None, target=None, tx_id=None, token_address=None):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "Timestamp", "Action", "Token", "Token Address",
                "Entry Price", "Current Price", "PnL (%)", "Target", "TxID"
            ])
        writer.writerow([
            datetime.utcnow().isoformat(),
            action,
            token,
            token_address or "",
            entry_price,
            current_price or "",
            pnl_pct or "",
            target or "",
            tx_id or ""
        ])

