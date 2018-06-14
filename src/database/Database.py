import time
import sqlite3
import os
import csv


# TODO make a private class that executes sql and only function inside the class can access it but they all use it
import GDAXCryptoCurrency
from config.Config import Config


class CryptoDatabase:
    def __init__(self):
        self.config = Config()
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_filename = os.path.join(self.config.database_location)
        self.schema_filename = os.path.join(self.ROOT_DIR, 'cryptoAlchemist_schema.sql')
        self.createDatabase()

    def createDatabase(self):
        with sqlite3.connect(self.db_filename) as conn:
            with open(self.schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)
            sqlite3.enable_shared_cache(True)

    def insertHistoryEntry(self, insert_time, exchange_name, currency_name, price, size, bid, ask, volume):
        with sqlite3.connect(self.db_filename) as conn:
            conn.execute(
                "insert into history (insert_time, exchange_name, currency_name, price, size, bid, ask, volume) values (" +
                    str(insert_time) + ", \'" + str(exchange_name) + "\', \'" + str(currency_name) + "\', " +
                    str(price) + ", " + str(size) + ", " + str(bid) + ", " + str(ask) + ", " + str(volume) +
                ")"
            )

    def insertOrderBookEntry(self, insert_time, exchange_name, currency_name, bid1_price, bid2_price, bid3_price, bid4_price, bid5_price, ask1_price, ask2_price, ask3_price, ask4_price, ask5_price, bid1_size, bid2_size, bid3_size, bid4_size, bid5_size, ask1_size, ask2_size, ask3_size, ask4_size, ask5_size, bid1_num_orders, bid2_num_orders, bid3_num_orders, bid4_num_orders, bid5_num_orders, ask1_num_orders, ask2_num_orders, ask3_num_orders, ask4_num_orders, ask5_num_orders):
        with sqlite3.connect(self.db_filename) as conn:
            conn.execute(
                "insert into order_book_summary (insert_time, exchange_name, currency_name, bid1_price , bid2_price, " +
                "bid3_price, bid4_price, bid5_price, ask1_price, ask2_price, ask3_price, ask4_price, ask5_price, " +
                "bid1_size, bid2_size, bid3_size, bid4_size, bid5_size, ask1_size, ask2_size, ask3_size, ask4_size, " +
                "ask5_size, bid1_num_orders, bid2_num_orders, bid3_num_orders, bid4_num_orders, bid5_num_orders, " +
                "ask1_num_orders, ask2_num_orders, ask3_num_orders, ask4_num_orders, ask5_num_orders) values (" +
                    str(insert_time) + ", \'" + str(exchange_name) + "\', \'" + str(currency_name) + "\', " +
                    str(bid1_price) + ", " + str(bid2_price) + ", " + str(bid3_price) + ", " + str(bid4_price) + ", " + str(bid5_price) + ", " +
                    str(ask1_price) + ", " + str(ask2_price) + ", " + str(ask3_price) + ", " + str(ask4_price) + ", " + str(ask5_price) + ", " +

                    str(bid1_size) + ", " + str(bid2_size) + ", " + str(bid3_size) + ", " + str(bid4_size) + ", " + str(bid5_size) + ", " +
                    str(ask1_size) + ", " + str(ask2_size) + ", " + str(ask3_size) + ", " + str(ask4_size) + ", " + str(ask5_size) + ", " +

                    str(bid1_num_orders) + ", " + str(bid2_num_orders) + ", " + str(bid3_num_orders) + ", " + str(bid4_num_orders) + ", " + str(bid5_num_orders) + ", " +
                    str(ask1_num_orders) + ", " + str(ask2_num_orders) + ", " + str(ask3_num_orders) + ", " + str(ask4_num_orders) + ", " + str(ask5_num_orders) +
                ")"
            )

    def insertBuyHistoryEntry(self, insert_time, exchange_name, currency_name, buy_price):
        with sqlite3.connect(self.db_filename) as conn:
            conn.execute(
                "insert into buy_history (insert_time, exchange_name, currency_name, buy_price) values (" +
                    str(insert_time) + ", \'" + str(exchange_name) + "\', \'" + str(currency_name) + "\', " +
                    str(buy_price) +
                ")"
            )

    def selectNewestHistory(self, exchange, currency, returnCount):

        with sqlite3.connect(self.db_filename) as conn:

            # Check for nulls # TODO if more than a certain percent are nulls then return a fail

            cursor = conn.cursor()

            cursor.execute(
                "SELECT * from history " +
                "WHERE exchange_name = \'" + exchange + "\' " +
                "AND currency_name = \'" + currency.value[0] + "\' " +

                "ORDER BY insert_time DESC "
                "LIMIT " + str(returnCount)
            )

            # TODO before return check if the return size is correct (ie: there are enough entries in the database)

            result = cursor.fetchall()

            if len(result) != returnCount:
                print("Not enough entries in the database yet. Currently: " + str(len(result)))
                return -1

            return result

    def selectAllColumnOrderBook(self, endTime, exchange, currency):

        with sqlite3.connect(self.db_filename) as conn:
            # Check for nulls # TODO if more than a certain percent are nulls then return a fail

            cursor = conn.cursor()

            cursor.execute(
                "SELECT insert_time, exchange_name, currency_name, bid1_price, bid2_price, bid3_price, bid4_price, bid5_price, ask1_price, ask2_price, ask3_price, ask4_price, ask5_price, bid1_size, bid2_size, bid3_size, bid4_size, bid5_size, ask1_size, ask2_size, ask3_size, ask4_size, ask5_size, bid1_num_orders, bid2_num_orders, bid3_num_orders, bid4_num_orders, bid5_num_orders, ask1_num_orders, ask2_num_orders, ask3_num_orders, ask4_num_orders, ask5_num_orders " +
                "FROM order_book_summary " +
                "where insert_time >= " + str(endTime) + " and insert_time <= " + str(int(round(time.time() * 1000))) + " " +
                "and exchange_name = \'" + exchange + "\' " +
                "and currency_name = \'" + currency.value[0] + "\' " +
                "ORDER BY insert_time DESC"
            )

            result = cursor.fetchall()

            return result

    def resultToCsv(self, filename, data, header):
        with open(filename, "w", newline="\n", encoding="utf-8") as out:

            # TODO check header same length as the result

            csv_out = csv.writer(out)
            csv_out.writerow(header)

            for row in data:
                csv_out.writerow(row)

    def getEmaData(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT price " +
                "FROM history " +
                "WHERE currency_name = \'" + self.config.currency.value[0] + "\' AND " +
                "insert_time > \'" + str((time.time() * 1000) - (self.config.ema_time_frame * 60 * 60 * 1000)) + "\' " +
                "ORDER BY insert_time DESC"
            )

            result = cursor.fetchall()

            #print("Size: ", len(result))
            #print("Expected Size: ", (self.config.EMATimeFrame * 60 * 60) / self.config.delay)
            #print(len(result) / ((self.config.EMATimeFrame * 60 * 60) / self.config.delay))

            # Check to make sure that there is enough data returned to make sure there aren't too many gaps
            if not len(result) / ((self.config.ema_time_frame * 60 * 60) / self.config.delay) > 0.75:
                print("Not Enough Data")
                print("%", 100 * (len(result) / ((self.config.ema_time_frame * 60 * 60) / self.config.delay)))
                return None

            # Reverse the list before sending back
            return result                   #[::-1]

    def getLastBoughtPrice(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT buy_price " +
                "FROM buy_history " +
                "WHERE currency_name = \'" + self.config.currency.value[0] + "\' " +
                "ORDER BY insert_time DESC "
                "LIMIT 1"
            )

            result = cursor.fetchall()

            return (result[0][0])

##########  Testing area ##########
#database = CryptoDatabase()

#database.insertBuyHistoryEntry(int(time.time() * 1000), "GDAX", GDAXCryptoCurrency.GDAXCryptoCurrency.BCH_USD.value[0], 3089.68)


#result = database.getLastBoughtPrice()



#result = database.selectNewestHistory("GDAX", GDAXCryptoCurrency.GDAXCryptoCurrency.BCH_USD, 100000)

#for i in result:
#print(result)

#print(type(result[0]))


#result = database.selectNewestHistory("GDAX", GDAXCryptoCurrency.BTC_USD, 100000)

#database.resultToCsv('result.csv', result, ['insert_time', 'exchange_name', 'currency_name', 'price', 'size', 'bid', 'ask', 'volume'])

#database.resultToCsv('result.csv', result, ['insert_time', 'exchange_name', 'currency_name', 'bid1_price', 'bid2_price', 'bid3_price', 'bid4_price', 'bid5_price', 'ask1_price', 'ask2_price', 'ask3_price', 'ask4_price', 'ask5_price', 'bid1_size', 'bid2_size', 'bid3_size', 'bid4_size', 'bid5_size', 'ask1_size', 'ask2_size', 'ask3_size', 'ask4_size', 'ask5_size', 'bid1_num_orders', 'bid2_num_orders', 'bid3_num_orders', 'bid4_num_orders', 'bid5_num_orders', 'ask1_num_orders', 'ask2_num_orders', 'ask3_num_orders', 'ask4_num_orders', 'ask5_num_orders'])



























'''
database.insertHistoryEntry(int(round(time.time() * 1000)), 'Poloniex', 'LTC-USD', 65.23)
database.insertHistoryEntry(int(round(time.time() * 1000)), 'Poloniex', 'LTC-USD', 65.23)

# Get all tables
database.printSqlResults("""
        SELECT name FROM sqlite_master WHERE type='table';
    """)
    
print()

# Describe Table
database.printSqlResults("""
        PRAGMA table_info(history);
    """)'''