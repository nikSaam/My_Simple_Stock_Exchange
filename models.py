from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    LMT = "LMT"
    MKT = "MKT"


@dataclass
class Order:
    id: int
    action_type: ActionType
    name: str
    order_type: OrderType
    price: float | None
    quantity: int
    filled: int = 0

    @property
    def remaining(self):
        return self.quantity - self.filled

    @property
    def status(self):
        if self.filled == 0:
            return "PENDING"
        elif self.filled < self.quantity:
            return "PARTIAL"
        else:
            return "FILLED"

    def __str__(self):
        price = f"${self.price:.2f}" if self.price is not None else "MKT"
        return f"{self.name} {self.order_type.value} {self.action_type.value} {price} {self.filled}/{self.quantity} {self.status}"