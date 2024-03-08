import datetime
class Order:
    def __init__(self, id ,amount, price, tp, sl):
        self.amount = amount
        self.price = price
        self.tp = tp
        self.sl = sl
        self.id = id

class Balance:
    def __init__(self, amount):
        self.amount = amount

    def add(self, amount):
        self.amount += amount

    def remove(self, amount):
        self.amount -= amount

    def get(self):
        return self.amount

class Account:

    def commission(self, side, amount):
        COMMISSION = 0.001
        if side == 'buy':
            return amount * (1 + COMMISSION)
        else:
            return amount * (1 - COMMISSION)

    def __init__(self, balance=1000):
        self.balance = Balance(balance)
        self.orders = []
        self.id_order = 0
        self.verbose = False
    
    def stoploss(self, price, percent):
        if percent == 0:
            return 0
        return price - (price * percent / 100)

    def takeprofit(self, price, percent):
        if percent == 0:
            return 0
        return price + (price * percent / 100)

    def buy(self, amount, price, tp=0, sl=0):
        price = float(price)
        if amount * price > self.get_balance():
            if self.verbose:
                print("Not enough balance")
            return
        self.orders.append(Order(self.id_order, amount, price, tp, sl))
        self.balance.remove(self.commission('buy',amount * price))
        self.id_order += 1
        with open("logfile.txt", "a") as file:
            file.write("[" + str(datetime.datetime.now()) + "] BoughtAt:" + str(price) + " SL:" + str(sl) + " TP:" + str(tp) + " Q:" + str(price*amount) + "\n")

    def check_tp_sl(self, high, low):
        high = float(high)
        low = float(low)
        toRemove = []
        for order in self.orders:
            if order.sl != 0 and low <= order.sl:
                self.balance.add(self.commission('sell',order.amount * order.sl))
                with open("logfile.txt", "a") as file:
                    file.write("[" + str(datetime.datetime.now()) + "] SellAt:" + str(high) + " P:" + str((order.amount*order.sl)) + " StopLoss" + "\n")
                toRemove.append(order)
                if self.verbose:
                    print("Stop loss: ", (order.amount * order.sl))
            elif order.tp != 0 and high >= order.tp:
                self.balance.add(self.commission('sell',order.amount * order.tp))
                with open("logfile.txt", "a") as file:
                    file.write("[" + str(datetime.datetime.now()) + "] SellAt:" + str(high) + " P:" + str((order.amount*order.tp)) + " TakeProfit" + "\n")
                toRemove.append(order)
                if self.verbose:
                    print("Take profit: ", (order.amount * order.tp))
        for id in toRemove:
            self.orders.remove(id)


    def print_orders(self):
        for order in self.orders:
            print(order.id, order.amount, order.price, order.tp, order.sl)

    def n_pending_orders(self):
        return len(self.orders)

    def get_balance(self):
        return self.balance.get()
    
    def sellAll(self, price):
        price = float(price)
        for order in self.orders:
            self.balance.add(self.commission('sell',order.amount * price))
        self.orders = []

    def get_n_orders(self):
        return self.id_order

# test methods
    
""" account = Account()
account.verbose = True
account.buy(1, 100, 110, 90)
account.buy(1, 100, 110, 90)
account.buy(1, 100, 110, 90)
account.print_orders()
print(account.get_balance())
account.check_tp_sl(110, 90)
print(account.get_balance())
account.print_orders()
account.sellAll(100)
print(account.get_balance()) """

