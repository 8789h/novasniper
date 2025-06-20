def sell_token(token, rpc_url, private_key, phantom_address, trigger="AUTO"):
    print(f"💸 [SIM] Selling token {token} – Triggered by: {trigger}")
    
    # Simulate a fake but successful sell response
    mock_response = {
        "txid": "SIMULATED_SELL_TX",
        "status": "success"
    }

    print(f"✅ [SIM] Sell simulated successfully for {token}")
    return mock_response

