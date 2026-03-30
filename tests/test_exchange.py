from exchange import Exchange


def test_simple_match():
    exchange = Exchange()

    # создаём BUY
    buy = exchange.place_order("AAPL", "BUY", "LMT", 30, 100)

    # создаём SELL (дешевле → должен сматчиться)
    sell = exchange.place_order("AAPL", "SELL", "LMT", 29, 100)

    # проверяем
    assert buy.filled == 100
    assert sell.filled == 100

    assert buy.status == "FILLED"
    assert sell.status == "FILLED"
