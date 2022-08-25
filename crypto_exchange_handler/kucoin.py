"""
Module contains class implementing handling API request for Kucoin exchange.
Exhange address:  https://www.kucoin.com/
Api documentation: https://docs.kucoin.com/
"""
import json
from typing import Optional, Dict, Tuple
import time
import hmac
import base64
import hashlib
import requests

from .exchange_template import ExchangeAPI, MarketSide


# fmt: off
HTTP_error_codes = {
    "400": "Bad Request -- Invalid request format.",
    "401": "Unauthorized -- Invalid API Key.",
    "403": "Forbidden or Too Many Requests -- The request is forbidden or Access limit breached.",
    "404": "Not Found -- The specified resource could not be found.",
    "405": "Method Not Allowed -- You tried to access the resource with an invalid method.",
    "415": "Unsupported Media Type. You need to use: application/json.",
    "500": "Internal Server Error -- We had a problem with our server. Try again later.",
    "503": "Service Unavailable -- We're temporarily offline for maintenance. "
           "Please try again later.",
}

SYSTEM_codes = {
    "200000": "Success",
    "200001": "Order creation for this pair suspended",
    "200002": "Order cancel for this pair suspended",
    "200003": "Number of orders breached the limit",
    "200009": "Please complete the KYC verification before you trade XX",
    "200004": "Balance insufficient",
    "400000": "Bad request",
    "400001": "Any of KC-API-KEY, KC-API-SIGN, KC-API-TIMESTAMP, KC-API-PASSPHRASE "
              "is missing in your request header",
    "400002": "KC-API-TIMESTAMP Invalid",
    "400003": "KC-API-KEY not exists",
    "400004": "KC-API-PASSPHRASE error",
    "400005": "Signature error",
    "400006": "The requested ip address is not in the api whitelist",
    "400007": "Access Denied",
    "404000": "Url Not Found",
    "400100": "Parameter Error",
    "400200": "Forbidden to place an order",
    "400500": "Your located country/region is currently not "
              "supported for the trading of this token",
    "400700": "Transaction restricted, there's a risk problem in your account",
    "400800": "Leverage order failed",
    "411100": "User are frozen",
    "500000": "Internal Server Error",
    "900001": "symbol not exists",
}

valid_intervals = (
    "1min", "3min", "5min", "15min", "30min",
    "1hour", "2hour", "4hour", "6hour", "8hour",
    "12hour", "1day", "1week"
)
# fmt: off

kucoin_codes = {
    **HTTP_error_codes,
    **SYSTEM_codes,
}


def is_response_valid(response: dict) -> bool:
    """
    Checks if data received from exchange is correct.

    :param response: response data from API
    :return: Boolean value representing validity of response
    """
    if response["code"] != "200000":
        print(f'ERROR: code: {response["code"]}, msg: {kucoin_codes[response["code"]]}')
        return False
    return True


class Kucoin(ExchangeAPI):
    """
    Class handles connection ot the KuCoin crypto exchange API.
    """
    order_id_num: int = 0

    def __init__(self, access_key: str, secret_key: str, api_passphrase: str):
        super().__init__("kucoin", access_key, secret_key, api_passphrase)
        self.api_addr = "https://api.kucoin.com"

    def send_priv_request(self, addr: str,
                          data: Optional[dict] = None,
                          req_type: str = "get") -> Optional[dict]:
        """
        Implementation of communication whith exchange API.
        :param addr: endpoint for request
        :param req_type: method of the request [post, get]
        :param data: data for request
        :return: json data with response
        """

        json_data = json.dumps(data) if data else ""
        now = int(time.time() * 1000)
        str_to_sign = str(now) + req_type.upper() + "/api/v1/" + addr + json_data
        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode('utf-8'),
                str_to_sign.encode('utf-8'),
                hashlib.sha256,
            ).digest()
        )

        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.access_key,
            "KC-API-PASSPHRASE": self.api_passphrase,
            "Content-Type": "application/json",
        }

        endpoint_addr = f'{self.api_addr}/api/v1/{addr}'
        if req_type == "get":
            response = requests.get(endpoint_addr, headers=headers, params=data)
        elif req_type == "post":
            response = requests.post(endpoint_addr, headers=headers, data=json_data)
        else:
            print(
                f"ERROR: Invalid request type: {req_type}. Use only ['post', 'get']"
            )
            return None

        return response.json()

    def get_all_balances(self) -> Optional[Dict[str, str]]:
        data = self.send_priv_request("accounts")
        if not is_response_valid(data):
            return None

        result = {}
        for item in data["data"]:
            if item["currency"] in result:
                coin_balance = float(item["balance"]) + float(result[item["currency"]])
                result[item["currency"]] = f"{coin_balance:.10f}"
            else:
                result[item["currency"]] = f"{float(item['balance']):.10f}"
        return result

    def get_balance(self, coin: str) -> Optional[str]:
        data = self.send_priv_request("accounts")
        if not is_response_valid(data):
            return None

        result = 0
        for item in data["data"]:
            if item["currency"] == coin:
                result += float(item["balance"])
        return f"{result:.10f}"

    def get_available_markets(self) -> Optional[Tuple[str, ...]]:
        data = self.send_priv_request("symbols")
        if not is_response_valid(data):
            return None
        return tuple((pair["symbol"].replace("-", "") for pair in data["data"]))

    def get_coin_price(self, coin: str,
                       quote: str = "BTC",
                       price_type: MarketSide = MarketSide.ASK) -> Optional[str]:

        pair = f"{coin.upper()}-{quote.upper()}"

        data = self.send_priv_request(
            "market/orderbook/level1",
            {
                "symbol": f"{pair}"
            }
        )

        if not is_response_valid(data):
            return None

        if data["data"]:
            if price_type == MarketSide.ASK:
                return data["data"]["bestAsk"]
            if price_type == MarketSide.BID:
                return data["data"]["bestBid"]
            if price_type == MarketSide.LATEST:
                return data["data"]["price"]
        else:
            print(
                f"ERROR: Coin: {pair} not found in available tickers. "
                f"Use get_available_markets to check if pair is available"
            )
            return None

        print(f"ERROR: Wrong price type: {price_type}\nAvailable values: [ask, bid, latest]")
        return None

    def get_coins_prices(
            self, coins: Tuple, quote: str = "BTC", price_type: MarketSide = MarketSide.ASK
    ) -> Optional[dict]:
        data = self.send_priv_request("market/allTickers")

        if not is_response_valid(data):
            return None

        symbols_list = [f"{coin.upper()}-{quote.upper()}" for coin in coins]
        result = {}

        for ticker in data["data"]["ticker"]:
            if ticker["symbol"] in symbols_list:
                if price_type == MarketSide.ASK:
                    result[ticker["symbol"]] = ticker["sell"]
                if price_type == MarketSide.BID:
                    result[ticker["symbol"]] = ticker["buy"]
                if price_type == MarketSide.LATEST:
                    result[ticker["symbol"]] = ticker["last"]
        return result

    def get_order_book(self, coin: str, quote: str) -> Optional[dict]:
        data = self.send_priv_request("market/orderbook/level2_100",
                                      {"symbol": f"{coin.upper()}-{quote.upper()}"}
                                      )

        if not is_response_valid(data):
            return None

        return {
            MarketSide.ASK: data["data"][MarketSide.ASK.value],
            MarketSide.BID: data["data"][MarketSide.BID.value]
        }

    def withdraw_asset(self, asset: str, target_addr: str, amount: str):
        print(f"ERROR: {self.name} client - Not implemented")

    def create_order(self, market: str, side: str, price: str, amount: str):
        print(f"ERROR: {self.name} client - Not implemented")

    def create_market_order(
            self, side: str, coin: str, quote: str,
            size: Optional[str] = None, amount: Optional[str] = None
    ):
        if size is not None and amount is not None:
            print("ERROR: Choose only one of the params.")
            return None

        if size is None and amount is None:
            print("ERROR: Fill size or amount.")
            return None

        if side not in ("buy", "sell"):
            print("ERROR: Parameter side can only by 'buy' or 'sell'")
            return None

        params = {
            "clientOid": f"handler_{str(self.order_id_num)}",
            "side": side,
            "symbol": f"{coin.upper()}-{quote.upper()}",
            "type": "market",
        }

        if size:
            params["size"] = size

        if amount:
            params["amount"] = amount

        self.order_id_num += 1
        response = self.send_priv_request("orders", data=params, req_type="post")
        if not is_response_valid(response):
            return None
        return response

    def get_candles(
            self,
            coin: str,
            quote: str,
            interval: str,
            start: Optional[str] = None,
            end: Optional[str] = None,
    ) -> Optional[tuple]:
        if interval not in valid_intervals:
            print(f"ERROR: Invalid interval. Valid intervals are: {valid_intervals}")
            return None

        params = {
            "symbol": f"{coin.upper()}-{quote.upper()}",
            "type": f"{interval}",
        }

        if start:
            time_start = time.strptime(start, "%Y-%m-%d")
            params["startAt"] = str(int(time.mktime(time_start)))

        if end:
            time_end = time.strptime(end, "%Y-%m-%d")
            params["endAt"] = str(int(time.mktime(time_end)))

        data = self.send_priv_request("market/candles", data=params)
        if not is_response_valid(data):
            return None

        klines = [
            {
                "ts": int(candle[0]),
                "open": float(candle[1]),
                "close": float(candle[2]),
                "high": float(candle[3]),
                "low": float(candle[4]),
            }
            for candle in data["data"]]

        return tuple(klines)

    def get_last_candles(
            self, coin: str, quote: str, interval: str, amount: int
    ) -> Optional[tuple]:
        if amount > 100:
            print("ERROR: Max number of last candles is 100")
            return None
        return self.get_candles(coin, quote, interval)[-amount:]
