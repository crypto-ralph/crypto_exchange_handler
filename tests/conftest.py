""" Pytest fixtures for all unit tests. """
import pytest

from crypto_exchange_handler import kucoin # pylint: disable=E0611


@pytest.fixture
def kucoin_client():
    """
    Fixture representing kucoin class instance.
    :return: kucoin class instance
    """
    return kucoin.Kucoin("access", "secret", "passphrase")


@pytest.fixture
def kucoin_markets_ok_resp():
    """
    Mock ok response with a kucoin-like format.
    :return: response dictionary
    """
    return {
        "code": "200000",
        "data": [
            {
                "symbol": "REQ-ETH",
                "name": "REQ-ETH",
                "baseCurrency": "REQ",
                "quoteCurrency": "ETH",
                "feeCurrency": "ETH",
                "isMarginEnabled": False,
                "enableTrading": True,
            },
            {
                "symbol": "REQ-BTC",
                "name": "REQ-BTC",
                "baseCurrency": "REQ",
                "quoteCurrency": "BTC",
                "feeCurrency": "BTC",
                "isMarginEnabled": False,
                "enableTrading": True,
            },
            {
                "symbol": "NULS-ETH",
                "name": "NULS-ETH",
                "baseCurrency": "NULS",
                "quoteCurrency": "ETH",
                "feeCurrency": "ETH",
                "isMarginEnabled": False,
                "enableTrading": True,
            },
        ],
    }


@pytest.fixture
def kucoin_markets_nok_resp():
    """
    Mock nok response with a kucoin-like format.
    :return: response dictionary
    """
    return {
        "code": "404",
    }
