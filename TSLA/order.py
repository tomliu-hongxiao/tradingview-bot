from ibapi.order import *


def market_order(action, quantity):
    order = Order()
    order.action = action
    order.orderType = "MKT"
    order.totalQuantity = quantity
    return order


def stop_order(quantity):
    order = Order()
    order.orderType = "STP"
    order.action = "SELL"
    order.totalQuantity = quantity
    return order


def mid_price_order(action, quantity):
    order = Order()
    order.action = action
    order.orderType = "MIDPRICE"
    order.totalQuantity = quantity
    return order
