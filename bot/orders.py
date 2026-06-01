from bot.client import BinanceClient
from bot.logging_config import get_logger

logger = get_logger("orders")

def place_market_order(client, symbol, side, quantity):
    logger.info(f"Placing MARKET {side} order - {symbol} qty={quantity}")
    params = {"symbol": symbol, "side": side, "type": "MARKET", "quantity": quantity}
    response = client.place_order(params)
    logger.info(f"MARKET order placed successfully - orderId={response.get('orderId')}")
    return response

def place_limit_order(client, symbol, side, quantity, price):
    logger.info(f"Placing LIMIT {side} order - {symbol} qty={quantity} price={price}")
    params = {"symbol": symbol, "side": side, "type": "LIMIT", "quantity": quantity, "price": price, "timeInForce": "GTC"}
    response = client.place_order(params)
    logger.info(f"LIMIT order placed successfully - orderId={response.get('orderId')}")
    return response

def place_stop_market_order(client, symbol, side, quantity, stop_price):
    logger.info(f"Placing STOP {side} order - {symbol} qty={quantity} stopPrice={stop_price}")
    import math
    limit_price = round(float(stop_price) * 0.99, 1) if side == "BUY" else round(float(stop_price) * 1.01, 1)
    params = {
        "symbol": symbol,
        "side": side,
        "type": "STOP",
        "quantity": quantity,
        "price": limit_price,
        "stopPrice": stop_price,
        "timeInForce": "GTC"
    }
    response = client.place_order(params)
    logger.info(f"STOP order placed successfully - orderId={response.get('orderId')}")
    return response

def print_order_summary(order_type, symbol, side, quantity, price=None, stop_price=None):
    print("\n" + "="*50)
    print("        ORDER REQUEST SUMMARY")
    print("="*50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    if stop_price:
        print(f"  Stop Price : {stop_price}")
    print("="*50 + "\n")

def print_order_response(response):
    print("\n" + "="*50)
    print("        ORDER RESPONSE")
    print("="*50)
    print(f"  Order ID     : {response.get('orderId', 'N/A')}")
    print(f"  Symbol       : {response.get('symbol', 'N/A')}")
    print(f"  Side         : {response.get('side', 'N/A')}")
    print(f"  Type         : {response.get('type', 'N/A')}")
    print(f"  Status       : {response.get('status', 'N/A')}")
    print(f"  Executed Qty : {response.get('executedQty', 'N/A')}")
    print(f"  Avg Price    : {response.get('avgPrice', 'N/A')}")
    print(f"  Time in Force: {response.get('timeInForce', 'N/A')}")
    print("="*50)
    print("  SUCCESS - ORDER PLACED SUCCESSFULLY")
    print("="*50 + "\n")
