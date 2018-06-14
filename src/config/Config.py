import os

# TODO make exchange / currency modular
from GDAXCryptoCurrency import GDAXCryptoCurrency

def ReadInFile():
    ## Open the file with read only permit
    f = open(os.path.dirname(os.path.abspath(__file__)) + "\\config.conf", "r")

    ## use readlines to read all lines in the file
    ## The variable "lines" is a list containing all lines
    lines = f.read().splitlines()

    ## close the file after reading the lines.
    f.close()

    return lines

def GetConfigItem(config_list, item_key):

    for item in config_list:
        if item_key in item:
            return item.split(' ')[1]

    # Error not found
    print("Error Config item: ", item_key, "  not found")
    exit(1)

class Config:
    def __init__(self):
        self.file_lines = ReadInFile()

        # Connection Info
        self.api_key = str(GetConfigItem(self.file_lines, "api_key"))
        self.secret_key = str(GetConfigItem(self.file_lines, "secret_key"))
        self.pass_phrase = str(GetConfigItem(self.file_lines, "pass_phrase"))

        self.database_location = str(GetConfigItem(self.file_lines, "database_location"))


        # Misc
        self.span_divider = int(GetConfigItem(self.file_lines, "span_divider"))
        self.order_rate = int(GetConfigItem(self.file_lines, "order_rate"))

        self.currency = None

        for coin in GDAXCryptoCurrency:
            if coin.value[0] == str(GetConfigItem(self.file_lines, "currency")):
                self.currency = coin

        if self.currency is None:
            print("Currency Could not be read in")
            exit(1)


        # URL
        self.ticker_end_url = '/products/' + self.currency.value[0] + '/ticker'
        self.gdax_api_url = str(GetConfigItem(self.file_lines, "gdax_api_url"))

        # Database options
        self.delay = int(GetConfigItem(self.file_lines, "delay"))
        self.ema_time_frame = int(GetConfigItem(self.file_lines, "ema_time_frame"))

