from watcher import watch_price_and_sell

# Simulate rising prices
class MockWatcher:
    def __init__(self, prices):
        self.prices = prices
        self.index = 0

    def fetch(self, token):
        price = self.prices[self.index]
        print(f\"📈 [SIM] Price: {price}\")
        self.index += 1
        return price

def test():
    fake_prices = [0.0001, 0.0002, 0.0003, 0.0005, 0.0006]
    mock = MockWatcher(fake_prices)

    import watcher
    watcher.fetch_birdeye_price = mock.fetch
    watcher.sell_token = lambda *args, **kwargs: print(f\"💸 [SIM] Sell: {kwargs.get('label')}\")
    
    watch_price_and_sell(
        token=\"FAKE_TOKEN\",
        entry_price=0.0001,
        rpc_url=\"https://fake.rpc\",
        private_key=\"FAKE_KEY\",
        phantom_address=\"FAKE_WALLET\"
    )

test()

