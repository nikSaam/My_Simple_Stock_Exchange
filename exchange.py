from models import Order
from order_book import OrderBook


class Exchange:
    def __init__(self):
        self.book = OrderBook()
        self.orders = []
        self.last_price = None
        self.counter = 1

    def place_order(self, symbol, side, order_type, price, quantity):
        # создаём заявку
        order = Order(self.counter, symbol, order_type, price, side, quantity)
        self.counter += 1

        # сохраняем
        self.orders.append(order)
        self.book.add(order)
        self.book.sort()

        # пытаемся исполнить
        self.match()

        return order

    def match(self):
        # основной matching engine
        for buy in self.book.buys:
            if buy.remaining() == 0:
                continue

            for sell in self.book.sells:
                if sell.remaining() == 0:
                    continue

                # проверяем, что это одна акция
                if buy.symbol != sell.symbol:
                    continue

                # условие сделки
                if (
                    buy.order_type == "MKT"
                    or sell.order_type == "MKT"
                    or buy.price >= sell.price
                ):
                    trade_qty = min(buy.remaining(), sell.remaining())

                    # определяем цену сделки
                    trade_price = sell.price if sell.price else buy.price

                    # обновляем
                    buy.filled += trade_qty
                    sell.filled += trade_qty

                    self.last_price = trade_price

                    # если BUY полностью исполнен — дальше не идём
                    if buy.remaining() == 0:
                        break

    def view_orders(self):
        for i, o in enumerate(self.orders, 1):
            print(f"{i}. {o}")

    def quote(self, symbol):
        # лучшие цены
        bids = [
            o.price for o in self.book.buys if o.symbol == symbol and o.remaining() > 0
        ]
        asks = [
            o.price for o in self.book.sells if o.symbol == symbol and o.remaining() > 0
        ]

        bid = max(bids) if bids else None
        ask = min(asks) if asks else None

        print(f"{symbol} BID: {bid} ASK: {ask} LAST: {self.last_price}")
