# 🤖 Binance Futures Testnet Trading Bot

A Python CLI trading bot for Binance Futures Testnet (USDT-M).
Supports Market, Limit, and Stop-Market orders with full logging.

## Setup

1. Clone the repo
2. Install dependencies:
   pip install -r requirements.txt

3. Create .env file:
   BINANCE_API_KEY=your_key
   BINANCE_SECRET_KEY=your_secret

4. Get keys from: https://testnet.binancefuture.com

## Run Examples

Market BUY:
   python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

Limit SELL:
   python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 95000

Stop Market BUY:
   python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.01 --stop-price 90000

## Project Structure

trading_bot/
  bot/
    __init__.py         → package init
    logging_config.py   → logging setup
    validators.py       → input validation
    client.py           → Binance API client
    orders.py           → order logic
  cli.py                → CLI entry point
  logs/                 → auto-generated log files
  .env                  → your API keys
  requirements.txt      → dependencies

## Assumptions

- Uses Binance Futures Testnet only (not real money)
- Supported symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- Python 3.11+ recommended