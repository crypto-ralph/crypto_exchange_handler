""" Unit tests for kucoin.py """


def test_kucoin_object_created(kucoin_client):
    """Tests if instance has been created correctly"""
    assert kucoin_client.access_key == "access"
    assert kucoin_client.secret_key == "secret"
    assert kucoin_client.api_passphrase == "passphrase"


def test_get_balance(kucoin_client):
    """Tests if balance has been retrieved correctly"""
    assert kucoin_client.get_balance("BTC") is None


def test_get_available_markets_ok(kucoin_client, kucoin_markets_ok_resp, monkeypatch):
    """Tests if available markets is extracted in desired format"""

    def send_priv_request_mock(self):  # pylint: disable=unused-argument
        return kucoin_markets_ok_resp

    monkeypatch.setattr(kucoin_client, "send_priv_request", send_priv_request_mock)

    expected_result = ("REQ-ETH", "REQ-BTC", "NULS-ETH")

    assert kucoin_client.get_available_markets() == expected_result


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

    ask_price = kucoin_client.get_coin_price("COIN", "PAIR", "ask")
    bid_price = kucoin_client.get_coin_price("COIN", "PAIR", "bid")
    latest_price = kucoin_client.get_coin_price("COIN", "PAIR", "latest")

    assert ask_price == kucoin_ticker_ok_resp["data"]["bestAsk"]
    assert bid_price == kucoin_ticker_ok_resp["data"]["bestBid"]
    assert latest_price == kucoin_ticker_ok_resp["data"]["price"]


def test_get_coins_prices(kucoin_client, kucoin_ticker_all_ok_resp, monkeypatch):
    """Tests if coins prices for given tuple has been gathered correctly"""

    def send_priv_request_mock(self):  # pylint: disable=unused-argument
        return kucoin_ticker_all_ok_resp

    monkeypatch.setattr(kucoin_client, "send_priv_request", send_priv_request_mock)

    ask_prices = kucoin_client.get_coins_prices(("ADA", "XRP"), "BTC", "ask")
    bid_prices = kucoin_client.get_coins_prices(("ADA", "XRP"), price_type="bid")
    latest_prices = kucoin_client.get_coins_prices(("ADA",), "BTC", "latest")

    assert ask_prices == {"ADA-BTC": "0.00002375", "XRP-BTC": "0.00001616"}
    assert bid_prices == {"ADA-BTC": "0.00002373", "XRP-BTC": "0.00001614"}
    assert latest_prices == {"ADA-BTC": "0.00002375"}
