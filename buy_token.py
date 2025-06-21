import os
import base58
import requests
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.rpc.types import TxOpts
from dotenv import load_dotenv

# === Load .env ===
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
BUY_AMOUNT_SOL = float(os.getenv("BUY_AMOUNT_SOL", 0.001))
JUPITER_API = os.getenv("JUPITER_API", "https://quote-api.jup.ag")

# === Setup Solana ===
client = Client(RPC_URL)
keypair = Keypair.from_secret_key(base58.b58decode(PRIVATE_KEY))
public_key = str(keypair.public_key)

# === Buy function ===
def buy_token(token_address):
    try:
        print(f"🛒 Buying token: {token_address}")

        # 1. Get best route from SOL → Token
        quote_url = f"{JUPITER_API}/v6/quote?inputMint=So11111111111111111111111111111111111111112&outputMint={token_address}&amount={int(BUY_AMOUNT_SOL * 1_000_000_000)}&slippageBps=500"
        quote = requests.get(quote_url).json()

        if not quote["routes"]:
            raise Exception("No swap route found.")

        route = quote["routes"][0]

        # 2. Get swap transaction
        swap_url = f"{JUPITER_API}/v6/swap"
        swap_data = {
            "userPublicKey": public_key,
            "wrapUnwrapSOL": True,
            "quoteResponse": route,
            "computeUnitPriceMicroLamports": 1
        }
        swap_txn = requests.post(swap_url, json=swap_data).json()
        swap_tx = base58.b58decode(swap_txn["swapTransaction"])

        # 3. Sign and send
        from solana.transaction import Transaction
        txn = Transaction.deserialize(swap_tx)
        txn.sign(keypair)
        result = client.send_transaction(txn, keypair, opts=TxOpts(skip_preflight=True, preflight_commitment="confirmed"))

        print(f"✅ Swap success! TxID: {result['result']}")
        return result['result']

    except Exception as e:
        print(f"❌ Buy failed: {e}")
        return False

