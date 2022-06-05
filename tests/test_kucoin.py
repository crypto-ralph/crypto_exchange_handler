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
    def send_priv_request_mock(self):
        return kucoin_markets_ok_resp

    monkeypatch.setattr(kucoin_client, "send_priv_request", send_priv_request_mock)

    expected_result = ("REQ-ETH", "REQ-BTC", "NULS-ETH")

    assert kucoin_client.get_available_markets() == expected_result


def test_get_available_markets_nok(kucoin_client, kucoin_markets_nok_resp, monkeypatch):
    """Tests if None is returned in case of error in response"""
    def send_priv_request_mock(self):
        return kucoin_markets_nok_resp

    monkeypatch.setattr(kucoin_client, "send_priv_request", send_priv_request_mock)

    assert kucoin_client.get_available_markets() is None


def test_get_coin_price(kucoin_client):
    """Tests if coin price has been gathered correctly"""
    assert kucoin_client.get_coin_price("ETH", "BTC") is None
