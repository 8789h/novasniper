from solana.rpc.api import Client
from solana.publickey import PublicKey
import os
from dotenv import load_dotenv

load_dotenv()

wallet_address = os.getenv("PHANTOM_PUBLIC_KEY")

def get_tokens():
    try:
        client = Client("https://api.mainnet-beta.solana.com")

        result = client.get_token_accounts_by_owner(
            PublicKey(wallet_address),
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
            encoding="jsonParsed"
        )

        if result.get("result") and result["result"]["value"]:
            print("📦 Token Balances:")
            for token in result["result"]["value"]:
                try:
                    parsed_info = token["account"]["data"]["parsed"]["info"]
                    mint = parsed_info["mint"]
                    amount = parsed_info["tokenAmount"]["uiAmountString"]
                    print(f"🪙 {mint} → {amount}")
                except Exception as e:
                    print("⚠️ Error parsing token:", e)
        else:
            print("📭 No tokens found in wallet.")

    except Exception as e:
        print("❌ Error fetching token balances:", e)

if __name__ == "__main__":
    get_tokens()


