import json
import os

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

FILE_PATH = "inventory.json"


# ---------- File handling ----------

def load_inventory(inventory):
    if not os.path.exists(FILE_PATH):
        print("inventory.json not found. Starting with an empty inventory.")
        return
    print("inventory.json found.")
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
        for item in data:
            product_type = item.get("type")
            if product_type == "physical":
                product = PhysicalProduct(
                    item["id"], item["name"], item["price"], item["stock"], item["weight"]
                )
            elif product_type == "digital":
                product = DigitalProduct(
                    item["id"], item["name"], item["price"], item["stock"], item["download_size"]
                )
            else:
                print(f"Unknown product type '{product_type}', skipping.")
                continue
            inventory.add_product(product)
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, KeyError, OSError):
        print("Could not read inventory.json.")


def save_inventory(inventory):
    print("Saving inventory...")
    data = [product.to_dict() for product in inventory.get_products()]
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)
    print("Inventory saved successfully to inventory.json.")


# ---------- Input helpers ----------

def read_price(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def read_stock(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Stock cannot be negative.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


# ---------- Menu actions ----------

def add_product_prompt(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id):
        print("A product with that ID already exists.")
        return
    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    price = read_price("Price: ")
    stock = read_stock("Stock Quantity: ")

    print("Product Type:")
    print("  1. Physical")
    print("  2. Digital")
    type_choice = input("Enter type (1 or 2): ").strip()

    if type_choice == "1":
        weight = read_price("Weight (kg): ")
        inventory.add_product(PhysicalProduct(product_id, name, price, stock, weight))
    elif type_choice == "2":
        download_size = read_price("Download Size (MB): ")
        inventory.add_product(DigitalProduct(product_id, name, price, stock, download_size))
    else:
        print("Invalid type. Product not added.")
        return

    print("Product added successfully!")


def update_stock_prompt(inventory):
    print("\nUpdate Stock")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    product.display_information()
    product.update_stock(read_stock("New Stock Quantity: "))
    print("Stock updated successfully!")


def search_prompt(inventory):
    print("\nSearch Product")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    product.display_information()


def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


# ---------- Main program ----------

def main():
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
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()