from exchangeAPI import templateApi

import ssl
import hashlib
import time
import hmac
import urllib.request
import urllib.parse
from urllib.error import HTTPError
import json
import sys


class Graviex(templateApi.ExchangeAPI):
    def __init__(self, designation, name, access_key: str, secret_key: str):
        super().__init__(name, access_key, secret_key, designation)
        self.name = "graviex"
        self.designation = designation
        """
        asks: sell
        bids: buy
        """
        self.api_addr = "https://graviex.net/api/v3/"
        self.ssl_ctxt = self.make_ssl_ctxt()
        self.epoch_time = "0"
        self.calc_epoch_time()
        self.request = ""

    ###########################################################
    # Ptivate Functions
    ###########################################################
    def calc_epoch_time(self):
        self.epoch_time = str(int(time.time())) + "000"

    def gen_priv_request(self, **kwargs):
        self.calc_epoch_time()
        self.request = "access_key=" + self.access_key
        for arg in kwargs:
            self.request += "&" + arg + "=" + kwargs[arg]
        self.request += "&tonce=" + self.epoch_time

    def gen_pub_request(self, **kwargs):
        self.request = ""
        for arg in kwargs:
            self.request += arg + "=" + kwargs[arg]

    def gen_hash(self, secret, msg):
        try:
            signature = hmac.new(secret, msg, hashlib.sha256).hexdigest()
            return signature
        except:
            print("ERROR:", sys.exc_info()[1])
            return -1

    def make_ssl_ctxt(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def get_request(self, addr):
        query = self.api_addr + addr + "?" + self.request

        if self.request.find("access_key") != -1:
            message = "GET|/api/v3/" + addr + "|" + self.request
            signature = self.gen_hash(
                bytes(self.secret_key, "utf-8"), bytes(message, "utf-8")
            )
            query += "&signature=" + signature
        try:
            content = urllib.request.urlopen(query, context=self.ssl_ctxt).read()
            time.sleep(1)
            return self.response_parse(content)
        except HTTPError as err:
            print(
                f"ERROR: HTTP Exception\nCode:  {str(err.code)}\nReason: {str(err.reason)}\n"
                f"Msg: {str(err.msg)}\nURL: {str(err.url)}"
            )
            time.sleep(1)
            return -1

    def post_request(self, addr):
        query = self.api_addr + addr + "?" + self.request
        message = "POST|/api/v3/" + addr + "|" + self.request
        signature = self.gen_hash(
            bytes(self.secret_key, "utf-8"), bytes(message, "utf-8")
        )
        req = urllib.request.Request(
            query, bytes(urllib.parse.urlencode({"signature": signature}), "utf-8")
        )

        try:
            content = urllib.request.urlopen(req, context=self.ssl_ctxt).read()
            return content
        except HTTPError as err:
            print(
                f"ERROR: HTTP Exception\nCode:  {str(err.code)}\nReason: {str(err.reason)}\n"
                f"Msg: {str(err.msg)}\nURL: {str(err.url)}"
            )
            time.sleep(1)
            return -1

    def response_parse(self, response):
        json_decode = json.JSONDecoder()
        response_string = response.decode("utf-8")
        parsed_response = json_decode.decode(response_string)
        return parsed_response

    ###########################################################
    # API Functions
    # Getters
    ###########################################################
    def get_all_balances(self):
        result = {}
        self.gen_priv_request()
        response = self.get_request("members/me")
        if response != -1:
            for account in response["accounts_filtered"]:
                if account["balance"] != "0.0":
                    result[account["currency"]] = account["balance"]
            return result
        else:
            return -1

    def get_balance(self, coin):
        response = self.get_all_balances()
        if response != -1:
            for account in response:
                if account == coin.lower():
                    return response[account]
        else:
            return -1

    def get_available_markets(self):
        available_markets = []
        ticker = self.get_request("markets")
        if ticker != -1:
            for item in ticker:
                index = item["id"].upper().find("BTC")
                if index != -1:
                    if item["id"][:index] != "":
                        available_markets.append(item["id"][:index].upper())
            return available_markets
        else:
            return -1

    def get_coin_price(self, name, pair="BTC"):
        if self.designation == "source":
            book = self.get_order_book(name.lower() + pair.lower(), "asks")
            if book != -1:
                return book[0][0]
            else:
                print("Wrong response")
                return -1
        elif self.designation == "target":
            book = self.get_order_book(name.lower() + pair.lower(), "bids")
            if book != -1:
                return book[0][0]
            else:
                print("Wrong response")
                return -1

    def get_coins_prices(self):
        ticker = -1
        for i in range(4):
            ticker = self.get_request("tickers")
            if ticker != -1:
                break
            else:
                time.sleep(1)
                print("Try again: " + str(i) + "/4")

        if ticker == -1:
            return -1

        coins = {}
        if ticker != -1:
            for item in ticker:
                if ticker[item]["quote_unit"] == "btc":
                    if self.designation == "source":
                        coins[ticker[item]["base_unit"].upper()] = ticker[item]["sell"]
                    elif self.designation == "target":
                        coins[ticker[item]["base_unit"].upper()] = ticker[item]["buy"]
            return coins
        else:
            print("ERROR: Could not get ticker")
            return -1

    def get_order_book(self, market, side):
        self.gen_priv_request(market=market)
        order_book = self.get_request("order_book")
        if order_book != -1:
            book = []
            try:
                for order in order_book[side]:
                    book.append([order["price"], order["remaining_volume"]])
                return book
            except KeyError as e:
                print("Error: Wrong key - " + str(e))
                return -1
        else:
            print("Wrong API response")
            return -1

    ###########################################################
    # Actions
    def withdraw_asset(self, asset, target_addr, amount):
        self.gen_priv_request(
            currency=asset.lower(), fund_uid=target_addr, sum=str(amount)
        )
        result = self.post_request("create_withdraw")
        return result

    def create_order(self, market, side, price, amount):
        self.gen_priv_request(market=market, side=side, price=price, volume=amount)
        result = self.post_request("orders")
        return result
