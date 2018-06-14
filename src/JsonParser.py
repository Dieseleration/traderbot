from enum import Enum

import requests

from config.Config import Config
from GDAXAuth import GDAXAuth
from GDAXCryptoCurrency import GDAXCryptoCurrency


class TickerFields(Enum):
    TRADE_ID = 'trade_id'
    VOLUME = 'volume'
    PRICE = 'price'
    ASK = 'ask'
    BID = 'bid'
    TIME = 'time'
    SIZE = 'size'


class AccountFields(Enum):
    HOLD = 'hold'
    ID = 'id'
    PROFILE_ID = 'profile_id'
    CURRENCY = 'currency'
    BALANCE = 'balance'
    AVAILABLE = 'available'


class JsonParser:

    def __init__(self):
        self.config = Config()

    def getCurrencyCode(self, mainConfig):
        currency = ''
        if mainConfig.currency == GDAXCryptoCurrency.BTC_USD:
            currency = 'BTC'
        elif mainConfig.currency == GDAXCryptoCurrency.ETH_USD:
            currency = 'ETH'
        elif mainConfig.currency == GDAXCryptoCurrency.LTC_USD:
            currency = 'LTC'
        elif mainConfig.currency == GDAXCryptoCurrency.BCH_USD:
            currency = 'BCH'

        else:
            print("Error unknown Currency Type")
            exit()
            # TODO Error and say why in the log file

        return currency

    def parseCryptoCurrencyPrice(self, json):
        try:
            return json[TickerFields.PRICE.value]
        except:
            if 'Rate limit' in json['message']:
                print("Rate Limit Exceeded")
            return None

    # Returns the boolean of whether we have any of our selected currency purchased or not
    def parseAvailableSelectedCurrency(self, jsonList, mainConfig):

        currency = self.getCurrencyCode(mainConfig)

        index = -1
        for i in range(len(jsonList) - 1):
            if jsonList[i][AccountFields.CURRENCY.value] == currency:
                index = i

        return 0 < float(jsonList[index][AccountFields.HOLD.value])

    def parseHoldingAmountSelectedCurrency(self, jsonList, mainConfig):
        currency = self.getCurrencyCode(mainConfig)
        index = -1
        for i in range(len(jsonList)):
            if jsonList[i][AccountFields.CURRENCY.value] == currency:
                index = i

        if index == -1:
            print('Error parsing Holding amount selected Currency')
            return -1

        return round(float(jsonList[index][AccountFields.BALANCE.value]), 8)

    def parseUsdBalance(self, jsonList):

        currency = 'USD'
        index = -1
        for i in range(len(jsonList) - 1):
            if jsonList[i][AccountFields.CURRENCY.value] == currency:
                index = i

        return float(jsonList[index][AccountFields.AVAILABLE.value])


