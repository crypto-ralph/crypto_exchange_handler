# def test_get_balance(kucoin_client, binance_client):
#     """Tests if balance has been retrieved correctly"""
#     assert binance_client.get_balance("BTC") is None
#     assert kucoin_client.get_balance("BTC") is None


def test_get_available_markets_ok(
    kucoin_client, binance_client, kucoin_markets_ok_resp, binance_markets_ok_resp, monkeypatch
):
    """Tests if available markets is extracted in desired format"""

    def send_priv_request_mock(self):  # pylint: disable=unused-argument
        return kucoin_markets_ok_resp

    def get_symbol_ticker_mock():
        return binance_markets_ok_resp

    monkeypatch.setattr(binance_client.client, "get_symbol_ticker", get_symbol_ticker_mock)
    monkeypatch.setattr(kucoin_client, "send_priv_request", send_priv_request_mock)

    expected_result = ("REQETH", "REQBTC", "NULSETH")

    assert kucoin_client.get_available_markets() == expected_result
    assert binance_client.get_available_markets() == expected_result


def test_get_candles(
    kucoin_client, binance_client, kucoin_klines_resp, binance_klines_resp, monkeypatch
):
    """Tests if proper candles tuple is returned"""

    def send_priv_request_mock(self, data):  # pylint: disable=unused-argument
        return kucoin_klines_resp

    def get_historical_klines_mock(**kwargs):  # pylint: disable=unused-argument
        return binance_klines_resp

    monkeypatch.setattr(kucoin_client, "send_priv_request", send_priv_request_mock)
    monkeypatch.setattr(binance_client.client, "get_historical_klines", get_historical_klines_mock)

    klines_kucoin = kucoin_client.get_candles("BTC", "USDT", "30min", "2022-06-15", "2022-06-17")
    klines_binance = binance_client.get_candles("BTC", "USDT", "30m", "2022-06-15", "2022-06-17")

    expected_result = (
        {"ts": 1655415000, "open": 20843.9, "close": 20673.8, "high": 20920.8, "low": 20626.0},
        {"ts": 1655413200, "open": 20711.7, "close": 20843.9, "high": 20935.6, "low": 20676.8},
        {"ts": 1655411400, "open": 20966.0, "close": 20711.7, "high": 20969.9, "low": 20510.0},
        {"ts": 1655409600, "open": 20871.9, "close": 20966.0, "high": 21096.0, "low": 20856.5},
        {"ts": 1655407800, "open": 21071.3, "close": 20872.7, "high": 21096.9, "low": 20850.0},
    )

    assert klines_kucoin == expected_result
    assert klines_binance == expected_result
