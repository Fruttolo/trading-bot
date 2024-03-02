from binance.client import Client
from account import Account

# Constants
PAIR = "EURUSDT"
QUANTITY = 1
STOPLOSS = 0
TAKEPROFIT = 1

# Initialize the Binance client
client = Client()
account = Account(1000)
account.verbose = False

# Fetch
candles = client.get_historical_klines(PAIR,'1m','1 month ago UTC')

for candle in candles:
    #print(candle[2]) # High
    #print(candle[3]) # Low
    #print()

    account.buy(QUANTITY, candle[4], TAKEPROFIT, STOPLOSS)
    account.check_tp_sl(candle[2], candle[3])


print()
print("Last Price:", candles[-1][4])
print("Pending orders:", account.n_pending_orders())

account.sellAll(candles[-1][4])

print("Final balance:", account.get_balance())
print("Number of buys:", account.get_n_orders())
print()

