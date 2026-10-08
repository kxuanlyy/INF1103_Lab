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


def load_inventory():
    if os.path.exists(FILE_PATH):
        print("inventory.json found.")
        try:
            with open(FILE_PATH, "r") as file:
                inventory = json.load(file)
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError):
            print("Could not read inventory.json. Starting with an empty inventory.")
            return []
    print("inventory.json not found. Starting with an empty inventory.")
    return []

if __name__ == "__main__":
    print(load_inventory())