# price_feed.py

import re
from playwright.async_api import async_playwright

async def get_token_price(token_address: str) -> float:
    url = f"https://pump.fun/{token_address}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=10000)
            await page.wait_for_selector("text=Market Cap", timeout=5000)

            # Find the element visually near "Market Cap"
            all_text = await page.inner_text('body')

            # Extract the first occurrence of $123,456 using regex
            match = re.search(r"\$([\d,]+)", all_text)
            if match:
                numeric_price = float(match.group(1).replace(",", ""))
                return numeric_price
            else:
                print("❌ Market cap regex failed.")
                return None

        except Exception as e:
            print(f"❌ Error getting token price: {e}")
            return None
        finally:
            await browser.close()

