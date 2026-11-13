from __future__ import annotations
from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.__order_lines: list[OrderLine] = []   # composition — Order creates and owns these

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)   # Order creates the OrderLine
        self.__order_lines.append(order_line)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_order(self) -> None:
        print(f"\nOrder ID: {self.order_id}")
        print("-" * 40)
        for line in self.__order_lines:
            line.display_line()
        print(f"  Total: ${self.calculate_total():.2f}")
        print("-" * 40)