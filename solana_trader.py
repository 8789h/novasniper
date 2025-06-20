import os
import requests
import time
from dotenv import load_dotenv
from solana.rpc.api import Client
from solders.keypair import Keypair

from wallet_tracker import (
    track_token,
    update_token_price,
    mark_token_sold
)

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
BUY_AMOUNT_SOL = float(os.getenv("BUY_AMOUNT_SOL", 0.05))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

client = Client(RPC_URL)
keypair = Keypair.from_base58_string(PRIVATE_KEY)

def buy_token(token_address):
    print(f"🚀 Buying token: {token_address}")

    entry_price = get_price(token_address)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    track_token(token_address, entry_price)

    return {
        "token": token_address,
        "entry_price": entry_price,
        "amount": BUY_AMOUNT_SOL,
        "timestamp": timestamp
    }

def get_price(token_address):
    try:
        url = f"https://public-api.birdeye.so/public/price?address={token_address}"
        headers = {"X-API-KEY": os.getenv("BIRDEYE_API_KEY")}
        response = requests.get(url, headers=headers)
        data = response.json()
        return float(data["data"]["value"])
    except Exception as e:
        print(f"⚠️ Error getting price: {e}")
        return 0.0

def watch_price_and_sell(token_address, entry_price):
    print(f"👀 Watching {token_address} for profit targets...")

    targets = {
        2: False,
        3: False,
        5: False,
        10: False,
        50: False
    }

    while True:
        current_price = get_price(token_address)
        update_token_price(token_address, current_price)

        if current_price == 0.0:
            print("⚠️ Price fetch failed, retrying...")
            time.sleep(10)
            continue

        price_ratio = current_price / entry_price
        print(f"📈 {token_address}: Entry = {entry_price} | Current = {current_price} | x = {price_ratio:.2f}")

        for multiple in targets:
            if price_ratio >= multiple and not targets[multiple]:
                targets[multiple] = True
                sell_token(token_address, multiple)

        if all(targets.values()):
            print(f"✅ All profit targets hit for {token_address}")
            mark_token_sold(token_address)
            break

        time.sleep(20)

def sell_token(token_address, multiple):
    print(f"💰 Selling {token_address} at {multiple}x profit")
    # This is a mock sell — replace with real Jupiter/pump.fun integration if needed

