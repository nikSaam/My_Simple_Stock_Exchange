from exchange import Exchange
from models import ActionType, OrderType


# Создание ордера
def test_place_order():
    ex_test = Exchange()

    order_test = ex_test.place_order(
        name="AAPL",
        action_type=ActionType.BUY,
        order_type=OrderType.LMT,
        price=100,
        quantity=10,
    )

    assert order_test.name == "AAPL"
    assert order_test.price == 100
    assert order_test.quantity == 10
    assert order_test.filled == 0


# матчинг
def test_match():
    ex_test = Exchange()

    buy = ex_test.place_order("AAPL", ActionType.BUY, OrderType.LMT, 100, 10)
    sell = ex_test.place_order("AAPL", ActionType.SELL, OrderType.LMT, 90, 10)

    assert buy.filled == 10
    assert sell.filled == 10
    assert buy.status == "FILLED"
    assert sell.status == "FILLED"


# Нет сделки
def test_no_order():
    ex_test = Exchange()

    buy = ex_test.place_order("SNAP", ActionType.BUY, OrderType.LMT, 70, 10)
    sell = ex_test.place_order("SNAP", ActionType.SELL, OrderType.LMT, 100, 10)

    assert buy.filled == 0
    assert sell.filled == 0


# MKT
def test_mkt_order():
    ex_test = Exchange()

    buy = ex_test.place_order("AAPL", ActionType.BUY, OrderType.MKT, None, 5)
    sell = ex_test.place_order("AAPL", ActionType.SELL, OrderType.LMT, 100, 10)

    assert buy.filled == 5
    assert sell.filled == 5
