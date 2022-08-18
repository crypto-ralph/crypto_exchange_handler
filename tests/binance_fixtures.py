import pytest


@pytest.fixture
def binance_markets_ok_resp():
    """
    Mock ok response with a binance-like format.
    :return: response list
    """
    return [
        {"symbol": "REQETH", "price": "0.07990400"},
        {"symbol": "REQBTC", "price": "0.00260900"},
        {"symbol": "NULSETH", "price": "0.01302100"},
    ]


@pytest.fixture
def binance_klines_resp():
    """
    Resposnse whit klines from market/candles endpoint.
    :return: response list
    """
    return [
        [
            1655415000000,
            "20843.90000000",
            "20920.80000000",
            "20626.00000000",
            "20673.80000000",
            "9928.37788000",
            1659041999999,
            "238297508.30548260",
            223164,
            "5053.28525000",
            "121321348.55092420",
            "0",
        ],
        [
            1655413200000,
            "20711.70000000",
            "20935.60000000",
            "20676.80000000",
            "20843.90000000",
            "4215.44152000",
            1659043799999,
            "101368085.47540840",
            107653,
            "2161.38546000",
            "51980514.36553620",
            "0",
        ],
        [
            1655411400000,
            "20966.00000000",
            "20969.90000000",
            "20510.00000000",
            "20711.70000000",
            "2267.81878000",
            1659045599999,
            "54227886.51585630",
            73967,
            "1091.69289000",
            "26107254.33713290",
            "0",
        ],
        [
            1655409600000,
            "20871.90000000",
            "21096.00000000",
            "20856.50000000",
            "20966.00000000",
            "3551.20149000",
            1659047399999,
            "84883974.97390910",
            102841,
            "1761.37823000",
            "42104064.60080590",
            "0",
        ],
        [
            1655407800000,
            "21071.30000000",
            "21096.90000000",
            "20850.00000000",
            "20872.70000000",
            "2716.13934000",
            1659049199999,
            "65014289.42109820",
            78897,
            "1345.43812000",
            "32206975.25982810",
            "0",
        ],
    ]
