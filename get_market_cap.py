import requests

def get_market_cap(token_address):
    try:
        url = f"https://pump.fun/metadata/{token_address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("marketCap", None)
    except Exception as e:
        print(f"❌ Error fetching market cap: {e}")
        return None

