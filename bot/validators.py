from bot.logging_config import get_logger

logger = get_logger("validators")

VALID_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP_MARKET"]


def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if symbol not in VALID_SYMBOLS:
        logger.error(f"Invalid symbol: {symbol}. Must be one of {VALID_SYMBOLS}")
        raise ValueError(f"Invalid symbol '{symbol}'. Allowed: {', '.join(VALID_SYMBOLS)}")
    return symbol


def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in VALID_SIDES:
        logger.error(f"Invalid side: {side}")
        raise ValueError(f"Invalid side '{side}'. Must be BUY or SELL")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        logger.error(f"Invalid order type: {order_type}")
        raise ValueError(f"Invalid order type '{order_type}'. Allowed: {', '.join(VALID_ORDER_TYPES)}")
    return order_type


def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError()
    except ValueError:
        logger.error(f"Invalid quantity: {quantity}")
        raise ValueError(f"Quantity must be a positive number. Got: '{quantity}'")
    return qty


def validate_price(price: str) -> float:
    try:
        p = float(price)
        if p <= 0:
            raise ValueError()
    except ValueError:
        logger.error(f"Invalid price: {price}")
        raise ValueError(f"Price must be a positive number. Got: '{price}'")
    return p


def validate_inputs(symbol, side, order_type, quantity, price=None, stop_price=None):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)

    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        price = validate_price(price)

    if order_type == "STOP_MARKET":
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_MARKET orders")
        stop_price = validate_price(stop_price)

    logger.debug(f"Validation passed — symbol={symbol} side={side} type={order_type} qty={quantity} price={price} stop={stop_price}")
    return symbol, side, order_type, quantity, price, stop_price
