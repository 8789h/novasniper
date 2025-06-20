import os
import base58
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.keypair import Keypair
from solana.publickey import PublicKey
from dotenv import load_dotenv

# === Load environment ===
load_dotenv()

# === Load config ===
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BUY_AMOUNT_SOL = float(os.getenv("BUY_AMOUNT_SOL", 0.01))
RPC_URL = os.getenv("RPC_URL")

# === Decode base58 Phantom key
keypair = Keypair.from_secret_key(base58.b58decode(PRIVATE_KEY))
phantom_public = keypair.public_key

# === Connect to Solana
client = Client(RPC_URL)

# === Buy Function
def buy_token(token_address):
    try:
        print(f"🛒 Buying token: {token_address}")
        destination = PublicKey(token_address)
        lamports = int(BUY_AMOUNT_SOL * 1_000_000_000)

        txn = Transaction()
        txn.add(
            transfer(
                TransferParams(
                    from_pubkey=phantom_public,
                    to_pubkey=destination,
                    lamports=lamports
                )
            )
        )

        result = client.send_transaction(txn, keypair)
        print(f"✅ Buy transaction sent! TxID: {result['result']}")
        return True

    except Exception as e:
        print(f"❌ Buy failed: {e}")
        return False

