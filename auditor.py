inventory = 0
failed_entries = 0

while True:
    stock_quantity = input("Enter the stock quantity, or type 'quit' to exit: ")
    if stock_quantity == 'quit':
        break
    is_negative = stock_quantity.startswith("-")
    digits = stock_quantity[1:] if is_negative else stock_quantity

    if not digits.isdigit():
        print("Invalid input. Please enter a valid number.")
        failed_entries += 1
        continue

    if int(stock_quantity) < 0:
        print("Invalid input. Please enter a non-negative number.")
        failed_entries += 1
        continue
    
    inventory += int(stock_quantity)
    if inventory >= 500:
        print("Inventory limit reached. Cannot add more stock.")
        failed_entries += 1
        break

    print(f"Current inventory: {inventory}")


print("The total unit processed is:", inventory)
print("The total failed/ rejected entries is:", failed_entries)
