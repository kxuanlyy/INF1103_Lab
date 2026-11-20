from __future__ import annotations
from order_line import OrderLine
from product import Product
from discount_strategy import DiscountStrategy, NoDiscount


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy = None) -> None:
        self.order_id: str = order_id
        self.__order_lines: list[OrderLine] = []   # composition — Order creates and owns these
        self.__discount: DiscountStrategy = discount or NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)   # Order creates the OrderLine
        self.__order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)   # delegate to strategy — no if/elif here

    def display_order(self) -> None:
        print(f"\nOrder ID: {self.order_id}")
        print("-" * 40)
        for line in self.__order_lines:
            line.display_line()
        print(f"  Total: ${self.calculate_total():.2f}")
        print("-" * 40)
