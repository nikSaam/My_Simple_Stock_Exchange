class Order:
    def __init__(self, id, symbol, order_type, price, side, quantity):
        self.id = id  # Уникальный идентификатор(для отслеживания заявок)
        self.symbol = (
            symbol  # Что торгуем(SNAP, FB,AAPL) чтобы не смешивать разные акции
        )
        self.order_type = order_type  # Тип завяки (LMT-есть лимитнаяцена, MKT- рыночная заявка(берет лучшую цену))
        self.side = side  # Направление (BUY/SELL)
        self.price = price  # Цена(для MKT - None)
        self.quantity = quantity  # Кол-во
        self.filled = 0

    def remaining(self):
        return self.quantity - self.filled  # Сколько осталось исполнить

    @property
    def status(self):
        if self.filled == 0:
            return "PENDING"
        elif self.filled < self.quantity:
            return "PARTIAL"
        else:
            return "FILLED"

    def __str__(
        self,
    ):  # ОПределяется в сущности, __стр__ описывает сам объект, а не способо его использования,тк объект должен знать как себя показать(Order знает -> свои поля и как себя показать)
        price = f"${self.price:.2f}" if self.price else "MKT"
        return f"{self.symbol} {self.order_type} {self.side} {price} {self.filled}/{self.quantity} {self.status}"
