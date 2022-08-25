""" Unit tests for kucoin.py """
from crypto_exchange_handler.exchange_template import MarketSide # pylint: disable=import-error


def test_kucoin_object_created(kucoin_client):
    """Tests if instance has been created correctly"""
    assert kucoin_client.access_key == "access"
    assert kucoin_client.secret_key == "secret"
    assert kucoin_client.api_passphrase == "passphrase"


def test_get_balance(kucoin_client):
    """Tests if balance has been retrieved correctly"""
    assert kucoin_client.get_balance("BTC") is None


def test_get_available_markets_nok(kucoin_client, kucoin_nok_resp, monkeypatch):
    """Tests if None is returned in case of error in response"""

    def send_priv_request_mock(self):  # pylint: disable=unused-argument
        return kucoin_nok_resp

    monkeypatch.setattr(kucoin_client, "send_priv_request", send_priv_request_mock)

    assert kucoin_client.get_available_markets() is None


def test_get_coin_price(kucoin_client, kucoin_ticker_ok_resp, monkeypatch):
    """Tests if coin price for given coin has been gathered correctly"""

    def send_priv_request_mock(self, data):  # pylint: disable=unused-argument
        return kucoin_ticker_ok_resp

    monkeypatch.setattr(kucoin_client, "send_priv_request", send_priv_request_mock)

    ask_price = kucoin_client.get_coin_price("COIN", "PAIR", MarketSide.ASK)
    bid_price = kucoin_client.get_coin_price("COIN", "PAIR", MarketSide.BID)
    latest_price = kucoin_client.get_coin_price("COIN", "PAIR", MarketSide.LATEST)

    assert ask_price == kucoin_ticker_ok_resp["data"]["bestAsk"]
    assert bid_price == kucoin_ticker_ok_resp["data"]["bestBid"]
    assert latest_price == kucoin_ticker_ok_resp["data"]["price"]


def test_get_coins_prices(kucoin_client, kucoin_ticker_all_ok_resp, monkeypatch):
    """Tests if coins prices for given tuple has been gathered correctly"""

    def send_priv_request_mock(self):  # pylint: disable=unused-argument
        return kucoin_ticker_all_ok_resp

    monkeypatch.setattr(kucoin_client, "send_priv_request", send_priv_request_mock)

    ask_prices = kucoin_client.get_coins_prices(("ADA", "XRP"), "BTC", MarketSide.ASK)
    bid_prices = kucoin_client.get_coins_prices(("ADA", "XRP"), price_type=MarketSide.BID)
    latest_prices = kucoin_client.get_coins_prices(("ADA",), "BTC", MarketSide.LATEST)

    assert ask_prices == {"ADA-BTC": "0.00002375", "XRP-BTC": "0.00001616"}
    assert bid_prices == {"ADA-BTC": "0.00002373", "XRP-BTC": "0.00001614"}
    assert latest_prices == {"ADA-BTC": "0.00002375"}


# def test_get_order_book(kucoin_client, kucoin_klines_resp, monkeypatch):
#     """Tests if proper candles tuple is returned"""
#
#     def send_priv_request_mock(self, data):  # pylint: disable=unused-argument
#         return kucoin_klines_resp
#
#     monkeypatch.setattr(kucoin_client, "send_priv_request", send_priv_request_mock)
#
#     klines = kucoin_client.get_candles("BTC-USDT", "30min", "2022-06-15", "2022-06-17")
#
#     expected_result = (
#         {"ts": 1655415000, "open": 20843.9, "close": 20673.8, "high": 20920.8, "low": 20626.0},
#         {"ts": 1655413200, "open": 20711.7, "close": 20843.9, "high": 20935.6, "low": 20676.8},
#         {"ts": 1655411400, "open": 20966.0, "close": 20711.7, "high": 20969.9, "low": 20510.0},
#         {"ts": 1655409600, "open": 20871.9, "close": 20966.0, "high": 21096.0, "low": 20856.5},
#         {"ts": 1655407800, "open": 21071.3, "close": 20872.7, "high": 21096.9, "low": 20850.0},
#     )
#
#     assert klines == expected_result
