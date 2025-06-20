def sell_token(token, rpc_url, private_key, phantom_address, trigger="AUTO"):
    print(f"💸 [SIM] Selling token {token} – Triggered by: {trigger}")

    # Simulate a fake but successful sell response
    mock_response = {
        "txid": "SIMULATED_SELL_TX",
        "status": "success"
    }

    print(f"✅ [SIM] Sell simulated successfully for {token}")

    # 🧾 Simulate logging to Google Sheets
    try:
        print(f"📊 [SIM] Logging trade to Google Sheets: Token={token}, TX={mock_response['txid']}, Trigger={trigger}")
        # Simulated row write
        print("🟢 [SIM] Log successful.")
    except Exception as e:
        print(f"⚠️ [SIM] Failed to log to sheet: {e}")

    return mock_response

def buy_token(token):
    print(f"🔄 [SIM] Buying token: {token}")

    # Simulate a fake buy transaction
    mock_tx = "SIMULATED_BUY_TX"
    print(f"✅ [SIM] Buy simulated successfully for {token}")
    print(f"🟢 Simulated buy TX: {mock_tx}")

    # 🧾 Simulate logging to Google Sheets
    try:
        print(f"📊 [SIM] Logging trade to Google Sheets: Token={token}, TX={mock_tx}, Trigger=BUY")
        # Simulated row write
        print("🟢 [SIM] Log successful.")
    except Exception as e:
        print(f"⚠️ [SIM] Failed to log to sheet: {e}")

    return mock_tx

