from queue import Queue

import time

from config.Config import Config
from database.Database import CryptoDatabase

import pandas as pd
import matplotlib.pyplot as plt

class EMAtracker:

    def __init__(self):
        # pull from database
        print("Initializing Exponential Moving Average tracker...")

        # Basic Queue carries unweighted price data

        self.mainConfig = Config()
        self.database = CryptoDatabase()

    def to_number(self, df):
        try:
            s1 = float(df)
            return s1
        except ValueError:
            return df

    def getFromDatabase(self):
        try:
            tupleList = self.database.getEmaData()
            floatList = [float(i[0]) for i in tupleList]
            return floatList
        except:
            return None

    def getEMA(self):
        try:
            average = pd.DataFrame(self.getFromDatabase())
            average = pd.Series.ewm(average, span=(len(average) / self.mainConfig.span_divider)).mean()
            # print(average)
            average = average[0]
            return average

        except:
            return None


    def getAvgPosVariance(self):
        try:
            floatList = self.getFromDatabase()
            fwd = self.getEMA()
            aboveAvg = 0
            for i in range(0, len(floatList)):
                if floatList[i] > fwd[i]:
                    aboveAvg += (floatList[i] - fwd[i])
                    aboveAvg /= 2
            return aboveAvg
        except:
            return aboveAvg

    def getAvgNegVariance(self):
        try:
            floatList = self.getFromDatabase()
            fwd = self.getEMA()
            belowAvg = 0
            for i in range(0, len(floatList)):
                if floatList[i] < fwd[i]:
                    belowAvg += (fwd[i] - floatList[i])
                    belowAvg /= 2
            return belowAvg
        except:
            return belowAvg


# tracker = EMAtracker()
# ema = tracker.getEMA()
#
# print("Positive Variance:")
# print(tracker.getAvgPosVariance())
# print("Negative Variance:")
# print(tracker.getAvgNegVariance())
#
# try:
#     plt.plot(tracker.getFromDatabase(), color='orange')
#     plt.plot(ema, color='red')
#     plt.show()
# except:
#     print("Not Enough Data")


