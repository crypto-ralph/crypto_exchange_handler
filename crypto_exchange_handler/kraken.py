import krakenex
from exchangeAPI import templateApi


class Kraken(templateApi.ExchangeAPI):
    def __init__(self, designation, name, access_key: str, secret_key: str):
        super().__init__(name, access_key, secret_key, designation)
        self.name = "kraken"
        self.designation = designation
        self.client = krakenex.API(key=access_key, secret=secret_key)

    ###########################################################
    # API Functions
    # Getters
    ###########################################################
    def get_all_balances(self):
        print("ERROR: " + self.name + "  Not implemented")
        return -1

    def get_balance(self, coin):
        print("ERROR: " + self.name + "  Not implemented")
        return -1

    def get_available_markets(self):
        available_markets = []
        assets = self.client.query_public("AssetPairs")

        for item in assets["result"]:
            index = item.find("XBT")
            print(item)
            if index != -1:
                if item[:index] != "":
                    available_markets.append(item[:index])
        return available_markets

    def get_coin_price(self, name, pair="BTC"):
        print("ERROR: " + self.name + "  Not implemented")
        return -1

    def get_coins_prices(self):
        print("ERROR: " + self.name + "  Not implemented")
        return -1

    def get_order_book(self, market, side):
        print("ERROR: " + self.name + "  Not implemented")
        return -1

    ###########################################################
    # Actions
    def withdraw_asset(self, asset, target_addr, amount):
        print("ERROR: " + self.name + "  Not implemented")
        return -1

    def create_order(self, market, side, price, amount):
        print("ERROR: " + self.name + "  Not implemented")
        return -1
