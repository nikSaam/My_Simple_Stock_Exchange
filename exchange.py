from models import Order, ActionType, OrderType
from order_book import OrderBook


class Exchange:
    def __init__(self):
        self.book = OrderBook()
        self.orders = []
        self.counter = 1
        self.last_price = None

    def place_order(self, name, action_type, order_type, price, quantity):
        if order_type == OrderType.MKT:
            price = None

        order = Order(
            id=self.counter,
            action_type=action_type,
            name=name,
            order_type=order_type,
            price=price,
            quantity=quantity,
        )

        self.counter += 1

        self.orders.append(order)
        self.book.add(order)
        self.book.sort()

        self.match()

        return order

    def match(self):
        while self.book.buys and self.book.sells:

            buy = self.book.buys[0]
            sell = self.book.sells[0]

            if buy.remaining == 0:
                self.book.buys.pop(0)
                continue

            if sell.remaining == 0:
                self.book.sells.pop(0)
                continue

            if buy.name != sell.name:
                break

            if buy.order_type == OrderType.MKT and sell.order_type == OrderType.MKT:
                break

            if (
                buy.price is not None and
                sell.price is not None and
                buy.price < sell.price
            ):
                break

            trade_qty = min(buy.remaining, sell.remaining)

            if sell.price is not None:
                trade_price = sell.price
            else:
                trade_price = buy.price

            if trade_price is None:
                break

            buy.filled += trade_qty
            sell.filled += trade_qty

            self.last_price = trade_price

            if buy.remaining == 0:
                self.book.buys.pop(0)

            if sell.remaining == 0:
                self.book.sells.pop(0)

    def view_orders(self):
        for o in self.orders:
            print(o)

    def quote(self, symbol):
        bids = [
            o.price for o in self.book.buys
            if o.name == symbol and o.remaining > 0 and o.price is not None
        ]

        asks = [
            o.price for o in self.book.sells
            if o.name == symbol and o.remaining > 0 and o.price is not None
        ]

        bid = max(bids) if bids else None
        ask = min(asks) if asks else None

        print(f"{symbol} BID: {bid} ASK: {ask} LAST: {self.last_price}")