from solana.rpc.api import Client
from solana.publickey import PublicKey

public_key_str = "C6dvxUfhF1jkUKxYj5winhGFCstMxXcdLsce47mh181n"
public_key = PublicKey(public_key_str)

client = Client("https://api.mainnet-beta.solana.com")
balance = client.get_balance(public_key)
sol = balance['result']['value'] / 1e9
print(f"🪙 Balance for {public_key_str}: {sol:.9f} SOL")

txs = client.get_signatures_for_address(public_key)

print("\n📜 Recent Transactions:")
for tx in txs['result'][:5]:
    print(f"- Signature: {tx['signature']} | Slot: {tx['slot']} | Status: {tx['confirmationStatus']}")

