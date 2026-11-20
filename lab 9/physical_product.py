from __future__ import annotations
from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"  Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        return f"Ships physically. Weight: {self.__weight} kg."

    def calculate_shipping_cost(self) -> float:
        return round(self.__weight * 2.5, 2)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data