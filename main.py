from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os
from time import sleep

# Constants
# Load the environment variables from .env file
load_dotenv()

# Get the API key
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PAIR = os.getenv("PAIR")
QUANTITY = os.getenv("QUANTITY")
TAKEPROFIT = float(os.getenv("TAKEPROFIT"))
STOPLOSS = float(os.getenv("STOPLOSS"))

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

def getPrice():
    price = client.get_symbol_ticker(symbol=PAIR)
    return price['price']

def getBalance():
    balance = client.get_asset_balance(asset='EUR')
    return balance

def calculateHighLow():
    klines = client.get_historical_klines(PAIR, "1w", "1 week ago UTC")
    lastWeekHigh = klines[-1][2]
    lastWeekLow = klines[-1][3]
    return float(lastWeekHigh), float(lastWeekLow)

waiting = False
while True:
    # Calulate 1/4 of the ranfe between the high and low of the last week
    lastWeekHigh, lastWeekLow = calculateHighLow()
    currentPrice = float(getPrice())
    lastWeekRange = lastWeekHigh - lastWeekLow
    quarterRange = lastWeekRange / 4
    entry = (lastWeekLow + quarterRange)
    percentRange = 1 + (quarterRange / entry)
    print("percentRange:",percentRange)
    print("Entry:",entry)
    print("Current:",currentPrice)
    print("Waiting:",waiting)
    print()

    if(currentPrice < entry and waiting == False):
        print("Buying")
        order = client.create_test_order(
            symbol=PAIR,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=QUANTITY,  # Replace with the desired quantity to buy
        )

        take_profit_price = float(order['price']) * TAKEPROFIT  # Set take profit price as 1% above the buy price

        client.create_test_order(
            symbol=PAIR,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            quantity=QUANTITY,  # Replace with the desired quantity to sell
            price=take_profit_price,
        )
        print("Bought at:",order['price'])

        stop_loss_price = float(order['price']) * STOPLOSS  # Set stop loss price as 1% below the buy price

        client.create_test_order(
            symbol=PAIR,
            side=SIDE_SELL,
            type=ORDER_TYPE_STOP_LOSS_LIMIT,
            quantity=QUANTITY,  # Replace with the desired quantity to sell
            stopPrice=stop_loss_price,
            price=stop_loss_price,
        )

        waiting = True

    if(currentPrice > entry + quarterRange and waiting == True):
        waiting = False

    sleep(1)
