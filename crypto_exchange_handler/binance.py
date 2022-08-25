"""
Module contains class implementing handling API request for Binance exchange.
Exhange address:   https://www.binance.com/
Api documentation: https://binance-docs.github.io/apidocs/spot/en/
"""

import time
from typing import Optional, Tuple, Dict

from binance.exceptions import BinanceRequestException, BinanceAPIException
from binance.client import Client

from . import exchange_template
from .exchange_template import MarketSide


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

    def get_available_markets(self) -> Tuple[str, ...]:
        markets = [item["symbol"] for item in self.client.get_symbol_ticker()]
        return tuple(markets)

    def get_listed_coins(self):
        """
        :return: list of all coins available on exchange
        """
        listed_coins = []
        ticker = self.client.get_symbol_ticker()

        for item in ticker:
            index = item["symbol"].find("BTC")
            if index != -1:
                if item["symbol"][:index] != "":
                    listed_coins.append(item["symbol"][:index])
        return listed_coins

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
        self, coins: Tuple, quote: str = "BTC", price_type: MarketSide = MarketSide.ASK
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
                    if price_type == MarketSide.ASK:
                        coins[item["symbol"][:index]] = item["askPrice"]
                    elif price_type == MarketSide.BID:
                        coins[item["symbol"][:index]] = item["bidPrice"]
        return coins

    def get_coin_price(
        self, coin: str, quote: str = "BTC", price_type: MarketSide = MarketSide.ASK
    ) -> Optional[str]:
        try:
            tickers = self.client.get_orderbook_tickers()
            print(tickers)
        except BinanceRequestException:
            print("ERROR: Could not get ticker")
            return None
        pair = coin.upper() + quote.upper()
        for ticker in tickers:
            if ticker["symbol"] == pair:
                if price_type == MarketSide.ASK:
                    return ticker["askPrice"]
                if price_type == MarketSide.BID:
                    return ticker["bidPrice"]

        print(
            f"ERROR: Pair: {pair} not found in available tickers. Use get_available_markets"
            f" to check if pair is available"
        )
        return None

    def get_order_book(self, coin: str, quote: str) -> Optional[dict]:
        try:
            order_book = self.client.get_order_book(symbol=f"{coin.upper()}{quote.upper()}")

            return {
                MarketSide.ASK: order_book[MarketSide.ASK.value],
                MarketSide.BID: order_book[MarketSide.BID.value],
            }
        except BinanceAPIException as exception:
            print(f"ERROR: {exception}")
            return None

    def get_candles(  # pylint: disable=too-many-arguments
        self,
        coin: str,
        quote: str,
        interval: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[tuple]:
        klines = self.client.get_historical_klines(
            symbol=f"{coin.upper()}{quote.upper()}",
            interval=interval,
            start_str=start,
            end_str=end,
        )
        candles = [
            {
                "ts": int(candle[0] / 1000),
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4]),
            }
            for candle in klines
        ]

        return tuple(candles)

    def get_last_candles(
        self, coin: str, quote: str, interval: str, amount: int
    ) -> Optional[tuple]:
        klines = self.client.get_klines(
            symbol=f"{coin.upper()}{quote.upper()}",
            interval=interval,
            limit=amount,
        )
        candles = [
            {
                "ts": int(candle[0]),
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4]),
            }
            for candle in klines
        ]

        return tuple(candles)

    def create_order(self, market, side, price, amount):
        print(f"ERROR: {self.name} client - Not implemented")
