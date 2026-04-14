from models import Order, OrderType, Trade
from order_book import OrderBook


class Exchange:
    def __init__(self):
        self.book = OrderBook()
        self.orders = []
        self.trades = []
        self.counter = 1
        self.last_price = {}

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
        self.book.sort(name)

        self.match(name)

        return order

    def match(self, name):
        buys = self.book.buys[name]
        sells = self.book.sells[name]

        while buys and sells:

            buy = buys[0]
            sell = sells[0]

            if buy.remaining == 0:
                buys.pop(0)
                continue

            if sell.remaining == 0:
                sells.pop(0)
                continue

            # Нельзя MKT vs MKT
            if buy.order_type == OrderType.MKT and sell.order_type == OrderType.MKT:
                break

            # Проверка цены
            if (
                buy.price is not None and
                sell.price is not None and
                buy.price < sell.price
            ):
                break

            trade_qty = min(buy.remaining, sell.remaining)

            trade_price = sell.price if sell.price is not None else buy.price

            if trade_price is None:
                break

            # Обновляем ордера
            buy.filled += trade_qty
            sell.filled += trade_qty

            # Сохраняем сделку
            trade = Trade(name=name, price=trade_price, quantity=trade_qty)
            self.trades.append(trade)

            # Последняя цена по тикеру
            self.last_price[name] = trade_price

            if buy.remaining == 0:
                buys.pop(0)

            if sell.remaining == 0:
                sells.pop(0)

    def view_orders(self):
        for o in self.orders:
            print(o)

    def view_trades(self):
        for t in self.trades:
            print(t)

    def quote(self, name):
        buys = self.book.buys[name]
        sells = self.book.sells[name]

        bids = [
            o.price for o in buys
            if o.remaining > 0 and o.price is not None
        ]

        asks = [
            o.price for o in sells
            if o.remaining > 0 and o.price is not None
        ]

        bid = max(bids) if bids else None
        ask = min(asks) if asks else None
        last = self.last_price.get(name)

        print(f"{name} BID: {bid} ASK: {ask} LAST: {last}")