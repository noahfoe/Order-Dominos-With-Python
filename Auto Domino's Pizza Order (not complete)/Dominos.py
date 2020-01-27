from pizzapy import Customer, StoreLocator, Order, ConsoleInput

TAXRATE = .0825

def searchMenu(menu):
    print("You are now searching the menu...")
    item = input("Type an item to look for: ").strip().lower()

    if len(item) > 1:
        item = item[0].upper() + item[1:]
        print(f"Results for: {item}\n")
        menu.search(Name=item)
        print()
    else:
        print("invalid, exiting search...")

def addToOrder(order):
    print("Type the codes of the items you want to order...")
    print("Press ENTER to stop ordering.")
    while True:
        item = input("Code: ").upper()
        try:
            order.add_item(item)
        except:
            if item == "":
                break
            print("Invalid Code...")

def show_stores(customer, k):
    print("\nFinding Closest Stores...")
    print("\n- CLOSEST STORES -")
    k_local_dominos = StoreLocator.find_k_closest_stores_to_customer(customer, k)
    for i, store in enumerate(k_local_dominos):
        print(str(i+1) + ".")
        print(store)
        print()

customer = Customer("Noah", "Foley", "noahfoley6@gmail.com", "9039181598", "40 Bay Street, Toronto, ON, M5J2X2")
# customer = ConsoleInput.get_new_customer()
my_local_dominos = StoreLocator.find_closest_store_to_customer(customer)
print("\nClosest Store: ")
print(my_local_dominos)

ans = input("Would you like to order from this store (y/n)? ")
if ans.lower() not in ["yes", "y"]:
    print("Goodbye!")
    quit()

print("\nMENU\n")
menu = my_local_dominos.get_menu()
order = Order.begin_customer_order(customer, my_local_dominos, "ca")

while True:
    searchMenu(menu)
    addToOrder(order)
    answer = input("Would you like to add more items (y/n)? ")
    if answer.lower() not in ["yes", "y"]:
        break

subtotal = 0
taxAmount = 0
total = 0
print("\nYour order is... ")
for item in order.data["Products"]:
    price = item["Price"]
    subtotal += float(item["Price"])
    taxAmount = subtotal * TAXRATE
    total = subtotal + taxAmount
    # TODO: remove items from order using order.remove_item('ITEM CODE HERE')

print("\nYour total before tax is: $" + str(subtotal) + "\n")
print("\nYour tax amount is: $" + str(taxAmount) + "\n")
print("\nYour total after tax is: $" + str(total) + "\n")

payment = input("\nWill you being paying with cash or a credit card? (cash, credit card)")
if payment.lower() in ["card", "credit card"]:
    card = ConsoleInput.get_credit_card()
else:
    card = False

ans = input("Would you like to place this order (y/n)? ")
if ans.lower() in ["y", "yes"]:
    order.place(card)
    my_local_dominos.place_order(order, card)
    print("Order Placed!")
else:
    print("Goodbye!")
