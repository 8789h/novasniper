#!/bin/sh
echo "Starting NovaSniper..."
echo "TELEGRAM_API_ID=$TELEGRAM_API_ID"
exec python run_novasniper_live.py
