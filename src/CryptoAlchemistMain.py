import requests
import sys
import time

from config.Config import Config
from EMAtracker import EMAtracker
from GDAXAuth import GDAXAuth
from JsonParser import JsonParser
from tradeHandler.DecisionMaker import DecisionMaker

# Initialize the Main config object
mainConfig = Config()

# Get your connection that the whole program will be using
connection = GDAXAuth(mainConfig.api_key, mainConfig.secret_key, mainConfig.pass_phrase)
jsonParser = JsonParser()
emaTracker = EMAtracker()
decisionMaker = DecisionMaker()

loopCounter = 0
startTime = 0
endTime = 0
# stepValue = 1       #for the gradual stepdown of sell price over time
while True:
    # Connect every 10 times
    if loopCounter % 10 == 0:
        connection = GDAXAuth(mainConfig.api_key, mainConfig.secret_key, mainConfig.pass_phrase)
        loopCounter = 0

    try:
        # Request the most recent Selected Currency price from the GDAX Website
        r = requests.get(mainConfig.gdax_api_url + mainConfig.ticker_end_url, auth=connection)

    except:
        print("Error Getting the most recent price")
        time.sleep(mainConfig.delay)
        continue

    currentMarketPriceSelectedCrypto = None

    try:
        currentMarketPriceSelectedCrypto = jsonParser.parseCryptoCurrencyPrice(r.json())

        if currentMarketPriceSelectedCrypto is None:
            raise Exception

    except:
        print("Error Parsing Price")
        time.sleep(mainConfig.delay)
        continue

    if currentMarketPriceSelectedCrypto is None:
        print('Problem parsing current price restarted loop')
        time.sleep(mainConfig.delay)
        continue

    # Handle decision making pertaining to setting limits
    decisionMaker.makeDecision(float(currentMarketPriceSelectedCrypto), mainConfig, mainConfig.gdax_api_url, connection, emaTracker)
    # print("Main Step Value:", stepValue)
    time.sleep(mainConfig.delay)

    loopCounter += 1

