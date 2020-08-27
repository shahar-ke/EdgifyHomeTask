import json
from typing import Dict

from models.order_status import OrderStatus


class Order:
    ORDER_ATTR = 'order'
    PRICE_ATTR = 'price'
    STATUS_ATTR = 'status'

    def __init__(self, price, order):
        self.price: float = price
        self.order: str = order
        self.status: OrderStatus = OrderStatus.UNPROCESSED

    def __str__(self):
        return f'{self.order=}, {self.price=}, {self.status=}'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_json(cls, json_data: json):
        if json_data is None:
            return None
        if cls.ORDER_ATTR not in json_data or cls.PRICE_ATTR not in json_data:
            return None
        return cls(price=json_data[cls.PRICE_ATTR], order=json_data[cls.ORDER_ATTR])

    def to_json(self) -> Dict[str, any]:
        return {self.ORDER_ATTR: self.order,
                self.PRICE_ATTR: self.price,
                self.STATUS_ATTR: self.status}
