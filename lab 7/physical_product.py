from product import Product


class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight   # in kg

    def display_information(self):
        super().display_information()
        print(f"  Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        return f"Ships physically. Weight: {self.__weight} kg."