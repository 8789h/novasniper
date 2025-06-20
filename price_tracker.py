# price_tracker.py

import aiohttp
import asyncio

# 🔑 Replace this with your actual Birdeye API Key
BIRDEYE_API_KEY = "5ed9a0c94bd245fc8598753cf3ca02e1"
BIRDEYE_BASE_URL = "https://public-api.birdeye.so/public"

headers = {
    "accept": "application/json",
    "x-api-key": BIRDEYE_API_KEY
}

async def get_token_price(session, token_address):
    """
    Get the current price of a Solana token from Birdeye API.
    
    :param session: aiohttp client session
    :param token_address: str, token's Solana address
    :return: float or None
    """
    url = f"{BIRDEYE_BASE_URL}/token_price?address={token_address}"

    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return float(data["data"]["value"])
            else:
                print(f"Birdeye API error {resp.status} for token {token_address}")
                return None
    except Exception as e:
        print(f"Error fetching price for {token_address}: {e}")
        return None


async def test_price_fetch(token_address):
    """
    Test function for standalone price checking
    """
    async with aiohttp.ClientSession() as session:
        price = await get_token_price(session, token_address)
        print(f"Price for {token_address}: {price}")


if __name__ == "__main__":
    test_token = "3XAsVenR7eGCZSNjfoKVRKj5NmadHUgnzHt5Cmn2"
    asyncio.run(test_price_fetch(test_token))

