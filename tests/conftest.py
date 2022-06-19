""" Pytest fixtures for all unit tests. """
import pytest

from crypto_exchange_handler.kucoin import Kucoin  # pylint: disable=E0611, E0401


@pytest.fixture
def kucoin_client():
    """
    Fixture representing kucoin class instance.
    :return: kucoin class instance
    """
    return Kucoin("access", "secret", "passphrase")


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
def kucoin_ticker_all_ok_resp():
    """
    Mock ticker ok response with a kucoin-like format.
    :return: response dictionary
    """
    return {
        "code": "200000",
        "data": {
            "time": 1655652664013,
            "ticker": [
                {
                    "symbol": "ADA-BTC",
                    "symbolName": "ADA-BTC",
                    "buy": "0.00002373",
                    "sell": "0.00002375",
                    "changeRate": "-0.0137",
                    "changePrice": "-0.00000033",
                    "high": "0.00002455",
                    "low": "0.00002361",
                    "vol": "4758214.26213239",
                    "volValue": "114.1738370725038569",
                    "last": "0.00002375",
                    "averagePrice": "0.00002093",
                    "takerFeeRate": "0.001",
                    "makerFeeRate": "0.001",
                    "takerCoefficient": "1",
                    "makerCoefficient": "1",
                },
                {
                    "symbol": "XRP-BTC",
                    "symbolName": "XRP-BTC",
                    "buy": "0.00001614",
                    "sell": "0.00001616",
                    "changeRate": "0.0087",
                    "changePrice": "0.00000014",
                    "high": "0.00001664",
                    "low": "0.00001581",
                    "vol": "1798977.80646462",
                    "volValue": "29.3331702506852608",
                    "last": "0.00001615",
                    "averagePrice": "0.00001366",
                    "takerFeeRate": "0.001",
                    "makerFeeRate": "0.001",
                    "takerCoefficient": "1",
                    "makerCoefficient": "1",
                },
            ],
        },
    }


@pytest.fixture
def kucoin_ticker_ok_resp():
    """
    Mock ticker ok response with a kucoin-like format.
    :return: response dictionary
    """
    return {
        "code": "200000",
        "data": {
            "time": 1655648614970,
            "sequence": "1631684567416",
            "price": "19284.4",
            "size": "0.00012447",
            "bestBid": "19284.3",
            "bestBidSize": "0.79593141",
            "bestAsk": "19284.4",
            "bestAskSize": "0.00417572",
        },
    }


@pytest.fixture
def kucoin_nok_resp():
    """
    Mock nok response with a kucoin-like format.
    :return: response dictionary
    """
    return {
        "code": "404",
    }
