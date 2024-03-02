from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os

# Constants
# Load the environment variables from .env file
load_dotenv()

# Get the API key
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PAIR = os.getenv("PAIR")

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

def getPrice():
    price = client.get_symbol_ticker(symbol=PAIR)
    return price['price']

def buyMarket(quantity):
    order = client.create_order(
        symbol=PAIR,
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=quantity
    )
    return order

def buyLimit(quantity, price):
    order = client.create_order(
        symbol=PAIR,
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=quantity,
        price=price
    )
    return order

def sellLimit(quantity, price):
    order = client.create_order(
        symbol=PAIR,
        side=SIDE_SELL,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=quantity,
        price=price
    )
    return order

def calculateOrderProfit(order):
    if order['side'] == 'BUY':
        buyPrice = float(order['price'])
        sellPrice = float(getPrice())
    else:
        sellPrice = float(order['price'])
        buyPrice = float(getPrice())
    return ((sellPrice - buyPrice) / buyPrice) * 100

def getOrders():
    orders = client.get_all_orders(symbol=PAIR)
    return orders

def getBalance():
    balance = client.get_asset_balance(asset='EUR')
    return balance

def calculateLastWeekHighLow():
    klines = client.get_historical_klines(PAIR, Client.KLINE_INTERVAL_1WEEK, "1 week ago UTC")
    lastWeekHigh = 0
    lastWeekLow = 999999999
    for kline in klines:
        lastWeekHigh = max(lastWeekHigh, float(kline[2]))
        lastWeekLow = min(lastWeekLow, float(kline[3]))
    return lastWeekHigh, lastWeekLow

def calculateLastMonthHighLow():
    klines = client.get_historical_klines(PAIR, Client.KLINE_INTERVAL_1MONTH, "1 month ago UTC")
    lastMonthHigh = 0
    lastMonthLow = 999999999
    for kline in klines:
        lastMonthHigh = max(lastMonthHigh, float(kline[2]))
        lastMonthLow = min(lastMonthLow, float(kline[3]))
    return lastMonthHigh, lastMonthLow

def calculateHighLow(interval, time):
    klines = client.get_historical_klines(PAIR, interval, time)
    high = 0
    low = 999999999
    for kline in klines:
        high = max(high, float(kline[2]))
        low = min(low, float(kline[3]))
    return high, low

def percentageChange(price1, price2):
    return ((price2 - price1) / price1) * 100

print(getPrice())

# Calulate 1/4 of the ranfe between the high and low of the last week
lastWeekHigh, lastWeekLow = calculateLastMonthHighLow()
print(lastWeekHigh, lastWeekLow)
lastWeekRange = lastWeekHigh - lastWeekLow
print(lastWeekRange)
quarterRange = lastWeekRange / 4
buyLimitPrice = (lastWeekLow + quarterRange)
print(buyLimitPrice)
sellLimitPrice = (lastWeekHigh - quarterRange)
print(sellLimitPrice)
print(percentageChange(buyLimitPrice, sellLimitPrice))

