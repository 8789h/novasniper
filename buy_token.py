import os
import time
from solana.transaction import Transaction, TransactionInstruction
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solders.keypair import Keypair
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
    receiver = PublicKey(token_address)
    sender = keypair.pubkey()
    lamports = int(BUY_AMOUNT_SOL * 1_000_000_000)

    for attempt in range(1, retries + 1):
        try:
            # Build raw transfer instruction
            instruction = TransactionInstruction(
                keys=[
                    {"pubkey": sender, "is_signer": True, "is_writable": True},
                    {"pubkey": receiver, "is_signer": False, "is_writable": True},
                ],
                program_id=PublicKey("11111111111111111111111111111111"),  # System program
                data=lamports.to_bytes(8, "little")  # 64-bit unsigned int LE
            )

            # Build transaction and send
            tx = Transaction().add(instruction)
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

