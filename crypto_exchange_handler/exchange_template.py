import csv
from typing import Optional, Tuple, Dict


class ExchangeAPI:
    def __init__(self, name, access_key: str, secret_key: str, api_passphrase: Optional[str] = None):
        self.name = name
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_passphrase = api_passphrase

    ###########################################################
    # API Functions
    # Getters
    # Abstract, need to be overriden
    ###########################################################

    def get_all_balances(self) -> Optional[Dict[str, str]]:
        raise NotImplementedError

    def get_balance(self, coin: str):
        raise NotImplementedError

    def get_available_markets(self) -> Optional[Tuple[str, ...]]:
        raise NotImplementedError

    def get_coin_price(self, name, pair="BTC"):
        raise NotImplementedError

    def get_coins_prices(self):
        raise NotImplementedError

    def get_order_book(self, market, side):
        raise NotImplementedError

    ###########################################################
    # Actions
    ###########################################################

    def withdraw_asset(self, asset, target_addr, amount):
        raise NotImplementedError

    def create_order(self, market, side, price, amount):
        raise NotImplementedError

    def get_candles(self, symbol: str, interval: str, start: str, end: str = None) -> tuple:
        raise NotImplementedError

    def get_last_candles(self, symbol: str, interval: str, amount):
        raise NotImplementedError

    ###########################################################
    # Data processing - Do not override!
    ###########################################################

    def dump_market_data_to_file(
        self,
        symbol: str,
        interval: str = "30m",
        file: str = "data.csv",
        amount=None,
        start: str = None,
        end: str = None,
    ):

        if amount is not None:
            candles = self.get_last_candles(symbol, interval, amount)
        else:
            if start is not None:
                candles = self.get_candles(symbol, interval, start, end)
            else:
                print("ERROR: Wrong paramaters. Provide amount or start")
                return

        with open(file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
            templist = [x for x in candles[0].keys()]
            writer.writerow(templist)

            for line in candles:
                templist.clear()
                for x in line.values():
                    templist.append(x)
                writer.writerow(templist)

    @staticmethod
    def load_market_data_file(file):
        if file.find(".csv") == -1:
            print("ERROR: Please provide .csv file")
            return -1

        candles = list()

        with open(file) as csv_file:
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
