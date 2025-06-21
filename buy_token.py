import os
import requests
import base58
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.transaction import Transaction
from solders.pubkey import Pubkey
from solders.instruction import Instruction
from solders.message import MessageV0
from solders.transaction import VersionedTransaction

# === Load config ===
RPC_URL = os.getenv("RPC_URL")
JUPITER_API = os.getenv("JUPITER_API", "https://quote-api.jup.ag")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BUY_AMOUNT_SOL = float(os.getenv("BUY_AMOUNT_SOL", 0.001))

# === Wallet setup ===
keypair = Keypair.from_secret_key(base58.b58decode(PRIVATE_KEY))
client = Client(RPC_URL)
async_client = AsyncClient(RPC_URL, commitment=Confirmed)

# === Buy token with Jupiter
def buy_token(token_address):
    try:
        print(f"🛒 Buying token: {token_address}")
        user_pubkey = str(keypair.public_key)

        # === 1. Fetch route
        quote_url = f"{JUPITER_API}/v6/quote"
        params = {
            "inputMint": "So11111111111111111111111111111111111111112",
            "outputMint": token_address,
            "amount": int(BUY_AMOUNT_SOL * 1_000_000_000),
            "slippageBps": 500,  # 5%
            "onlyDirectRoutes": True
        }

        quote_res = requests.get(quote_url, params=params)
        route = quote_res.json().get("data", [None])[0]

        if not route:
            print("❌ No route found — cannot buy.")
            return False

        # === 2. Get swap transaction
        swap_url = f"{JUPITER_API}/v6/swap"
        swap_res = requests.post(swap_url, json={
            "userPublicKey": user_pubkey,
            "route": route,
            "wrapUnwrapSOL": True,
            "computeUnitPriceMicroLamports": 1
        })

        swap_tx_encoded = swap_res.json().get("swapTransaction")
        if not swap_tx_encoded:
            print("❌ Failed to retrieve swap transaction.")
            return False

        # === 3. Decode + sign
        swap_tx_bytes = base58.b58decode(swap_tx_encoded)
        msg = MessageV0.from_bytes(swap_tx_bytes)
        tx = VersionedTransaction(msg, [keypair])

        # === 4. Send
        tx_sig = client.send_raw_transaction(tx.serialize(), opts={"skip_preflight": True})
        print(f"✅ Buy successful. Tx: {tx_sig['result']}")
        return True

    except Exception as e:
        print(f"❌ Buy failed with error: {e}")
        print(f"🔍 Exception type: {type(e)}")
        return False

