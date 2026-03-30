class OrderBook:
    def __init__(self):
        self.buys = []
        self.sells = []

    def add(self, order):
        # кладём заявку в нужный список
        if order.side == "BUY":  # Утиная типизация
            self.buys.append(order)
        else:
            self.sells.append(order)

    def sort(self):
        # BUY: чем выше цена — тем раньше
        self.buys.sort(key=lambda o: o.price if o.price else float("inf"), reverse=True)

        # SELL: чем ниже цена — тем раньше
        self.sells.sort(key=lambda o: o.price if o.price else 0)
