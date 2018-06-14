import threading, time
import requests

from config.Config import Config
from GDAXCryptoCurrency import GDAXCryptoCurrency
from GDAXAuth import GDAXAuth
from database.Database import CryptoDatabase


class ExchangeThread(threading.Thread):

    def __init__(self, currency, connection, delay, config):
        threading.Thread.__init__(self)
        self.name = currency.value[0]
        self.delay = delay
        self.config = config
        self.api_url = currency.value[1]
        self.connection = connection
        self.exchange = currency.value[2]
        self.database = CryptoDatabase()

    def run(self):
        print("Starting: " + self.name)
        self.retrieveAndCommit(self.name, self.delay)
        print("Exiting: " + self.name)

    def collectTicker(self):
        r = requests.get(self.api_url + '/products/' + self.name + '/ticker', auth=self.connection)

        self.database.insertHistoryEntry(int(round(time.time() * 1000)), self.exchange, self.name, r.json()['price'],
                                         r.json()['size'], r.json()['bid'], r.json()['size'], r.json()['volume'])

        print(self.name, ":  ", r.json())

    def collectOrderBook(self):
        r = requests.get("https://api.gdax.com/products/" + self.name + "/book?level=2", auth=self.connection)

        # TODO make the group of 3 a class object for ease of moving around
        self.database.insertOrderBookEntry(int(round(time.time() * 1000)), self.exchange, self.name,
                   r.json()['bids'][0][0], r.json()['bids'][1][0], r.json()['bids'][2][0], r.json()['bids'][3][0], r.json()['bids'][4][0],
                   r.json()['asks'][0][0], r.json()['asks'][1][0], r.json()['asks'][2][0], r.json()['asks'][3][0], r.json()['asks'][4][0],

                   r.json()['bids'][0][1], r.json()['bids'][1][1], r.json()['bids'][2][1], r.json()['bids'][3][1], r.json()['bids'][4][1],
                   r.json()['asks'][0][1], r.json()['asks'][1][1], r.json()['asks'][2][1], r.json()['asks'][3][1], r.json()['asks'][4][1],

                   r.json()['bids'][0][2], r.json()['bids'][1][2], r.json()['bids'][2][2], r.json()['bids'][3][2], r.json()['bids'][4][2],
                   r.json()['asks'][0][2], r.json()['asks'][1][2], r.json()['asks'][2][2], r.json()['asks'][3][2], r.json()['asks'][4][2])

        print(self.name, ":  ", r.json()['bids'] + r.json()['asks'])

    def retrieveAndCommit(self, thread, delay):

        # Start Collection
        while True:
            try:
                self.collectTicker()
                #self.collectOrderBook()
                time.sleep(delay)

            except:
                print("Error Connecting: ", self.name)
                time.sleep(self.delay)
                continue

# TODO put in a file only for getting connections
def generateGDAXAuth(config):
    return GDAXAuth(config.api_key, config.secret_key, config.pass_phrase)


config = Config()

# Create thread lock and thread array
threadLock = threading.Lock()
threads = []

# Create new threads
offset = 2
for currency in GDAXCryptoCurrency:
    thread = ExchangeThread(currency, generateGDAXAuth(config), config.delay, config)
    time.sleep(offset)
    thread.start()
    threads.append(thread)


# Wait for all threads to complete
for t in threads:
    t.join()

print("Exiting Main Thread")
