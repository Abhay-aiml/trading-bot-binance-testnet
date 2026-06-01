import hashlib
import hmac
import time
from urllib.parse import urlencode
import requests
from bot.logging_config import get_logger

logger = get_logger("client")
BASE_URL = "https://testnet.binancefuture.com"

class BinanceClient:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key, "Content-Type": "application/json"})
        logger.info("BinanceClient initialized - connected to Testnet")

    def _sign(self, params):
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(self.secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        params["signature"] = signature
        return params

    def place_order(self, params):
        url = f"{BASE_URL}/fapi/v1/order"
        signed_params = self._sign(params)
        logger.debug(f"REQUEST POST {url} | params: { {k: v for k, v in signed_params.items() if k != 'signature'} }")
        try:
            response = self.session.post(url, params=signed_params, timeout=10)
            data = response.json()
            if response.status_code == 200:
                logger.debug(f"RESPONSE {response.status_code} | {data}")
                return data
            else:
                logger.error(f"API ERROR {response.status_code} | {data}")
                raise Exception(f"Binance API Error {response.status_code}: {data.get('msg', data)}")
        except requests.exceptions.ConnectionError:
            raise Exception("Network error - check your internet connection")
        except requests.exceptions.Timeout:
            raise Exception("Request timed out - Binance Testnet did not respond")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    def place_stop_order(self, params):
        url = f"{BASE_URL}/fapi/v1/order"
        params["type"] = "STOP_MARKET"
        params["workingType"] = "CONTRACT_PRICE"
        signed_params = self._sign(params)
        logger.debug(f"REQUEST POST {url} | params: { {k: v for k, v in signed_params.items() if k != 'signature'} }")
        try:
            response = self.session.post(url, params=signed_params, timeout=10)
            data = response.json()
            if response.status_code == 200:
                logger.debug(f"RESPONSE {response.status_code} | {data}")
                return data
            else:
                logger.error(f"API ERROR {response.status_code} | {data}")
                raise Exception(f"Binance API Error {response.status_code}: {data.get('msg', data)}")
        except requests.exceptions.ConnectionError:
            raise Exception("Network error - check your internet connection")
        except requests.exceptions.Timeout:
            raise Exception("Request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
