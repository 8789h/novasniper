import time
from sell import sell_token

# 🧪 Mock price fetcher for testing
def fetch_birdeye_price(token):
    print(f"📈 [SIM] Fetching price for token {token}")

    try:
        price = 0.0002  # Simulated fixed price for trigger
        print(f"💹 [SIM] Price returned: {price}")
        return price

    except Exception as e:
        print(f"❌ Price fetch error: {e}")
        return None


# 🪜 Simulated sell ladder trigger
def watch_price_and_sell(token, rpc_url, private_key, phantom_address, label="AUTO", entry_price=None):
    print(f"⏳ [SIM] Watching price for {token}...")

    try:
        for i in range(3):  # Simulate 3 attempts
            time.sleep(1)
            price = fetch_birdeye_price(token)

            if price >= 0.0002:
                print(f"🎯 Target hit! Price = {price}")
                sell_token(token, rpc_url, private_key, phantom_address, label)
                break
            else:
                print(f"📉 Waiting... (Price = {price})")

    except Exception as e:
        print(f"🔥 Error during sell ladder: {e}")

