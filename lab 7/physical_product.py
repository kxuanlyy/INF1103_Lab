from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight   # in kg

    def display_information(self):
        super().display_information()
        print(f"  Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        return f"Ships physically. Weight: {self.__weight} kg."

    def calculate_shipping_cost(self):
        return round(self.__weight * 2.5, 2)   # $2.50 per kg

    def to_dict(self):
        data = super().to_dict()       # gets {"id", "name", "price", "stock"}
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data