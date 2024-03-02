class Order:
    def __init__(self, id ,amount, price, tp, sl):
        self.amount = amount
        self.price = price
        self.tp = tp
        self.sl = sl
        self.id = id