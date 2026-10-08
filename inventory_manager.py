import json
import os

# Where inventory.json lives. Defaults to the current folder, but Docker can
# point it at a mounted volume by setting the DATA_DIR environment variable.
DATA_DIR = os.environ.get("DATA_DIR", ".")
FILE_PATH = os.path.join(DATA_DIR, "inventory.json")


# ---------- Data representation ----------

def sample_products():
    """Three starter products, each represented as a dictionary."""
    return [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
    ]


# ---------- Persistence ----------

def load_inventory():
    """Load inventory.json if it exists, otherwise return an empty list."""
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


def save_inventory(inventory):
    """Write the inventory list to inventory.json."""
    print("Saving inventory...")
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(FILE_PATH, "w") as file:
            json.dump(inventory, file, indent=4)
        print("Inventory saved successfully to inventory.json.")
    except OSError as error:
        print(f"Error saving inventory: {error}")


# ---------- Input helpers ----------

def read_price(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Price cannot be negative.")
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


# ---------- Data manipulation (CRUD) ----------

def search_product(inventory, product_id):
    """Return the product dictionary with this ID, or None if not found."""
    for product in inventory:
        if product["id"].upper() == product_id.upper():
            return product
    return None


def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("No products in inventory.")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if search_product(inventory, product_id):
        print("A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    price = read_price("Price: ")
    stock = read_stock("Stock Quantity: ")

    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    product["stock"] = read_stock("New Stock Quantity: ")
    print("Stock updated successfully!")


def search_and_show(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)


# ---------- Menu ----------

def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    # First run: no file yet, so start with three sample products.
    if not inventory:
        inventory = sample_products()
        print("Added 3 sample products.")

    while True:
        show_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_and_show(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
