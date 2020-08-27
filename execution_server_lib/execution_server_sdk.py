import random
from typing import List

from models.order import Order
from models.order_status import OrderStatus


class ExecutionServerSDK:

    @staticmethod
    def execute_orders(orders: List[Order]):
        for order in orders:
            if random.randrange(100) < 50:
                order_status = OrderStatus.APPROVED
            else:
                order_status = OrderStatus.REJECTED
            order.status = order_status
        return orders
