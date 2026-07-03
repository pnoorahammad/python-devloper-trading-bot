# Binance Futures Testnet Trading Bot

A **production-grade** Python trading bot for Binance USDT-M Futures **Testnet/Demo Trading**. Supports MARKET and LIMIT orders via a clean CLI and a FastAPI REST API, with full structured logging, Docker support, and Render deployment.

---

## Features

- ✅ **MARKET and LIMIT orders** (BUY & SELL)
- ✅ **Automatic limit price adjustment** — if price is > 5% from market, auto-corrects to a valid tick-aligned price
- ✅ **Rich CLI** with formatted tables and progress spinners
- ✅ **FastAPI REST API** with `/order`, `/order/market`, `/order/limit` endpoints
- ✅ **Structured logging** — `logs/trading.log`, `logs/market_order.log`, `logs/limit_order.log`
- ✅ **Dockerized** — both CLI and API modes
- ✅ **Render deployment ready** via `render.yaml`
- ✅ **Full input validation** with custom exceptions
- ✅ **pytest test suite**

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/pnoorahammad/python-devloper-trading-bot.git
cd python-devloper-trading-bot
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

```bash
cp .env.example .env
```

Edit `.env` with your **Binance Futures Testnet** credentials:

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_SECRET_KEY=your_testnet_secret_key
BINANCE_BASE_URL=https://testnet.binancefuture.com
```

> Get credentials at: https://testnet.binancefuture.com

---

## CLI Usage

```bash
# Set PYTHONPATH first (Windows PowerShell)
$env:PYTHONPATH="."

# BUY MARKET order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# SELL LIMIT order (price auto-adjusted if unrealistic)
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 105000

# Help
python cli.py --help
```

### Sample CLI Output

```
+--------------------------+
|     Trading Request      |
| +----------------------+ |
| |     Symbol | BTCUSDT | |
| |       Side | BUY     | |
| | Order Type | MARKET  | |
| |   Quantity | 0.001   | |
| +----------------------+ |
+--------------------------+

+-----------------------------------------+
|                Response                 |
| +-------------------------------------+ |
| |      Order ID | 18691093016         | |
| |        Status | NEW                 | |
| |  Executed Qty | 0.0000              | |
| | Average Price | 0                   | |
| |     Timestamp | 2026-07-03 15:28:00 | |
| |        Result | Success             | |
| +-------------------------------------+ |
+-----------------------------------------+
```

---

## FastAPI Usage

### Start the API Server

```bash
$env:PYTHONPATH="."
uvicorn api:app --reload --port 8000
```

Visit the interactive docs: **http://localhost:8000/docs**

### API Endpoints

| Method | Endpoint        | Description                  |
|--------|----------------|------------------------------|
| GET    | `/`            | Health check                 |
| GET    | `/health`      | Health check                 |
| POST   | `/order`       | Place MARKET or LIMIT order  |
| POST   | `/order/market`| Place a MARKET order         |
| POST   | `/order/limit` | Place a LIMIT order          |

### Example Request

```bash
curl -X POST http://localhost:8000/order \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT", "side": "BUY", "type": "MARKET", "quantity": 0.001}'
```

### Example Response

```json
{
  "order_id": "18691093016",
  "symbol": "BTCUSDT",
  "side": "BUY",
  "order_type": "MARKET",
  "quantity": "0.001",
  "price": "0",
  "status": "NEW",
  "executed_qty": "0.0000",
  "avg_price": "0",
  "timestamp": 1751544480000,
  "result": "SUCCESS"
}
```

---

## Docker Usage

### Build and Run the FastAPI Server

```bash
docker compose up --build
```

The API will be available at **http://localhost:8000/docs**

### Run CLI Commands via Docker

```bash
# MARKET order
docker compose run --rm trading-cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# LIMIT order
docker compose run --rm trading-cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 105000
```

---

## Logging

All logs are written to the `logs/` directory:

| File                      | Contents                            |
|---------------------------|-------------------------------------|
| `logs/trading.log`        | Combined log — all executions       |
| `logs/market_order.log`   | Copy of log from MARKET order run   |
| `logs/limit_order.log`    | Copy of log from LIMIT order run    |

Log entries include: **timestamp**, **HTTP request**, **payload**, **response**, **errors**.

---

## Running Tests

```bash
$env:PYTHONPATH="."
pytest tests/ -v
```

---

## Deployment (Render)

The project includes `render.yaml` for one-click deployment on [Render](https://render.com).

1. Push this repository to GitHub.
2. Go to https://render.com → **New Web Service** → connect your GitHub repo.
3. Render will auto-detect `render.yaml`.
4. Add your `BINANCE_API_KEY` and `BINANCE_SECRET_KEY` as environment variables in Render's dashboard.
5. Deploy!

---

## Project Structure

```
├── api.py                  # FastAPI REST API wrapper
├── cli.py                  # Typer CLI entry point
├── bot/
│   ├── client.py           # Binance client initialization
│   ├── config.py           # Environment variable loading
│   ├── exceptions.py       # Custom exception hierarchy
│   ├── logging_config.py   # Structured logging setup
│   ├── orders.py           # Order placement logic
│   └── validators.py       # Input validation
├── tests/
│   └── test_validators.py  # pytest test suite
├── examples/
│   └── run_examples.sh     # Example shell scripts
├── logs/                   # Auto-created log files
├── Dockerfile              # Docker image (FastAPI server)
├── docker-compose.yml      # Docker Compose (API + CLI)
├── render.yaml             # Render deployment config
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

---

## Live Execution Evidence

Both orders were successfully executed on the **Binance USDT-M Futures Testnet**:

| Order Type | Symbol  | Side | Quantity | Order ID      | Status |
|------------|---------|------|----------|---------------|--------|
| MARKET     | BTCUSDT | BUY  | 0.001    | 18691093016   | NEW    |
| LIMIT      | BTCUSDT | SELL | 0.001    | 18691172755   | NEW    |

---

## License

MIT
