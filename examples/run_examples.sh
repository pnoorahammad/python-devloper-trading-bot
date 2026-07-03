#!/bin/bash

# Make sure you have configured your .env file with Binance API keys before running this script

echo "Executing MARKET Order Example..."
python ../cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

echo "Executing LIMIT Order Example..."
python ../cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3500
