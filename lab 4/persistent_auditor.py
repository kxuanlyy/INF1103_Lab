def get_valid_input():
    value = input("Enter the stock quantity, or type 'quit' to exit: ")
    
    if value == 'quit':
        return 'quit'
    
    if not value.isdigit():
        print("Invalid input. Please enter a valid non-negative number.")
        return None
    
    return int(value)


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, deliveries_processed, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Units Processed:", total_units)
    print("Total Deliveries Processed:", deliveries_processed)
    print("Number of Failed/Rejected Entries:", failed_attempts)

def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            total = int(file.readline().strip())

            history_line = file.readline().strip()
            history = [
                int(value)
                for value in history_line.split(",")
                if value
            ]

            return total, history

    except FileNotFoundError:
        return 0, []



def main():
    inventory, history = load_inventory()
    deliveries_processed = 0
    failed_entries = 0

    while True:
        result = get_valid_input()

        if result == 'quit':
            break

        if result is None:
            failed_entries += 1
            continue

        inventory = process_delivery(inventory, result)
        history.append(result)
        tax = calculate_tax(result)
        deliveries_processed += 1

        print(f"Current inventory: {inventory} | Tax on this delivery: {tax:.2f}")

        if inventory >= 500:
            print("Inventory limit reached. Cannot add more stock.")
            break

    generate_report(inventory, deliveries_processed, failed_entries)


if __name__ == "__main__":
    main()



