# pumpfun_price_tracker.py

import aiohttp
import asyncio

async def get_pumpfun_price(token_address):
    url = f"https://client-api.pump.fun/token/{token_address}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    price = float(data["price"])
                    return price
                else:
                    print(f"Pump.fun API error {resp.status} for token {token_address}")
                    return None
    except Exception as e:
        print(f"Error fetching pump.fun price for {token_address}: {e}")
        return None


async def test_price():
    token = "3XAsVenR7eGCZSNjfoKVRKj5NmadHUgnzHt5Cmn2"  # no 'pump'
    price = await get_pumpfun_price(token)
    print(f"Pump.fun price: {price} SOL")


if __name__ == "__main__":
    asyncio.run(test_price())

