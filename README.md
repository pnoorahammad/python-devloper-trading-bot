# Binance Futures Testnet Trading Bot

A production-quality Python CLI application to execute trades on the Binance Futures Testnet.

## Project Overview

This trading bot allows users to place MARKET and LIMIT orders (both BUY and SELL sides) on the Binance USDT-M Futures Testnet. Built with modern tooling, it uses a modular architecture, features robust error handling, detailed file-based logging, and provides an enhanced interactive CLI experience via Typer and Rich. It is fully Dockerized for seamless deployment.

## Architecture & Folder Structure

- **Modular Design**: Separates the API client initialization, core order execution logic, and input validation.
- **Exception Handling**: Uses custom exceptions (`bot/exceptions.py`) to distinguish between validation, configuration, API, and network errors.
- **Rich CLI**: Uses `typer` and `rich` for command-line parsing, animated progress spinners, and formatted table outputs.

```
python-devloper-trading-bot/
├── bot/
│   ├── __init__.py
│   ├── client.py         # Binance client wrapper
│   ├── orders.py         # Order placement logic
│   ├── validators.py     # Strict input validation
│   ├── config.py         # Environment configuration
│   ├── logging_config.py # Structured logging setup
│   └── exceptions.py     # Custom exceptions
├── logs/                 # Output directory for trading.log
├── examples/             # Example usage scripts
├── tests/                # Pytest directory
├── Dockerfile            # Containerization
├── docker-compose.yml    # Compose for easy startup
├── .env.example          # Template for credentials
├── .gitignore
├── cli.py                # Main Typer CLI entry point
├── requirements.txt
└── README.md
```

## Installation

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Configure .env
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your API credentials:
```
BINANCE_API_KEY=your_key
BINANCE_SECRET_KEY=your_secret
BINANCE_BASE_URL=https://testnet.binancefuture.com
```

## Run Examples

Use the interactive CLI. See help via:
```bash
python cli.py --help
```

**MARKET Order Example**:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**LIMIT Order Example**:
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 105000
```

## Docker Usage

To run the bot in an isolated Docker container without polluting your host environment:

1. Ensure `.env` is configured.
2. Build and run a command via `docker-compose`:
```bash
docker-compose run --rm trading-bot trade --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

The logs will automatically be saved to your host's `./logs/trading.log` directory via a volume mount.

## Assumptions

- Python 3.11+ is installed.
- API Keys provided belong to the Binance Futures Testnet.
- The `pytest` framework is used for testing.

## Troubleshooting

- **Missing Credentials**: Ensure your `.env` file is loaded correctly and you've replaced the placeholder strings.
- **API Timestamp Error**: If Binance returns a Timestamp or Signature error, make sure your system clock is correctly synchronized.
- **Network Failures**: The bot will gracefully log and raise a `NetworkError`. Check your internet connection or if the Testnet is currently under maintenance.
