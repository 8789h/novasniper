from telegram_listener import start_telegram_listener

if __name__ == "__main__":
    start_telegram_listener()

from price_tracker import get_token_price

# Replace with a token you bought
token = "Dd2T3apN8Vc1GRr8oPkCpnkNu3ykvKDcFt1AEk8ypump".replace("pump", "")
get_token_price(token)

