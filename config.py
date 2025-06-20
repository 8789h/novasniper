# config.py

import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    # Telegram
    "TELEGRAM_API_ID": int(os.getenv("TELEGRAM_API_ID")),
    "TELEGRAM_API_HASH": os.getenv("TELEGRAM_API_HASH"),
    "SESSION_NAME": os.getenv("SESSION_NAME", "novasniper"),
    "TARGET_CHANNEL_ID": int(os.getenv("TARGET_CHANNEL_ID")),

    # Solana
    "PRIVATE_KEY": os.getenv("PRIVATE_KEY"),
    "PHANTOM_PUBLIC_KEY": os.getenv("PHANTOM_PUBLIC_KEY"),
    "RPC_URL": os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com"),
    "BUY_AMOUNT_SOL": float(os.getenv("BUY_AMOUNT_SOL", 0.0001)),

    # Logging
    "GOOGLE_SHEETS_CREDENTIALS": os.getenv("GOOGLE_SHEETS_CREDENTIALS"),
    "SHEET_ID": os.getenv("SHEET_ID"),

    # Jupiter
    "JUPITER_API": os.getenv("JUPITER_API", "https://quote-api.jup.ag"),
}

