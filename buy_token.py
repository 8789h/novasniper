import os
from dotenv import load_dotenv
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.publickey import PublicKey
from solders.keypair import Keypair
from solana.rpc.types import TxOpts

# === Load environment variables ===
load_dotenv()
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BUY_AMOUNT_SOL = float(os.getenv("BUY_AMOUNT_SOL", 0.001))

# === Setup wallet and Solana client ===
client = Client(RPC_URL)
keypair = Keypair.from_base58_string(PRIVATE_KEY)
wallet = keypair.pubkey()
lamports = int(BUY_AMOUNT_SOL * 1_000_000_000)

# === Direct Pump.fun Buy Function ===
def buy_token(token_address: str) -> bool:
    print(f"🛒 Buying on Pump.fun: {token_address}")
    try:
        token_pubkey = PublicKey(token_address)

        txn = Transaction()
        txn.add(
            transfer(
                TransferParams(
                    from_pubkey=wallet,
                    to_pubkey=token_pubkey,
                    lamports=lamports
                )
            )
        )

        res = client.send_transaction(txn, keypair, opts=TxOpts(skip_preflight=True))
        sig = res.get("result")

        if sig:
            print(f"✅ Buy successful: https://solscan.io/tx/{sig}")
            return True
        else:
            print("❌ Transaction failed:", res)
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

