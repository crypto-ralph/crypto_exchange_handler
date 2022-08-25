"""
Module contains template class ExchangeAPI from which every
exchange class should derive to keep common output of methods.
"""

import csv
from enum import Enum
from typing import Optional, Tuple, Dict


class MarketSide(Enum):
    """
    Class representing market side for various requests i.e. klines or orderbook.
    """
    ASK = "asks"
    BID = "bids"
    LATEST = "latest"


class ExchangeAPI:
    """
    A base class for every exchange specific class.
    Defines common methods and contains common parameters.

    Attributes
    ----------
    name : str
        lowercase name of exchange
    access_key : str
        public API key
    secret_key : str
        private API key
    api_passphrase : str optional
        oassphrase required by some exchanges

    Methods
    -------
    """

    def __init__(
        self, name, access_key: str, secret_key: str, api_passphrase: Optional[str] = None
    ):
        """
        Constructs all the necessary attributes for the ExchangeAPI object.

        Parameters
        ----------
        name : str
            lowercase name of exchange
        access_key : str
            public API key
        secret_key : str
            private API key
        api_passphrase : str optional
            oassphrase required by some exchanges
        """
        self.name = name.lower()
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_passphrase = api_passphrase

    def get_all_balances(self) -> Optional[Dict[str, str]]:
        """
        Gets all balances available on account.

        :return: Dictionary with coin - balance pair
        """
        raise NotImplementedError

    def get_balance(self, coin: str) -> Optional[str]:
        """
        Gets balance of coin specified in parameter.

        :param coin: str with coin name
        :return: str representing coin balance. If there is no such coin returns None
        """
        raise NotImplementedError

    def get_available_markets(self) -> Optional[Tuple[str, ...]]:
        """
        Gets tuple of markets available on target exchange.
        :return: Tuple of available market.
        """
        raise NotImplementedError

    def get_coin_price(
        self, coin: str, quote: str = "BTC", price_type: MarketSide = MarketSide.ASK
    ) -> Optional[str]:
        """
        :param coin: currency to trade
        :param quote: quote currency
        :param price_type:
        :return:
        """
        raise NotImplementedError

    def get_coins_prices(
        self, coins: Tuple, quote: str = "BTC", price_type: MarketSide = MarketSide.ASK
    ) -> Optional[dict]:
        """
        :return:
        """
        raise NotImplementedError

    def get_order_book(self, coin: str, quote: str) -> Optional[dict]:
        """
        :param coin: currency to trade
        :param quote: quote currency
        :return:
        """
        raise NotImplementedError

    def withdraw_asset(self, asset: str, target_addr: str, amount: str):
        """
        Sends request for asset withdrawal to the exchange.

        :param asset:
        :param target_addr:
        :param amount:
        :return: None
        """
        raise NotImplementedError

    def create_order(self, market, side, price, amount):
        """
        Send request to create order on target exchange
        :param market:
        :param side:
        :param price:
        :param amount:
        :return:
        """
        raise NotImplementedError

    def create_market_order(  # pylint: disable=too-many-arguments
        self,
        side: str,
        coin: str,
        quote: str,
        size: Optional[str] = None,
        amount: Optional[str] = None,
    ):
        """
        Send trade request to buy or sell at the market's current best available price.
        :param side: buy or sell
        :param coin: currency to trade
        :param quote: quote currency
        :param size: amount of base currency to use
        :param amount: amount of quote currency to use
        :return:
        """

    def get_candles(  # pylint: disable=too-many-arguments
        self,
        coin: str,
        quote: str,
        interval: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[tuple]:
        """
        Gets market historical data in form of candles represented by dictionary
        :param coin:
        :param quote:
        :param interval:
        :param start: start time for data in format %Y-%m-%d
        :param end: end time for data in format %Y-%m-%d
        :return: tuple of kline dictionaries in format:
                {
                    "ts": int,
                    "open": float, open price of current interval
                    "close": float, close price of current interval
                    "high": float, highest price of current interval
                    "low": float, lowest price of current interval
                }
        """
        raise NotImplementedError

    def get_last_candles(
        self, coin: str, quote: str, interval: str, amount: int
    ) -> Optional[tuple]:
        """

        :param coin:
        :param quote:
        :param interval:
        :param amount:
        :return:
        """
        raise NotImplementedError

    def dump_market_data_to_file(  # pylint: disable=too-many-arguments
        self,
        coin: str,
        quote: str,
        interval: str = "30m",
        file: str = "data.csv",
        amount=None,
        start: str = None,
        end: str = None,
    ):
        """
        Creates .csv file with market data gathered from exchange API.

        :param coin:
        :param quote:
        :param interval:
        :param file:
        :param amount:
        :param start:
        :param end:
        :return:
        """

        if amount is not None:
            candles = self.get_last_candles(coin, quote, interval, amount)
        else:
            if start is not None:
                candles = self.get_candles(coin, quote, interval, start, end)
            else:
                print("ERROR: Wrong paramaters. Provide amount or start")
                return

        with open(file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(list(candles[0].keys()))
            for line in candles:
                writer.writerow(list(line.values()))

    @staticmethod
    def load_market_data_file(file) -> Optional[tuple]:
        """
        Parse and load existing file created using dump_market_data_to_file method.

        :param file: path to file to be parsed
        :return: tuple with candles data loaded from file
        """
        if file.find(".csv") == -1:
            print("ERROR: Please provide .csv file")
            return None

        candles = []

        with open(file, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0

            for row in csv_reader:
                if line_count != 0:
                    temp = {
                        "ts": float(row[0]),
                        "open": float(row[1]),
                        "high": float(row[2]),
                        "low": float(row[3]),
                        "close": float(row[4]),
                    }
                    candles.append(temp)
                    line_count += 1
                else:
                    line_count += 1
        return tuple(candles)
