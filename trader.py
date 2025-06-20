import os
import requests
import base58
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

# Load config
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BUY_AMOUNT_SOL = Decimal(os.getenv("BUY_AMOUNT_SOL", "0.01"))
RPC_URL = os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")

# Decode wallet key
secret = base58.b58decode(PRIVATE_KEY)
keypair = Keypair.from_secret_key(secret)
client = Client(RPC_URL)

# ✅ Get metadata from pump.fun
def get_token_metadata(token):
    try:
        url = f"https://pump.fun/metadata/{token}"
        response = requests.get(url, timeout=4)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Failed to fetch metadata for {token}: {e}")
        return None

# ✅ BUY FUNCTION
async def buy_token(token_address):
    print(f"🛒 Attempting to buy token: {token_address}")

    # Step 1: Fetch metadata (get mintAuthority address)
    metadata = get_token_metadata(token_address)
    if not metadata or "mintAuthority" not in metadata:
        print("❌ Invalid or missing mintAuthority — skipping buy.")
        return

    mint_authority = metadata["mintAuthority"]
    print(f"✅ Found mintAuthority: {mint_authority}")

    # Step 2: Convert SOL to lamports
    lamports = int(BUY_AMOUNT_SOL * 1_000_000_000)

    # Step 3: Create transfer transaction
    try:
        txn = Transaction().add(
            transfer(
                TransferParams(
                    from_pubkey=keypair.public_key,
                    to_pubkey=mint_authority,
                    lamports=lamports
                )
            )
        )

        # Step 4: Send transaction
        result = client.send_transaction(txn, keypair)
        tx_sig = result.get("result")

        if tx_sig:
            print(f"✅ Buy transaction submitted: {tx_sig}")
        else:
            print(f"❌ Transaction failed to return result: {result}")

    except Exception as e:
        print(f"❌ Error during send_transaction: {e}")

