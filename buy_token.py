import os
import time
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction
from solders.transaction import Transaction
from solders.message import Message
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from dotenv import load_dotenv

# === Load env variables ===
load_dotenv()
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BUY_AMOUNT_SOL = float(os.getenv("BUY_AMOUNT_SOL", 0.001))

# === Setup
keypair = Keypair.from_base58_string(PRIVATE_KEY)
client = Client(RPC_URL)

def buy_token(token_address: str, retries: int = 3, delay: int = 5) -> bool:
    print(f"🛒 Sending SOL to token address: {token_address}")
    sender = keypair.pubkey()
    receiver = Pubkey.from_string(token_address)
    lamports = int(BUY_AMOUNT_SOL * 1_000_000_000)

    for attempt in range(1, retries + 1):
        try:
            # === Create transfer instruction (raw SOL)
            keys = [
                {"pubkey": sender, "is_signer": True, "is_writable": True},
                {"pubkey": receiver, "is_signer": False, "is_writable": True},
            ]
            data = b'\x02' + lamports.to_bytes(8, byteorder="little")
            instruction = Instruction(
                program_id=Pubkey.from_string("11111111111111111111111111111111"),
                accounts=keys,
                data=data
            )

            # === Build and send tx
            latest_blockhash = client.get_latest_blockhash()["result"]["value"]["blockhash"]
            message = Message([instruction], payer=sender)
            tx = Transaction([keypair], message, recent_blockhash=latest_blockhash)

            sig = client.send_raw_transaction(tx.serialize(), opts=TxOpts(skip_preflight=True))["result"]
            print(f"✅ Buy successful: https://solscan.io/tx/{sig}")
            return True

        except Exception as e:
            print(f"❌ [Attempt {attempt}] Error: {e}")
            time.sleep(delay)

    print(f"❌ All {retries} attempts failed for token {token_address}")
    return False

