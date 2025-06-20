from playwright.async_api import async_playwright

async def fetch_price(token_address: str) -> str:
    url = f"https://pump.fun/{token_address}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=10000)
            await page.wait_for_selector("text=$", timeout=5000)
            price_element = await page.query_selector("text=$")
            return await price_element.inner_text() if price_element else "Price not found"
        except Exception as e:
            return f"Error fetching price: {e}"
        finally:
            await browser.close()

