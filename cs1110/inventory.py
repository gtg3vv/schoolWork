import os.path

price = 0

def restock(filename, product, quantity):
    global price

    if os.path.exists(filename): # return the contents of a file
        f = open(filename)
        if product in f:
            price = f.read().strip()
            f = (filename, 'w')
            quantity=+quantity
            print(product,quantity,str(price),file=f)
        else:
            price = input('What is the price of ' + product + '? ')
            f = (filename, 'w')
            print(product,quantity,str(price),file=f)
        f.close()
    else: # get user input and create a file
        # if not there, ask the user and save the file
        price = input('What is the price of '+product+'?')
        with open(filename, 'w') as s:
            print(product, quantity, price, file=s)
    return quantity

def sell(filename, product, quantity):
    global price
    if os.path.exists(filename): # return the contents of a file
        f = open(filename)
        if product in f:
            price = f.read().strip()
            if quantity == 0:
                return None
            else:
                quantity=-quantity
                if quantity<=0:
                    quantity=(quantity*-1)
                    f = open(filename, 'w')
                    print(product, quantity, price, file=f)
                else:
                    f = open(filename, 'w')
                    print(product, quantity, price, file=f)
        else:
            price = input('What is the price of ' + product + '?')
            if quantity == 0:
                return None
            else:
                print(product, quantity, price, file=f)
    else: # get user input and create a file
        # if not there, ask the user and save the file
        price = input('What is the price of '+product+'?')
        with open(filename, 'w') as s:
            print(product, quantity, price, file=s)
            if quantity == 0:
                return None
            else:
                quantity = -quantity
                print(product, quantity, price, file=s)
    return quantity

print(restock('shop.csv', 'toaster', 5))
print(restock('shop.csv', 'marmalade', 5))