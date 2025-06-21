import os
import requests
import base64
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
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

# === Buy token using Jupiter
def buy_token(token_address: str) -> bool:
    try:
        print(f"🛒 Buying token: {token_address}")
        user_pubkey = str(keypair.pubkey())

        # 1. Fetch quote
        quote_res = requests.get(f"{JUPITER_API}/v6/quote", params={
            "inputMint": "So11111111111111111111111111111111111111112",  # Native SOL
            "outputMint": token_address,
            "amount": int(BUY_AMOUNT_SOL * 1_000_000_000),  # In lamports
            "slippageBps": 500,  # 5% slippage
            "onlyDirectRoutes": True
        })

        quote_data = quote_res.json().get("data", [])
        if not quote_data:
            print("❌ No route found — token illiquid or invalid.")
            return False

        route = quote_data[0]

        # 2. Request swap transaction
        swap_res = requests.post(f"{JUPITER_API}/v6/swap", json={
            "userPublicKey": user_pubkey,
            "route": route,
            "wrapUnwrapSOL": True,
            "computeUnitPriceMicroLamports": 1
        })

        swap_tx_base64 = swap_res.json().get("swapTransaction")
        if not swap_tx_base64:
            print("❌ Failed to retrieve swap transaction.")
            return False

        # 3. Decode and sign the transaction
        swap_tx_bytes = base64.b64decode(swap_tx_base64)
        message = MessageV0.from_bytes(swap_tx_bytes)
        tx = VersionedTransaction(message, [keypair])

        # 4. Send transaction
        response = client.send_raw_transaction(tx.serialize(), opts={"skip_preflight": True})
        sig = response.get("result")

        if not sig:
            print("❌ Transaction rejected or failed.")
            return False

        print(f"✅ Buy successful: https://solscan.io/tx/{sig}")
        return True

    except Exception as e:
        print(f"❌ Buy failed with error: {e}")
        return False

