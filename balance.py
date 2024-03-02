class Balance:
    def __init__(self, amount):
        self.amount = amount

    def add(self, amount):
        self.amount += amount

    def remove(self, amount):
        self.amount -= amount

    def get(self):
        return self.amount