import os
import base58
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed
from solana.transaction import Transaction
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.system_program import TransferParams, transfer
from spl.token.instructions import get_associated_token_address, create_associated_token_account
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from dotenv import load_dotenv

# === Load env ===
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BUY_AMOUNT_SOL = float(os.getenv("BUY_AMOUNT_SOL", 0.001))
RPC_URL = os.getenv("RPC_URL")

# === Set up wallet and client ===
keypair = Keypair.from_secret_key(base58.b58decode(PRIVATE_KEY))
wallet = keypair.public_key
client = Client(RPC_URL, commitment=Confirmed)

# === Pump.fun bonding curve derivation ===
def get_bonding_curve_address(token_address: str) -> PublicKey:
    token_pubkey = PublicKey(token_address)
    seeds = [b"bonding_curve", bytes(token_pubkey)]
    curve_pubkey, _ = PublicKey.find_program_address(seeds, PublicKey("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkgkPjKSb8G49"))
    return curve_pubkey

# === Buy function ===
def buy_token(token_address: str) -> bool:
    try:
        print(f"🛒 Buying token: {token_address}")

        token_pubkey = PublicKey(token_address)
        bonding_curve = get_bonding_curve_address(token_address)
        ata = get_associated_token_address(wallet, token_pubkey)

        txn = Transaction()

        # Create ATA if missing
        resp = client.get_account_info(ata)
        if not resp["result"]["value"]:
            txn.add(create_associated_token_account(
                payer=wallet,
                owner=wallet,
                mint=token_pubkey
            ))

        # Transfer SOL to bonding curve
        lamports = int(BUY_AMOUNT_SOL * 1_000_000_000)
        txn.add(transfer(TransferParams(
            from_pubkey=wallet,
            to_pubkey=bonding_curve,
            lamports=lamports
        )))

        # Send transaction
        resp = client.send_transaction(txn, keypair)
        sig = resp["result"]
        print(f"✅ Buy sent! TxID: {sig}")
        return True

    except Exception as e:
        print(f"❌ Buy failed: {e}")
        return False

