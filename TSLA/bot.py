import datetime
import threading
import time


from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import *


from order import *
from database import DataBase


class Bot(EClient, EWrapper):
    def __init__(self, symbol):
        EClient.__init__(self, self)

        # **********    交易机器人 基础数据    ***********#
        self.db = DataBase('cred.json')

        self.symbol = symbol

        self.order_id = None
        self.place_quantity = None
        self.hold_position = None
        self.prev_order_action = None
        self.prev_order_time = None
        self.cur_order_action = None
        self.cur_order_time = None

        self.has_order = False

        # *******************************************#

        # *************    连接 TWS     ***************#
        self.lock = threading.Lock()
        self.connect("127.0.0.1", 7497, 1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)

        self.run_trading_view()

        # *******************************************#

    def init_bot(self):
        api_respond = self.db.get_signal()
        if api_respond is not None:
            self.prev_order_action = api_respond['order_action']
            self.hold_position = api_respond['order_position']
            self.prev_order_time = api_respond['time']

    def run_trading_view(self):
        while True:
            self.lock.acquire()
            api_respond = self.db.get_signal()
            self.lock.release()

            if api_respond is not None and api_respond['time'] % 5 == 0:
                self.lock.acquire()
                self.cur_order_action = api_respond['order_action']
                self.place_quantity = api_respond['order_position']
                self.cur_order_time = api_respond['time']

                # 当前没有单  进单
                if self.cur_order_time != self.prev_order_time and not self.has_order:
                    self.perform_order(self.place_quantity)
                    self.prev_order_action = self.cur_order_action
                    self.hold_position = self.place_quantity
                    self.prev_order_time = self.cur_order_time
                    self.has_order = True

                # 当前有单  出单
                elif self.cur_order_time != self.prev_order_time and self.has_order:
                    self.perform_order(self.hold_position)
                    self.prev_order_action = self.cur_order_action
                    self.hold_position = self.place_quantity
                    self.prev_order_time = self.cur_order_time
                    self.has_order = False
                self.lock.release()

                second = int(str(datetime.datetime.now().time())[6:8])
                minute = int(str(datetime.datetime.now().time())[3:5])
                sec = (4 - (minute % 5)) * 60 + (65 - second)
                time.sleep(sec)
            else:
                second = int(str(datetime.datetime.now().time())[6:8])
                minute = int(str(datetime.datetime.now().time())[3:5])
                sec = (4 - (minute % 5)) * 60 + (65 - second)
                time.sleep(sec)

    def perform_order(self, quantity):
        if self.cur_order_action == 'sell':
            self.place_sell_order(quantity)
        elif self.cur_order_action == 'buy':
            self.place_buy_order(quantity)

    def place_market_order(self, action, quantity):
        self.placeOrder(self.order_id, self.tsla_contract(), mid_price_order(action, quantity))

    def place_sell_order(self, quantity):
        self.place_market_order("SELL", quantity)
        self.order_id += 1

    def place_buy_order(self, quantity):
        self.place_market_order("BUY", quantity)
        self.order_id += 1

    def run_loop(self):
        try:
            self.run()
        except Exception as e:
            print(e)

    # Get next order id we can use
    def nextValidId(self, nextOrderId):
        self.order_id = nextOrderId

    def error(self, id, errorCode, errorMsg):
        print(errorCode)
        print(errorMsg)

    def tsla_contract():
        contract = Contract()
        contract.symbol = "TSLA"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        return contract