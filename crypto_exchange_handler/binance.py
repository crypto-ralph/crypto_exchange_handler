"""
Module contains class implementing handling API request for Binance exchange.
Exhange address:   https://www.binance.com/
Api documentation: https://binance-docs.github.io/apidocs/spot/en/
"""

import time
from typing import Optional, Tuple, Dict

from binance.exceptions import BinanceRequestException
from binance.client import Client

from . import exchange_template


class Binance(exchange_template.ExchangeAPI):
    """
    Class handles connection ot the Binance crypto exchange API.
    """

    def __init__(self, access_key: str, secret_key: str):
        super().__init__("binance", access_key, secret_key)
        self.client = Client(self.access_key, self.secret_key)

    def get_balance(self, coin: str) -> Optional[str]:
        """
        :param coin: coin abbreviation for which balance will be returned
        :type coin: str
        :return: String representing float value of balance on account
        :rtype: str if there is such currency listed, otherwise None
        """
        info = self.client.get_account()
        for asset in info["balances"]:
            if asset["asset"] == coin.upper():
                total = float(asset["free"]) + float(asset["locked"])
                return f"{total:.10f}"
        return None

    def get_all_balances(self) -> Optional[Dict[str, str]]:
        info = self.client.get_account()
        result = {}
        for asset in info["balances"]:
            total = float(asset["free"]) + float(asset["locked"])
            if total != 0:
                result[asset["asset"]] = f"{total:.10f}"
        return result

    def withdraw_asset(self, asset, target_addr, amount):
        result = self.client.withdraw(asset=asset, address=target_addr, amount=amount)
        return result

    def get_available_markets(self):
        available_markets = []
        ticker = self.client.get_symbol_ticker()
        for item in ticker:
            index = item["symbol"].find("BTC")
            if index != -1:
                if item["symbol"][:index] != "":
                    available_markets.append(item["symbol"][:index])
        return available_markets

    def get_symbol_info(self, symbol: str) -> Optional[dict]:
        """
        Gets symbol info from API
        :param symbol: cryptocurrency symbol as a string
        :return:
        """
        return self.get_symbol_info(symbol)

    def get_symbol_ticker(self) -> dict:
        """
        Gets actual ticker from API.
        :return: dict
        """
        return {symbol["symbol"]: symbol["price"] for symbol in self.client.get_symbol_ticker()}

    def get_coins_prices(
        self, coins: Tuple, pair: str = "BTC", price_type: str = "ask"
    ) -> Optional[dict]:
        ticker = None
        for i in range(4):
            ticker = self.client.get_orderbook_tickers()
            if ticker is None:
                time.sleep(1)
                print("Try again: " + str(i) + "/4")
            else:
                break

        if ticker is None:
            return None

        coins = {}
        for item in ticker:
            index = item["symbol"].find("BTC")
            if index != -1:
                if item["symbol"][:index] != "":
                    if price_type == "ask":
                        coins[item["symbol"][:index]] = item["askPrice"]
                    elif price_type == "bid":
                        coins[item["symbol"][:index]] = item["bidPrice"]
        return coins

    def get_coin_price(
        self, coin: str, pair: str = "BTC", price_type: str = "ask"
    ) -> Optional[str]:
        try:
            tickers = self.client.get_orderbook_tickers()
        except BinanceRequestException:
            print("ERROR: Could not get ticker")
            return None
        pair = coin.upper() + pair.upper()
        for ticker in tickers:
            if ticker["symbol"] == pair:
                if price_type == "ask":
                    return ticker["askPrice"]
                if price_type == "bid":
                    return ticker["bidPrice"]

        print(
            f"ERROR: Pair: {pair} not found in available tickers. Use get_available_markets"
            f" to check if pair is available"
        )
        return None

    def get_order_book(self, market, side):
        order_book = self.client.get_order_book(symbol=market.upper())
        return order_book[side]

    def get_candles(
        self, symbol: str, interval: str, start: Optional[str] = None, end: Optional[str] = None
    ) -> Optional[tuple]:
        candles = []

        klines = self.client.get_historical_klines(
            symbol=symbol, interval=interval, start_str=start, end_str=end
        )
        for candle in klines:
            temp = {
                "ts": int(candle[0]),
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4]),
            }
            candles.append(temp)
        return tuple(candles)

    def get_last_candles(self, symbol, interval, amount):
        candles = []
        klines = self.client.get_klines(symbol=symbol, interval=interval, limit=amount)

        for i in range(2):
            print(f"test {i}")

        for candle in klines:
            temp = {
                "ts": int(candle[0]),
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4]),
            }
            candles.append(temp)
        return candles

    def create_order(self, market, side, price, amount):
        print(f"ERROR: {self.name} client - Not implemented")
