import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tboult@6666"
)

cursor = connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS school_project")

cursor.execute("USE school_project")
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tboult@6666",
    database="school_project"
)

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        item VARCHAR(100) PRIMARY KEY,
        quantity INT NOT NULL,
        price INT NOT NULL
    )""")

connection.commit()

cursor.execute("SELECT item, quantity, price FROM inventory")
rows = cursor.fetchall()

stock = {}
stock_price = {}

for row in rows:
    stock[row[0]] = int(row[1])
    stock_price[row[0]] = int(row[2])

cursor.close()
connection.close()



print("Welcome to my Inventory!!!")


def save_inventory():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tboult@6666",
        database="school_project"
    )

    cursor = connection.cursor()

    cursor.execute("DELETE FROM inventory")

    for item in stock:
        cursor.execute(
            "INSERT INTO inventory (item, quantity, price) VALUES (%s, %s, %s)",
            (item, stock[item], stock_price[item])
        )

    connection.commit()

    cursor.close()
    connection.close()


def printer(dic):
    inte=0
    print("S.No."," "*(5-5),"|"," "*(2),"Items"," "*(15-5),"|"," "*(5),"Quantity")
    print("-"*(7)+"|"+"-"*(21)+"|"+"-"*(20))
    for i,j in dic.items():
        inte+=1
        print(inte," "*(5-len(str(inte))),"|"," "*(2),i," "*(15-len(i)),"|"," "*(7),j)
    print("-"*(7)+"|"+"-"*(21)+"|"+"-"*(20))

def printer2(dic1,listi,lista,listin=None,dic2=None):
    if dic2 is not None:
        listin=[j for i,j in dic2.items()]
    a,b,c,d,e=lista
    inte=0
    print(a," "*(5-5),"|"," "*(2),b," "*(15-5),"|"," "*(3),c," "*(3),"|"," "*(1),d," "*(16-len(d)),"|"," "*(3),e)
    print("-"*(7)+"|"+"-"*(21)+"|"+"-"*(18)+"|"+"-"*(21)+"|"+"-"*(22))
    for (i,j),l,m in zip(dic1.items(),listin,listi):
        inte+=1
        print(inte," "*(5-len(str(inte))),"|"," "*(2),i," "*(15-len(i)),"|"," "*(6),j," "*(8-len(str(j))),"|"," "*3,l," "*(14-len(str(l))),"|"," "*(5),m)
    print("-"*(7)+"|"+"-"*(21)+"|"+"-"*(18)+"|"+"-"*(21)+"|"+"-"*(22))

def overview():
    print()
    print("Inventory Overview")
    print()
    list_of_total=[]
    list22=["S.No.","Items","Quantity","Price Per Piece","Total Price"]
    for (a,b),(c,d) in zip(stock.items(),stock_price.items()):
        tot=b*d
        list_of_total.append(tot)
    printer2(stock,list_of_total,list22,[],stock_price)


def order(ord_list=None):
    list1=["S.No.","Items","Quantity","Available","Availability"]
    list2=["S.No.","Items","Quantity","Price Per Piece","Total Price"]
    if ord_list==None:
        ord_list={}
    confirmed={}
    stat=[]
    while True:
        try:
            n=int(input("Enter the number of items in your shopping list: "))
            break
        except ValueError:
            print("Invalid Datatype Entered")
            continue
    for i in range(n):
        item=input(f"Enter item number {i+1} you want: ").title().strip()
        while True: 
            try:
                amount=int(input(f"Enter the amount of item number {i+1} you want: "))
                break
            except ValueError:
                print("Invalid Datatype Entered")
                continue
        ord_list.update({item:amount})
    while True:
        try:
            xy=int(input("Enter 1 if you want to confirm the order list else enter 0: "))
            break
        except ValueError:
            print("Invalid Datatype Entered")
            continue
    if xy==0:
        return order(ord_list)
    elif xy==1:
        print("Order List Confirmed")
        printer(ord_list)
    

    for i,j in ord_list.items():
        if i in stock.keys():
            if j>stock[i]:
                available=stock[i]
                confirmed.update({i:available})
                status="Not Fully"
            else:
                available=j
                confirmed.update({i:available})
                status="Fully"
        else:
            available=0
            status="Not Available"
        stat.append(status)
    print()
    print()
    print("Final Order List")
    print()
    l_of_avail = [stock.get(i, 0) for i in ord_list]
    printer2(ord_list,stat,list1,l_of_avail)

    print()
    print()
    print("Final Bill")
    print()
    l_of_price=[]
    l_per_piece=[]

    for i,j in confirmed.items():
        p = stock_price.get(i, 0)
        stock[i] = max(stock[i] - j, 0)
        l_per_piece.append(p)
        tot=p*j
        l_of_price.append(tot)
        
        if stock[i] == 0:
            stock_price.pop(i)
            stock.pop(i)

    printer2(confirmed,l_of_price,list2,l_per_piece)
    print()
    print("Total Bill:",sum(l_of_price))
    again = input("Do you want to place another order? (yes/no): ").lower()
    if again == "yes":
        order()
    else:
        print("Thanks for shopping with us!")
    return stock


def refil():
    while True:
        try:
            num=int(input("Enter the number of items you want to add in the inventory."))
            break
        except ValueError:
            print("Invalid Input Entered")
            continue
    for i in range(num):
        item=input("Enter the item you want to add in the Inventory: ").title()
        while True: 
            try:
                qty=int(input("Enter the quantity of the item you want to add: "))
                break
            except ValueError:
                print("Invalid Datatype Entered")
                continue
        if item in stock:
            stock[item] += qty
            print(f"Updated '{item}' — new quantity: {stock[item]}")
        else:
            stock[item] = qty
            while True:
                try:
                    price = int(input(f"Enter the price for '{item}': "))
                    stock_price[item] = price
                    break
                except ValueError:
                    print("Invalid input! Please enter a number.")
            print(f"Added new item '{item}' with quantity {qty} and price ₹{price}.")

    return stock,stock_price

def clear():
    while True:
        try:
            x=int(input("Enter 1 if you are sure to remove all the items from the inventory else press 0: "))
            break
        except ValueError:
            print("Invalid Datatype Entered.")
            continue
    if x==1:
        stock.clear()
    else:
        print("The inventory will remain as it was.")
    return stock,stock_price
    

def main():
    print("\nWelcome to My Inventory Management System ")

    while True:
        print("\nChoose an option:")
        print("1. View Inventory Overview")
        print("2. Place an Order")
        print("3. Refill Stock")
        print("4. To Clear the Inventory")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            overview()
        elif choice == "2":
            order()
        elif choice == "3":
            refil()
        elif choice == "4":
            clear()
        elif choice == "5":
            print("Exiting... Thank you for using the Inventory System!")
            break
        else:
            print("Invalid choice. Please try again.")
        


        if choice in ["2", "3", "4"]:
            save_inventory()
main()
