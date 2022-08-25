""" Pytest fixtures for all unit tests. """
import pytest
from crypto_exchange_handler.kucoin import Kucoin
from crypto_exchange_handler.binance import Binance


pytest_plugins = ["kucoin_fixtures", "binance_fixtures"]


@pytest.fixture
def kucoin_client():
    """
    Fixture representing kucoin class instance.
    :return: kucoin class instance
    """
    return Kucoin("access", "secret", "passphrase")


@pytest.fixture
def binance_client():
    """
    Fixture representing binance class instance.
    :return: binance class instance
    """
    return Binance("access", "secret")


@pytest.fixture
def binance_balances_resp():
    """
    Mock account balances response from binance
    """
    return {
        "makerCommission": 10,
        "takerCommission": 10,
        "buyerCommission": 0,
        "sellerCommission": 0,
        "canTrade": True,
        "canWithdraw": True,
        "canDeposit": True,
        "updateTime": 1656196276658,
        "accountType": "SPOT",
        "balances": [
            {"asset": "BTC", "free": "0.05090135", "locked": "0.00000000"},
            {"asset": "LTC", "free": "0.00031844", "locked": "0.00000000"},
            {"asset": "NEO", "free": "0.00000000", "locked": "0.00000000"},
            {"asset": "EOS", "free": "0.00000000", "locked": "0.00000000"},
            {"asset": "SNT", "free": "0.00000000", "locked": "0.00000000"},
            {"asset": "USDT", "free": "0.10495989", "locked": "0.00000000"},
            {"asset": "HSR", "free": "0.00000000", "locked": "0.00000000"},
            {"asset": "OAX", "free": "0.00000000", "locked": "0.00000000"},
        ],
        "permissions": ["SPOT", "LEVERAGED"],
    }
