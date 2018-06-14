import json
import time
import requests

from JsonParser import JsonParser
from database.Database import CryptoDatabase


class TradeHandler:

    def __init__(self, connection, config):
        self.config = config
        self.connection = connection
        self.jsonParser = JsonParser()
        self.database = CryptoDatabase()


    def buy(self, currentSelectedCryptoPrice):
        r = None

        try:
            r = requests.get(self.config.gdax_api_url + '/accounts', auth=self.connection)
        except:
            print("Error getting account info")
            if r.json() in None:
                print(r.json())
            return

        usdInBank = self.jsonParser.parseUsdBalance(r.json())

        size = (usdInBank / float(currentSelectedCryptoPrice))

        print('USD: ', usdInBank)
        print('Size: ', round(size, 8))

        #move the messages out of the methods and into their own class
        buy_limit_order = {
            'type': 'limit',
            'side': 'buy',
            'product_id': self.config.currency.value[0],
            'size': round(size, 8),
            'price': round(currentSelectedCryptoPrice, 2),
            'post_only': True,
            'time_in_force': 'GTT',
            'cancel_after': 'hour'
        }

        response = requests.post(self.config.gdax_api_url + '/orders', data=json.dumps(buy_limit_order), auth=self.connection)

        if response.json() is not None:
            print('buy response: ', response.json())
            print('Buy Order Sent: ', round(size, 8), ' At Price: ', buy_limit_order['price'], ' Time in Force: ')

        if 'message' in response.json().keys():
            print("Error submitting buy limit order")
            print(response.json())
            print()
        else:
            # TODO make a general util class and the first function in there should be a time getter
            self.database.insertBuyHistoryEntry(int(round(time.time() * 1000)), "GDAX", self.config.currency.value[0], buy_limit_order['price'])


    def sell(self, sell_price):
        try:
            r = requests.get(self.config.gdax_api_url + '/accounts', auth=self.connection)
        except:
            print("Error getting account info")
            return

        holdAmount = -1

        try:
            holdAmount = self.jsonParser.parseHoldingAmountSelectedCurrency(r.json(), self.config)
        except:
            print("Error getting hold amount")
            return

        # Error Parsing
        if holdAmount == -1:
            print("Error Parsing hold amount")
            return

        sell_order = {
            'type': 'limit',
            'side': 'sell',
            'product_id': self.config.currency.value[0],
            'size':  round(holdAmount, 8),
            'price': round(sell_price, 2),
            'post_only': True,
            'time_in_force': 'GTT',
            'cancel_after': 'hour'
        }


        response = requests.post(self.config.gdax_api_url + '/orders', data=json.dumps(sell_order), auth=self.connection)

        print('sell response: ', response.json())


        if 'message' in response.json().keys():
            print("Error submitting buy limit order")
            print(response.json())
            print()