from solders.pubkey import Pubkey as SoldersPubkey

# 🧪 Mock buy_token with full signature support
def buy_token(token, rpc_url=None, private_key=None, phantom_address=None):
    print(f"🔄 Buying token: {token}")

    try:
        if isinstance(token, str):
            token = SoldersPubkey.from_string(token)

        print(f"✅ [SIM] Buy simulated successfully for {token}")
        return "SIMULATED_BUY_TX"

    except Exception as e:
        print(f"❌ BUY Failed: {e}")
        return None

