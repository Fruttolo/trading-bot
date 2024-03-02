from binance.client import Client
from account import Account

# Constants
PAIR = "BTCEUR"
QUANTITY = 0.001
STOPLOSS = 0
TAKEPROFIT = 1

# Initialize the Binance client
client = Client()
account = Account(1000)
account.verbose = False

# Fetch
candles = client.get_historical_klines(PAIR,'1m', "21 Feb, 2024", "26 Feb, 2024")

candlesCalculate = client.get_historical_klines(PAIR,'1d', "16 Feb, 2024", "21 Feb, 2024")
high = 0
low = 1000000
for candle in candlesCalculate:
    if float(candle[2]) > high:
        high = float(candle[2])
    if float(candle[3]) < low:
        low = float(candle[3])
quarter = (high - low) / 4
entry = low + quarter

for candle in candles:
    #print(candle[2]) # High
    #print(candle[3]) # Low
    #print()

    if float(candle[2]) <= entry:
        account.buy(QUANTITY, candle[4], TAKEPROFIT, STOPLOSS)

    if float(candle[2]) < low:
        low = float(candle[2])
        quarter = (high - low) / 4
        entry = low + quarter
    
    if float(candle[3]) > high:
        high = float(candle[3])
        quarter = (high - low) / 4
        entry = low + quarter

    account.check_tp_sl(candle[2], candle[3])


print()
print("Last Price:", candles[-1][4])
print("Pending orders:", account.n_pending_orders())

account.sellAll(candles[-1][4])

print("Final balance:", account.get_balance())
print("Number of buys:", account.get_n_orders())
print()

