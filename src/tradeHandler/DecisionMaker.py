import requests

from config.Config import Config
from JsonParser import JsonParser
from database.Database import CryptoDatabase
from tradeHandler.TradeHandler import TradeHandler


class DecisionMaker:

    def __init__(self):
        self.parser = JsonParser()
        self.database = CryptoDatabase()

    # TODO make into 4 methods [Done -TJ]


    def ifHolding(self, holdingBool, connection, mainConfig):
        try:
            r = requests.get(mainConfig.gdax_api_url + '/accounts', auth=connection)
        except:
            print("Error getting account info")
            return

        try:
            holdingBool = 0 < self.parser.parseHoldingAmountSelectedCurrency(r.json(), mainConfig)
        except:
            print('Error with jsonParser.parseAvailableSelectedCurrency()')
            return

        return holdingBool

    # Determine if Limit Set For Selected Crypto
    def ifOrderExists(self, limitSetBool, config, connection):
        try:
            r = requests.get(config.gdax_api_url + '/orders/', auth=connection)
        except:
            print("Error getting account info")
            return None

        try:
            if not r.json():
                limitSetBool = False
        except:
            limitSetBool = False

        return limitSetBool

    # Sell checks and stuff
    def sellLogic(self, emaTracker, connection, currentSelectedCryptoPrice, mainConfig):

        avgPosVariance = emaTracker.getAvgPosVariance()

        print("Avg Pos Variance: ", avgPosVariance)

        ema = emaTracker.getEMA()

        try:
            last_ema_val = ema[len(ema) - 1]
        except:
            print("Error with getting Ema")
            return

        trade_handler = TradeHandler(connection, Config())

        if avgPosVariance is not None:

            print("Last EMA Val: ", last_ema_val, '   ', "Current Price: ", currentSelectedCryptoPrice)
            # print("Step Value decisionMaker.sellLogic(): ", stepValue)
            print("Sell Val: ", last_ema_val + (avgPosVariance / mainConfig.order_rate))

            last_buy_price = self.database.getLastBoughtPrice()
            sell_price = last_buy_price + (avgPosVariance / mainConfig.order_rate)

            if sell_price < last_buy_price:
                sell_price = last_buy_price + .01
                print("Sell Price is currently being calculated below profitability.")
                print("Selling at 1 cent above bought price: ", sell_price)

            trade_handler.sell(sell_price)
            # stepValue += 1
            # print("Step Value decisionsMaker.sellLogic() 2:", stepValue)
            # return stepValue


    def buyLogic(self, emaTracker, connection, currentSelectedCryptoPrice, mainConfig):
        ################################################################################################################
        #################################### Buy #######################################################################
        # See if the conditions are right for a sell limit to be placed

        avgNegVariance = emaTracker.getAvgNegVariance()

        print("Avg Neg Variance: ", (avgNegVariance / mainConfig.order_rate))

        ema = emaTracker.getEMA()

        try:
            last_ema_val = ema[len(ema) - 1]
        except:
            print("Error with getting Ema")
            return

        print("Last EMA Val: ", last_ema_val, '   ', "Current Price: ", currentSelectedCryptoPrice)

        if avgNegVariance is not None:
            print("Min Buy Val: ", last_ema_val - avgNegVariance)

            # Altered buy logic to immediately set buy order
            # The Buy orders are all timed to elapse in 1 hour, with the amount needed scaling towards EMA
            buy_val = float(currentSelectedCryptoPrice) - float(avgNegVariance / mainConfig.order_rate)  # hard-coding offset
            tradeHandler = TradeHandler(connection, Config())
            tradeHandler.buy(buy_val)


    def makeDecision(self, currentSelectedCryptoPrice, mainConfig, api_url, connection, emaTracker):
        # Determine if holding Selected Crypto
        # print("Top of DecisionMaker stepVal: ", stepValue)
        holdingBool = None
        holdingBool = self.ifHolding(holdingBool, connection, mainConfig)
        print("Holding: ", holdingBool)

        # Determine if Limit Set For Selected Crypto
        limitSetBool = True
        limitSetBool = self.ifOrderExists(limitSetBool, mainConfig, connection)

        if limitSetBool is None:
            return

        print("Limit Extant: ", limitSetBool)

        # Checks for Sell stuff
        if holdingBool:
            if not limitSetBool:
                self.sellLogic(emaTracker, connection, currentSelectedCryptoPrice, mainConfig)

        # Checks for Buy stuff
        elif not holdingBool:
            if not limitSetBool:
                self.buyLogic(emaTracker, connection, currentSelectedCryptoPrice, mainConfig)
                # return 1    # resets stepValue

        # elif holdingBool:
        #     if limitSetBool:
        #         print("DecisionMaker.makeDecision() stepValue:", stepValue)
        #         return stepValue
        #
        # elif not holdingBool:
        #     if limitSetBool:
        #         print("Not holding, as currency is in order/escrow.")
        #         print("DecisionMaker.makeDecision() 2 stepValue:", stepValue)
        #         return stepValue
        # return 1

