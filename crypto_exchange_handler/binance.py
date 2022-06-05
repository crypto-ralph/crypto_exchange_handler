import time
from typing import Optional

from binance.exceptions import BinanceRequestException
from binance.client import Client

from . import exchange_template


class Binance(exchange_template.ExchangeAPI):
    def __init__(self, access_key: str, secret_key: str):
        super().__init__("binance", access_key, secret_key)
        self.client = Client(self.access_key, self.secret_key)

    def get_balance(self, coin) -> Optional[str]:
        info = self.client.get_account()
        for balance in info["balances"]:
            if balance["asset"] == coin.upper():
                return balance["free"]
        return None

    def get_all_balances(self) -> dict:
        """
        Gets all balances available on account.

        :return: Dictionary with coin - balance pair
        """
        info = self.client.get_account()
        result = {}
        for asset in info["balances"]:
            total = float(asset["free"]) + float(asset["locked"])
            if total != 0:
                result[asset["asset"]] = "{:.10f}".format(total)
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
        return self.get_symbol_info(symbol)

    def get_symbol_ticker(self) -> dict:
        return {symbol["symbol"]: symbol["price"] for symbol in self.client.get_symbol_ticker()}

    def get_coins_prices(self, side: str = "ask") -> Optional[dict]:
        ticker = None
        for i in range(4):
            ticker = self.client.get_orderbook_tickers()
            if ticker is not None:
                break
            else:
                time.sleep(1)
                print("Try again: " + str(i) + "/4")

        if ticker is None:
            return None

        coins = {}
        for item in ticker:
            index = item["symbol"].find("BTC")
            if index != -1:
                if item["symbol"][:index] != "":
                    if side == "ask":
                        coins[item["symbol"][:index]] = item["askPrice"]
                    elif side == "bid":
                        coins[item["symbol"][:index]] = item["bidPrice"]
        return coins

    def get_coin_price(self, coin: str, pair: str = "BTC", side: str = "ask"):
        try:
            tickers = self.client.get_orderbook_tickers()
        except BinanceRequestException:
            print("ERROR: Could not get ticker")
            return -1

        for ticker in tickers:
            if ticker["symbol"] == coin.upper() + pair.upper():
                if side == "ask":
                    return ticker["askPrice"]
                elif side == "bid":
                    return ticker["bidPrice"]

    def get_order_book(self, symbol, side):
        order_book = self.client.get_order_book(symbol=symbol.upper())
        return order_book[side]

    def get_candles(self, symbol: str, interval: str, start: str, end: str = None) -> tuple:
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
