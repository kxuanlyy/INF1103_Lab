import csv
import json
import os

from inventory import Inventory
from supplier import Supplier
from product import Product
from product_factory import ProductFactory

FILE_PATH = "inventory.json"

# ---------- Pre-defined suppliers ----------

SUPPLIERS: list[Supplier] = [
    Supplier("S001", "TechWorld", "techworld@example.com"),
    Supplier("S002", "DigitalHub", "hub@example.com"),
    Supplier("S003", "MegaStore", "mega@example.com"),
]


def find_supplier(supplier_id: str) -> Supplier | None:
    for s in SUPPLIERS:
        if s.get_supplier_id() == supplier_id:
            return s
    return None


# ---------- File handling ----------

def load_inventory(inventory: Inventory) -> None:
    if not os.path.exists(FILE_PATH):
        print("inventory.json not found. Starting with an empty inventory.")
        return
    print("inventory.json found.")
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
        for item in data:
            supplier = find_supplier(item.get("supplier_id", ""))
            if supplier is None:
                supplier = SUPPLIERS[0]   # fallback to first supplier
            product_type = item.get("type")
            try:
                product = ProductFactory.create(
                    product_type,
                    item["id"], item["name"], item["price"], item["stock"], supplier,
                    weight=item.get("weight", 0.0),
                    download_size=item.get("download_size", 0.0),
                )
                inventory.add_product(product)
            except ValueError as e:
                print(f"Skipping product '{item.get('id')}': {e}")
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, KeyError, OSError):
        print("Could not read inventory.json.")


def save_inventory(inventory: Inventory) -> None:
    print("Saving inventory...")
    data = [product.to_dict() for product in inventory.get_products()]
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)
    print("Inventory saved successfully to inventory.json.")


# ---------- CSV loader ----------

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader)   # skip header row
            loaded = 0
            for row in reader:
                try:
                    product_type, product_id, name, price_str, stock_str = row
                    product = ProductFactory.create(
                        product_type, product_id, name,
                        float(price_str), int(stock_str), supplier
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as e:
                    print(f"Skipping row {row}: {e}")
            print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


# ---------- Input helpers ----------

def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def read_stock(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Stock cannot be negative.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def pick_supplier() -> Supplier:
    print("Available suppliers:")
    for i, s in enumerate(SUPPLIERS, 1):
        s.display_information()
    while True:
        try:
            choice = int(input(f"Choose supplier (1-{len(SUPPLIERS)}): "))
            if 1 <= choice <= len(SUPPLIERS):
                return SUPPLIERS[choice - 1]
            print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")


# ---------- LSP demo ----------

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


# ---------- Menu actions ----------

def add_product_prompt(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.find_product(product_id):
        print("A product with that ID already exists.")
        return
    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    price = get_positive_float("Price: ")
    stock = read_stock("Stock Quantity: ")
    supplier = pick_supplier()

    print("Product Type:")
    print("  1. Physical")
    print("  2. Digital")
    type_choice = input("Enter type (1 or 2): ").strip()

    try:
        if type_choice == "1":
            weight = get_positive_float("Weight (kg): ")
            product = ProductFactory.create("physical", product_id, name, price, stock, supplier, weight=weight)
        elif type_choice == "2":
            download_size = get_positive_float("Download Size (MB): ")
            product = ProductFactory.create("digital", product_id, name, price, stock, supplier, download_size=download_size)
        else:
            print("Invalid type. Product not added.")
            return
        inventory.add_product(product)
        print("Product added successfully!")
    except ValueError as e:
        print(f"Could not add product: {e}")


def update_stock_prompt(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product = inventory.find_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    product.display_information()
    product.update_stock(read_stock("New Stock Quantity: "))
    print("Stock updated successfully!")


def search_prompt(inventory: Inventory) -> None:
    print("\nSearch Product")
    product = inventory.find_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    show_product_details(product)   # uses LSP demo function


def show_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Load from CSV")
    print("7. Exit")
    print("----------------------------")


# ---------- Main ----------

def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = Inventory()
    load_inventory(inventory)

    while True:
        show_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_prompt(inventory)
        elif choice == "3":
            update_stock_prompt(inventory)
        elif choice == "4":
            search_prompt(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            load_products("products.csv", inventory, SUPPLIERS[0])
        elif choice == "7":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
