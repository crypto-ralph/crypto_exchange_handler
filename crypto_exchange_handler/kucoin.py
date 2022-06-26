"""
Module contains class implementing handling API request for Kucoin exchange.
Exhange address:  https://www.kucoin.com/
Api documentation: https://docs.kucoin.com/
"""
from typing import Optional, Dict, Tuple
import time
import hmac
import base64
import hashlib
import requests

from . import exchange_template


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


class Kucoin(exchange_template.ExchangeAPI):
    """
    Class handles connection ot the KuCoin crypto exchange API.
    """
    def __init__(self, access_key: str, secret_key: str, api_passphrase: str):
        super().__init__("kucoin", access_key, secret_key, api_passphrase)
        self.api_addr = "https://api.kucoin.com"

    def send_priv_request(self, addr: str,
                          data: Optional[dict] = None) -> dict:
        """
        Implementation of communication whith exchange API.
        :param addr: endpoint for request
        :param req_type: data for request
        :param data: data for request
        :return: json data with response
        """

        req_type = "GET"

        def build_data_string(_data: dict) -> str:
            result = "?"
            for param, value in _data.items():
                result += f'{param}={value}&'

            return result[:-1]

        if data:
            data_str = build_data_string(data)
        else:
            data_str = ""

        now = int(time.time() * 1000)
        str_to_sign = str(now) + req_type + "/api/v1/" + addr + data_str
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

        addr = f'{self.api_addr}/api/v1/{addr}{data_str}'
        response = requests.request("get", f"{addr}", headers=headers)

        return response.json()

    def get_all_balances(self) -> Optional[Dict[str, str]]:
        data = self.send_priv_request("accounts")
        if not is_response_valid(data):
            return None

        result = {}
        for coin in data["data"]:
            if coin["currency"] in result:
                coin_balance = float(coin["balance"]) + float(result[coin["currency"]])
                result[coin["currency"]] = f"{coin_balance:.10f}"
            else:
                result[coin["currency"]] = f"{float(coin['balance']):.10f}"
        return result

    def get_balance(self, coin: str):
        print(f"ERROR: {self.name} client - Not implemented")

    def get_available_markets(self) -> Optional[Tuple[str, ...]]:
        data = self.send_priv_request("symbols")
        if not is_response_valid(data):
            return None
        return tuple((pair["symbol"] for pair in data["data"]))

    def get_coin_price(self, coin: str,
                       pair: str = "BTC",
                       price_type: str = "ask") -> Optional[str]:

        pair = coin.upper() + pair.upper()

        data = self.send_priv_request(
            "market/orderbook/level1",
            {
                "symbol": f"{pair}"
            }
        )

        if not is_response_valid(data):
            return None

        if data["data"]:
            if price_type == "ask":
                return data["data"]["bestAsk"]
            if price_type == "bid":
                return data["data"]["bestBid"]
            if price_type == "latest":
                return data["data"]["price"]
        else:
            print(
                f"ERROR: Pair: {pair} not found in available tickers. "
                f"Use get_available_markets to check if pair is available"
            )
            return None

        print(f"ERROR: Wrong price type: {price_type}\nAvailable values: [ask, bid, latest]")
        return None

    def get_coins_prices(
            self, coins: Tuple, pair: str = "BTC", price_type: str = "ask"
    ) -> Optional[dict]:
        data = self.send_priv_request("market/allTickers")

        if not is_response_valid(data):
            return None

        symbols_list = [f"{coin.upper()}-{pair.upper()}" for coin in coins]
        result = {}

        for ticker in data["data"]["ticker"]:
            if ticker["symbol"] in symbols_list:
                if price_type == "ask":
                    result[ticker["symbol"]] = ticker["sell"]
                if price_type == "bid":
                    result[ticker["symbol"]] = ticker["buy"]
                if price_type == "latest":
                    result[ticker["symbol"]] = ticker["last"]
        return result

    def get_order_book(self, market: str, side: str):
        print(f"ERROR: {self.name} client - Not implemented")

    def withdraw_asset(self, asset: str, target_addr: str, amount: str):
        print(f"ERROR: {self.name} client - Not implemented")

    def create_order(self, market: str, side: str, price: str, amount: str):
        print(f"ERROR: {self.name} client - Not implemented")

    def get_candles(
        self, symbol: str, interval: str, start: Optional[str] = None, end: Optional[str] = None
    ) -> Optional[tuple]:

        if interval not in valid_intervals:
            print(f"ERROR: Invalid interval. Valid intervals are: {valid_intervals}")
            return None

        if "-" not in symbol:
            print("ERROR: Wrong symbol pattern. Correct pattern is <COIN>-<PAIR>")
            return None

        params = {
            "symbol": f"{symbol}",
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

    def get_last_candles(self, symbol: str, interval: str, amount):
        print(f"ERROR: {self.name} client - Not implemented")
