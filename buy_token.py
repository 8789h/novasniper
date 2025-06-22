import os
import time
import requests
from dotenv import load_dotenv
from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.types import TxOpts

# === Load env variables ===
load_dotenv()
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BUY_AMOUNT_SOL = float(os.getenv("BUY_AMOUNT_SOL", 0.001))

# === Setup
keypair = Keypair.from_base58_string(PRIVATE_KEY)
client = Client(RPC_URL)

def buy_token(token_address: str, retries: int = 3, delay: int = 5) -> bool:
    print(f"🚀 Attempting pump.fun buy for: {token_address}")
    for attempt in range(1, retries + 1):
        try:
            # === Step 1: Get serialized transaction from pump.fun API
            response = requests.post(
                "https://pump.fun/api/buy",
                json={
                    "buyer": str(keypair.pubkey()),
                    "mint": token_address,
                    "amount": int(BUY_AMOUNT_SOL * 1_000_000_000),  # in lamports
                    "priorityFee": 1  # optional, can be 0–2
                },
                timeout=10
            )
            response.raise_for_status()
            tx_base64 = response.json()["transaction"]

            # === Step 2: Send transaction
            send_result = client.send_raw_transaction(
                bytes.fromhex(tx_base64),
                opts=TxOpts(skip_preflight=True)
            )
            sig = send_result.value
            print(f"✅ Buy successful: https://solscan.io/tx/{sig}")
            return True

        except Exception as e:
            print(f"❌ [Attempt {attempt}] Error: {e}")
            time.sleep(delay)

    print(f"❌ All {retries} pump.fun buy attempts failed for token {token_address}")
    return False

