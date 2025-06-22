import os
import time
from solana.transaction import Transaction
from solana.system_program import transfer, TransferParams
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BUY_AMOUNT_SOL = float(os.getenv("BUY_AMOUNT_SOL", 0.001))

# === Wallet setup ===
keypair = Keypair.from_base58_string(PRIVATE_KEY)
client = Client(RPC_URL)

# === Function to buy token via raw SOL transfer ===
def buy_token(token_address: str, retries: int = 3, delay: int = 5) -> bool:
    print(f"🛒 Attempting SOL transfer to: {token_address}")
    receiver = Pubkey.from_string(token_address)
    sender = keypair.pubkey()
    lamports = int(BUY_AMOUNT_SOL * 1_000_000_000)

    for attempt in range(1, retries + 1):
        try:
            tx = Transaction()
            tx.add(
                transfer(
                    TransferParams(
                        from_pubkey=sender,
                        to_pubkey=receiver,
                        lamports=lamports,
                    )
                )
            )

            response = client.send_transaction(tx, keypair)
            sig = response.get("result")
            if not sig:
                print(f"❌ [Attempt {attempt}] Transfer rejected: {response}")
                time.sleep(delay)
                continue

            print(f"✅ Transfer successful: https://solscan.io/tx/{sig}")
            return True

        except Exception as e:
            print(f"❌ [Attempt {attempt}] Error: {e}")
            time.sleep(delay)

    print(f"❌ All {retries} attempts failed for token {token_address}")
    return False

