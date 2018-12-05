# -*- coding: utf-8 -*- 
import MySQLdb

items = {}

menu = '''  ========= Inventory Tracker Menu =========   
    1. List current inventory   
    2. Add inventory   
    3. Delete inventory   
    4. Get inventory from database   
    5. Commit to database   
    6. Exit   
    Please make your selection:  '''

def print_items():
    global items
    print("========= Current Inventory =========\n")
    if items == {}:
        print("None (your inventory is currently empty)\n")
    else:
        i = 1
        for name in items:
            print("%d. %s (quantity: %d)\n"%(i, name, items[name]))
            i += 1
    return

def add_item():
    global items
    name = raw_input("Input item name: ")
    quantity = raw_input("Input item quantity: ")
    try:
        quantity = int(quantity)%4294967295
    except Exception:
        print('Invalid number: %s'%(quantity))
        return 
    
    if name in items:
        items[name] += quantity
    else:
        items[name] = quantity
    
    print("Adding item %s with quantity %d"%(name, quantity))
    return 

def delete_item():
    global items
    name = raw_input("Input item you would like to remove: ")
    if name in items:
        quantity = raw_input("How many of this item would you like to remove: ")
        try:
            quantity = int(quantity)
        except Exception:
            print('Invalid number: %s'%(quantity))
            return 
        if quantity >= items[name]:
            items[name] = 0
            print("Updated item %s to quantity %u.\n"%(name, items[name]))
            del items[name]
        else:
            items[name] = items[name] - quantity
            print("Updated item %s to quantity %u.\n"%(name, items[name]))
    else:
        print("Could not find item %s in inventory list. Please try again.\n"%(name))
    

def get_inventory_from_db(conn):
    cursor = conn.cursor()
    query = "SELECT * FROM Items"
    cursor.execute(query)
    values = cursor.fetchall()
    i = 1
    for e in values:
        print("%d. %s (quantity: %s)"%(i, e[0], int(e[1])))
        i+=1
    cursor.close()

def commit_db(conn):
    global items
    cursor = conn.cursor()
    try:
        for name in items:
            cursor.execute("insert into Items values (%s, %s)", (name, items[name]))
    except Exception:
        print("Error while insert item: %s with quantity %d.\n"%(name, items[name]))
        return
    conn.commit()
    cursor.close()
    print("Successfully committed inventory to database. Exiting.\n")
    exit()

def main():
    global items
    conn = MySQLdb.connect(host = '10.0.22.7', user = 'inventoryuser', db = 'inventory', passwd = 'Mdq4LVBl7HRp5fxCcB', port = 3306)
    while True:
        print(menu)
        inp = raw_input()
        if len(inp) < 1 or inp[0] not in '123456':
            print("Invalid selection. Please try again.\n\n")
            continue
        print("You selected option: \n" + inp[0])
        if inp[0] is '1':
            print_items()
        elif inp[0] is '2':
            add_item()
        elif inp[0] is '3':
            delete_item()
        elif inp[0] is '4':
            get_inventory_from_db(conn)
        elif inp[0] is '5':
            commit_db(conn)
        elif inp[0] is '6':
            if items != {}:
                print("You have unsaved changes.")
            inp = raw_input("Are you sure you want to exit? (y/N) ")
            if inp[0] == 'y' or inp[0] == 'Y':
                break
            else:
                continue
        else:
            print("Invalid selection. Please try again.\n\n")
            continue
    
    conn.close()
    return

if __name__ == "__main__":
    main()
