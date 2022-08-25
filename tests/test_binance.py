""" Unit tests for binance.py """


def test_binance_object_created(binance_client):
    """Tests if instance has been created correctly"""
    assert binance_client.access_key == "access"
    assert binance_client.secret_key == "secret"


def test_get_balance(binance_client, binance_balances_resp, monkeypatch):
    """Tests if balance has been retrieved correctly"""

    def get_account_mock():  # pylint: disable=unused-argument
        return binance_balances_resp

    monkeypatch.setattr(binance_client.client, "get_account", get_account_mock)

    assert binance_client.get_balance("BTC") == "0.0509013500"
    assert binance_client.get_balance("EOS") == "0.0000000000"
    assert binance_client.get_balance("QAB") is None
