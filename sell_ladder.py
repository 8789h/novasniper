import os
import datetime
import base58
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.instruction import Instruction
from solana.rpc.api import Client
from logger import log_trade  # ✅ CSV logger
from get_market_cap import get_market_cap  # ✅ Market cap fetcher

# === Load env vars ===
load_dotenv()
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PHANTOM_PUBLIC_KEY = os.getenv("PHANTOM_PUBLIC_KEY")

# === Setup Solana client and wallet ===
client = Client(RPC_URL)
keypair = Keypair.from_base58_string(PRIVATE_KEY)
phantom_pubkey = Pubkey.from_string(PHANTOM_PUBLIC_KEY)

# === Constants ===
SYS_PROGRAM_ID = Pubkey.from_string("11111111111111111111111111111111")

# === SELL FUNCTION using market cap logic ===
def sell_fn(token_symbol, token_address, entry_marketcap, wallet_total_sol, initial_sol_amount):
    try:
        current_marketcap = get_market_cap(token_address)
        if not current_marketcap or not entry_marketcap:
            print(f"❌ Missing market cap data for {token_symbol}")
            return None

        ratio = current_marketcap / entry_marketcap
        targets_hit = []

        if ratio >= 2:
            targets_hit.append(("2x", 0.5))
        if ratio >= 3:
            targets_hit.append(("3x", 0.3))
        if ratio >= 5:
            targets_hit.append(("5x", 0.2))

        for label, percent in targets_hit:
            sell_amount = initial_sol_amount * percent
            lamports = int(sell_amount * 1_000_000_000)

            # Build transfer instruction
            ix = Instruction(
                program_id=SYS_PROGRAM_ID,
                accounts=[
                    {"pubkey": keypair.pubkey(), "is_signer": True, "is_writable": True},
                    {"pubkey": phantom_pubkey, "is_signer": False, "is_writable": True}
                ],
                data=lamports.to_bytes(8, "little") + b"\x02"  # transfer instruction layout
            )

            txn = Transaction([ix])
            try:
                response = client.send_raw_transaction(txn.sign([keypair]).serialize(), opts={"skip_preflight": True})
                txid = response["result"]
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                log_trade(
                    action="SELL",
                    token=token_symbol,
                    entry_price=entry_marketcap,
                    current_price=current_marketcap,
                    pnl_pct=(ratio - 1) * 100,
                    target=label,
                    tx_id=txid,
                    token_address=token_address
                )

                print(f"✅ Auto-sold {sell_amount:.4f} SOL @ {label} | TxID: {txid}")
                return txid

            except Exception as e:
                print(f"❌ Error selling {label}: {e}")
                continue

    except Exception as e:
        print(f"❌ Sell logic error: {e}")
        
    return None

