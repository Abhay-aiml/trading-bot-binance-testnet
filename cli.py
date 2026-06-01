import argparse
import os
import sys
from dotenv import load_dotenv
from bot.client import BinanceClient
from bot.logging_config import get_logger
from bot.orders import place_limit_order, place_market_order, place_stop_market_order, print_order_response, print_order_summary
from bot.validators import validate_inputs

load_dotenv()
logger = get_logger("cli")

def get_client():
    api_key = os.getenv("BINANCE_API_KEY")
    secret_key = os.getenv("BINANCE_SECRET_KEY")
    if not api_key or not secret_key:
        print("ERROR: API keys not found in .env file")
        sys.exit(1)
    return BinanceClient(api_key, secret_key)

def main():
    print("Binance Futures Testnet Trading Bot starting...")
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--quantity", required=True)
    parser.add_argument("--price", required=False)
    parser.add_argument("--stop-price", required=False, dest="stop_price")
    args = parser.parse_args()
    print(f"Received: symbol={args.symbol} side={args.side} type={args.type} qty={args.quantity}")
    try:
        symbol, side, order_type, quantity, price, stop_price = validate_inputs(
            symbol=args.symbol, side=args.side, order_type=args.type,
            quantity=args.quantity, price=args.price, stop_price=args.stop_price)
        print_order_summary(order_type, symbol, side, quantity, price, stop_price)
        client = get_client()
        if order_type == "MARKET":
            response = place_market_order(client, symbol, side, quantity)
        elif order_type == "LIMIT":
            response = place_limit_order(client, symbol, side, quantity, price)
        elif order_type == "STOP_MARKET":
            response = place_stop_market_order(client, symbol, side, quantity, stop_price)
        print_order_response(response)
    except ValueError as e:
        print(f"Validation Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Order Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
