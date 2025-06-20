import requests
import re

def get_pump_price(token_address):
    try:
        url = f"https://pump.fun/{token_address}"
        response = requests.get(url)
        html = response.text

        match = re.search(r'Market Cap</div><div[^>]*>\$(\d{1,3}(?:,\d{3})*)', html)
        if match:
            market_cap_str = match.group(1).replace(",", "")
            return float(market_cap_str)
    except Exception as e:
        print(f"❌ Error getting pump.fun price for {token_address}: {e}")
    return None


