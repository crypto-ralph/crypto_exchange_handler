import time
import hmac
from typing import Optional, Dict, Tuple

import requests
import base64
import hashlib

from . import exchange_template

HTTP_error_codes = {
    "400": "Bad Request -- Invalid request format.",
    "401": "Unauthorized -- Invalid API Key.",
    "403": "Forbidden or Too Many Requests -- The request is forbidden or Access limit breached.",
    "404": "Not Found -- The specified resource could not be found.",
    "405": "Method Not Allowed -- You tried to access the resource with an invalid method.",
    "415": "Unsupported Media Type. You need to use: application/json.",
    "500": "Internal Server Error -- We had a problem with our server. Try again later.",
    "503": "Service Unavailable -- We're temporarily offline for maintenance. Please try again later.",
}

SYSTEM_codes = {
    "200000": "Success",
    "200001": "Order creation for this pair suspended",
    "200002": "Order cancel for this pair suspended",
    "200003": "Number of orders breached the limit",
    "200009": "Please complete the KYC verification before you trade XX",
    "200004": "Balance insufficient",
    "400001": "Any of KC-API-KEY, KC-API-SIGN, KC-API-TIMESTAMP, KC-API-PASSPHRASE is missing in your request header",
    "400002": "KC-API-TIMESTAMP Invalid",
    "400003": "KC-API-KEY not exists",
    "400004": "KC-API-PASSPHRASE error",
    "400005": "Signature error",
    "400006": "The requested ip address is not in the api whitelist",
    "400007": "Access Denied",
    "404000": "Url Not Found",
    "400100": "Parameter Error",
    "400200": "Forbidden to place an order",
    "400500": "Your located country/region is currently not supported for the trading of this token",
    "400700": "Transaction restricted, there's a risk problem in your account",
    "400800": "Leverage order failed",
    "411100": "User are frozen",
    "500000": "Internal Server Error",
    "900001": "symbol not exists",
}

kucoin_codes = {
    **HTTP_error_codes,
    **SYSTEM_codes,
}


def is_response_valid(response: dict) -> bool:
    if response["code"] != "200000":
        print(f'ERROR: code: {response["code"]}, msg: {kucoin_codes[response["code"]]}')
        return False
    return True


class Kucoin(exchange_template.ExchangeAPI):
    def __init__(self, access_key: str, secret_key: str, api_passphrase: str):
        super().__init__("kucoin", access_key, secret_key, api_passphrase)
        self.api_addr = "https://api.kucoin.com"

    def send_priv_request(self, addr: str, req_type: str = "GET"):
        now = int(time.time() * 1000)
        str_to_sign = str(now) + req_type + "/api/v1/" + addr
        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode("utf-8"),
                str_to_sign.encode("utf-8"),
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

        addr = self.api_addr + "/api/v1/" + addr
        response = requests.request("get", addr, headers=headers)
        return response.json()

    def get_all_balances(self) -> Optional[Dict[str, str]]:
        data = self.send_priv_request("accounts")
        if not is_response_valid(data):
            return None

        result = {}
        for coin in data["data"]:
            if coin["currency"] in result:
                result[coin["currency"]] = "{:.10f}".format(float(coin["balance"]) + float(result[coin["currency"]]))
            else:
                result[coin["currency"]] = "{:.10f}".format(float(coin["balance"]))
        return result

    def get_balance(self, coin: str):
        print(f"ERROR: {self.name} client - Not implemented")
        return None

    def get_available_markets(self) -> Optional[Tuple[str, ...]]:
        data = self.send_priv_request("symbols")
        if not is_response_valid(data):
            return None
        return tuple((pair["symbol"] for pair in data["data"]))

    def get_coin_price(self, coin: str, pair: str = "BTC"):
        print(f"ERROR: {self.name} client - Not implemented")
        return None

    def get_coins_prices(self):
        print(f"ERROR: {self.name} client - Not implemented")
        return None

    def get_order_book(self, market: str, side: str):
        print(f"ERROR: {self.name} client - Not implemented")
        return None

    def withdraw_asset(self, asset: str, target_addr: str, amount: str):
        print(f"ERROR: {self.name} client - Not implemented")
        return None

    def create_order(self, market: str, side: str, price: str, amount: str):
        print(f"ERROR: {self.name} client - Not implemented")
        return None

    def get_candles(self, symbol: str, interval: str, start: str, end: str = None) -> Optional[tuple]:
        print(f"ERROR: {self.name} client - Not implemented")
        return None

    def get_last_candles(self, symbol: str, interval: str, amount):
        print(f"ERROR: {self.name} client - Not implemented")
        return None
