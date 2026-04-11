class OrderBook:
    def __init__(self):
        self.buys = []
        self.sells = []

    def add(self, order):
        if order.action_type.value == "BUY":
            self.buys.append(order)
        else:
            self.sells.append(order)

    def sort(self):
        # BUY — по убыванию цены (None в конец)
        self.buys.sort(key=lambda o: (o.price is None, -(o.price or 0)))

        # SELL — по возрастанию цены (None в конец)
        self.sells.sort(key=lambda o: (o.price is None, o.price or 0))