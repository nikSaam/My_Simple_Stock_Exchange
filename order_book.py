from collections import defaultdict
from models import OrderType


class OrderBook:
    def __init__(self):
        self.buys = defaultdict(list)
        self.sells = defaultdict(list)

    def add(self, order):
        if order.action_type.value == "BUY":
            self.buys[order.name].append(order)
        else:
            self.sells[order.name].append(order)

    def sort(self, name):
        # BUY: MKT вперед, далее по большей цене
        self.buys[name].sort(
            key=lambda o: (
                o.order_type != OrderType.MKT,
                -(o.price or 0)
            )
        )

        # SELL: MKT первым, далее по меньшей цене
        self.sells[name].sort(
            key=lambda o: (
                o.order_type != OrderType.MKT,
                (o.price or float("inf"))
            )
        )