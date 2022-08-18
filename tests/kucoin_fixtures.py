import pytest


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
def kucoin_klines_resp():
    """
    Resposnse whit klines from market/candles endpoint.
    :return: response dictionary
    """
    return {
        "code": "200000",
        "data": [
            [
                "1655415000",
                "20843.9",
                "20673.8",
                "20920.8",
                "20626",
                "123.98034374",
                "2576013.394928467",
            ],
            [
                "1655413200",
                "20711.7",
                "20843.9",
                "20935.6",
                "20676.8",
                "281.93338746",
                "5865493.858205836",
            ],
            [
                "1655411400",
                "20966",
                "20711.7",
                "20969.9",
                "20510",
                "760.96912518",
                "15713004.882986378",
            ],
            [
                "1655409600",
                "20871.9",
                "20966",
                "21096",
                "20856.5",
                "498.41595179",
                "10464215.073549074",
            ],
            [
                "1655407800",
                "21071.3",
                "20872.7",
                "21096.9",
                "20850",
                "774.62700373",
                "16196368.501153962",
            ],
        ],
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
