import os
import time
import base64
import requests
from solders.keypair import Keypair
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
from solana.rpc.api import Client
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
RPC_URL = os.getenv("RPC_URL")
JUPITER_API = os.getenv("JUPITER_API", "https://quote-api.jup.ag")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BUY_AMOUNT_SOL = float(os.getenv("BUY_AMOUNT_SOL", 0.001))

# === Wallet setup ===
keypair = Keypair.from_base58_string(PRIVATE_KEY)
client = Client(RPC_URL)

# === Buy token using Jupiter with retries
def buy_token(token_address: str, retries: int = 3, delay: int = 5) -> bool:
    print(f"🛒 Attempting to buy token: {token_address}")
    user_pubkey = str(keypair.pubkey())
    amount_lamports = int(BUY_AMOUNT_SOL * 1_000_000_000)

    for attempt in range(1, retries + 1):
        try:
            # 1. Fetch quote
            quote_res = requests.get(f"{JUPITER_API}/v6/quote", params={
                "inputMint": "So11111111111111111111111111111111111111112",  # SOL
                "outputMint": token_address,
                "amount": amount_lamports,
                "slippageBps": 500,
                "onlyDirectRoutes": "true"  # NOTE: string, not boolean!
            })

            quote_json = quote_res.json()
            print("🔍 Quote response:", quote_json)

            # ✅ Use the whole response directly
            route = quote_json

            if "routePlan" not in route:
                print(f"❌ [Attempt {attempt}] No route found. Full response: {quote_json}")
                time.sleep(delay)
                continue

            # 2. Request swap transaction
            swap_res = requests.post(f"{JUPITER_API}/v6/swap", json={
                "userPublicKey": user_pubkey,
                "route": route,
                "wrapUnwrapSOL": True,
                "computeUnitPriceMicroLamports": 1
            })

            swap_data = swap_res.json()
            print("🔁 Swap response:", swap_data)
            swap_tx_base64 = swap_data.get("swapTransaction")

            if not swap_tx_base64:
                print(f"❌ [Attempt {attempt}] No transaction returned. Full response: {swap_data}")
                time.sleep(delay)
                continue

            # 3. Decode and sign the transaction
            swap_tx_bytes = base64.b64decode(swap_tx_base64)
            message = MessageV0.from_bytes(swap_tx_bytes)
            tx = VersionedTransaction(message, [keypair])

            # 4. Send transaction
            response = client.send_raw_transaction(tx.serialize(), opts={"skip_preflight": True})
            sig = response.get("result")

            if not sig:
                print(f"❌ [Attempt {attempt}] Transaction rejected: {response}")
                time.sleep(delay)
                continue

            print(f"✅ Buy successful: https://solscan.io/tx/{sig}")
            return True

        except Exception as e:
            print(f"❌ [Attempt {attempt}] Error: {e}")
            time.sleep(delay)

    print(f"❌ All {retries} attempts failed for token {token_address}")
    return False

