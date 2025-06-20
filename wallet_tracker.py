# wallet_tracker.py
active_tokens = []

def track_token(token_address, entry_price):
    active_tokens.append({
        "token": token_address,
        "entry_price": entry_price,
        "current_price": entry_price,
        "status": "OPEN"
    })

def update_token_price(token_address, current_price):
    for token in active_tokens:
        if token["token"] == token_address:
            token["current_price"] = current_price
            break

def mark_token_sold(token_address):
    for token in active_tokens:
        if token["token"] == token_address:
            token["status"] = "SOLD"
            break

def get_current_holdings():
    return active_tokens

