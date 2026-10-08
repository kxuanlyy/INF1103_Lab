import json
import os

DATA_DIR = os.environ.get("DATA_DIR", ".")
FILE_PATH = os.path.join(DATA_DIR, "inventory.json")


def sample_products():
    return [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
    ]


if __name__ == "__main__":
    print(sample_products())