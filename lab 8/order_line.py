from __future__ import annotations
from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product   # reference — not owned
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity

    def display_line(self) -> None:
        subtotal = self.calculate_subtotal()
        print(f"  {self.product.get_product_id()} - {self.quantity} unit(s) "
              f"@ ${self.product.get_price():.2f} = ${subtotal:.2f}")