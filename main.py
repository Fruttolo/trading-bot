from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os
from time import sleep
import datetime
from account import Account


# Constants
# Load the environment variables from .env file
load_dotenv()

# Get the API key
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PAIR = os.getenv("PAIR")
QUANTITY = os.getenv("QUANTITY")
QUANTITY = float(QUANTITY)

account = Account(1000)

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

def getPrice():
    price = client.get_symbol_ticker(symbol=PAIR)
    return price['price']

def getBalance():
    balance = client.get_asset_balance(asset='EUR')
    return balance

def calculateHighLow():
    klines = client.get_historical_klines(PAIR, "1m", "1 hour ago UTC")
    lastWeekHigh = 0
    lastWeekLow = 1000000
    for candle in klines:
        if float(candle[2]) > lastWeekHigh:
            lastWeekHigh = float(candle[2])
        if float(candle[3]) < lastWeekLow:
            lastWeekLow = float(candle[3])
    return float(lastWeekHigh), float(lastWeekLow)

waiting = False
while True:

    # Calulate 1/4 of the ranfe between the high and low of the last week
    lastWeekHigh, lastWeekLow = calculateHighLow()
    currentPrice = float(getPrice())
    lastWeekRange = lastWeekHigh - lastWeekLow
    quarterRange = lastWeekRange / 4
    entry = (lastWeekLow + quarterRange)
    percentRange = round(1 + (quarterRange / entry), 4)

    print("percentRange:",percentRange)
    print("lastWeekHigh:",lastWeekHigh)
    print("lastWeekLow:",lastWeekLow)
    print("Entry:",entry)
    print("Current:",currentPrice)
    print("Pending orders:", account.n_pending_orders())
    print("Balance available:", account.get_balance())
    print("Waiting:",waiting)
    print()

    if(currentPrice < entry and waiting == False):
        TAKEPROFIT = entry + (quarterRange * 2)
        STOPLOSS = entry - quarterRange

        """ order = client.create_test_order(
            symbol=PAIR,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=QUANTITY,  # Replace with the desired quantity to buy
        ) """

        """ client.create_test_order(
            symbol=PAIR,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            quantity=QUANTITY,  # Replace with the desired quantity to sell
            price=TAKEPROFIT,
        )
        print("Bought at:",order['price']) """

        """ client.create_test_order(
            symbol=PAIR,
            side=SIDE_SELL,
            type=ORDER_TYPE_STOP_LOSS_LIMIT,
            quantity=QUANTITY,  # Replace with the desired quantity to sell
            stopPrice=STOPLOSS,
            price=STOPLOSS,
        ) """

        account.buy(QUANTITY, currentPrice, TAKEPROFIT, STOPLOSS)
        waiting = True

        with open("logfile.txt", "a") as file:
            file.write("[" + str(datetime.datetime.now()) + "] BoughtAt:" + str(currentPrice) + " SL:" + str(STOPLOSS) + " TP:" + str(TAKEPROFIT) + " Q:" + str(currentPrice*QUANTITY) + "\n")

    if(currentPrice > entry + (quarterRange*2) and waiting == True):
        waiting = False
        with open("logfile.txt", "a") as file:
            file.write("[" + str(datetime.datetime.now()) + "] WAITING:FALSE" + "\n")

    account.check_tp_sl(currentPrice, currentPrice)
    sleep(1)

