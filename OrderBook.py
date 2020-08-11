# coding=utf-8

from Order import Order
from Utils.constants import orderKeysAdd, orderKeys
from Utils.errors import customValueError


class OrderBook(object):

    def __init__(self):
        self.orders = {}

    def _addOrder(self, order):
        """
        Adds order to orderBook (orders dict)
        """
        self.orders[order.orderId] = order

    def _cancelOrder(self, orderId):
        """
        Remove order from orderBook (orders dict)
        """
        if orderId in self.orders:
            self.orders.pop(orderId)
        else:  # If order does not exists. One could consider ignoring it.
            customValueError('orderId', orderId, "Unable to cancel order as it does not exist.")

    def maxBid(self, ticker):
        """
        Max Bid price as best to sell to them.
        """
        bidPrice = []
        for order in self.orders.values():
            if order.ticker == ticker and order.side == 'B':
                bidPrice.append(order.price)
        return str(max(bidPrice,default=0.0))

    def minAsk(self, ticker):
        """
        Min Ask price as best to buy from them.
        """
        askPrice = []
        for order in self.orders.values():
            if order.ticker == ticker and order.side == 'S':
                askPrice.append(order.price)
        return str(min(askPrice,default=0.0))

    def _updateOrder(self, lOrder):
        """
        Identifies field based on B/S, alpha, numeric or decimal.
        Processes update as a cancel followed by a new order.
        """
        dictOrderUpdate = dict(zip(orderKeys, lOrder[:len(orderKeys)]))
        # The unpolished code is to allow update of most fields
        if len(lOrder) > len(orderKeys) - 1:  # If there are any fields to update
            for n in lOrder[len(orderKeys):]:
                if n in ['B', 'S']:  # If it is B/S, it is a side.
                    dictOrderUpdate['side'] = n
                elif n.isalpha():  # If it is alpha, it is a ticker.
                    dictOrderUpdate['ticker'] = n
                elif n.isdigit():  # If it is a int, it is a quantity.
                    dictOrderUpdate['quantity'] = n
                else:  # Else a price.
                    dictOrderUpdate['price'] = n
            if dictOrderUpdate['orderId'] in self.orders:  # If order exists
                orgOrder = self.orders[dictOrderUpdate['orderId']]  # fetch original order
                # Generate new order based based original order and updates
                order = Order(dictOrderUpdate['timestamp'], dictOrderUpdate['orderId'],
                              dictOrderUpdate.get('ticker', None), dictOrderUpdate.get('side', None),
                              dictOrderUpdate.get('price', None), dictOrderUpdate.get('quantity', None), orgOrder)
                self._cancelOrder(dictOrderUpdate['orderId'])  # Cancel original order
                self._addOrder(order)  # Add new order
            else:  # If order does not exists
                customValueError('orderId', dictOrderUpdate['orderId'], "Unable to amend order as it does not exist.")

    def processOrder(self, data):
        """
        Processes orders based on action
        """
        dictOrder = dict(zip(orderKeys, data.split('|')))
        if dictOrder['action'] == 'a':
            dictOrderAdd = dict(zip(orderKeysAdd, data.split('|')))
            order = Order(dictOrderAdd['timestamp'], dictOrderAdd['orderId'], dictOrderAdd['ticker'],
                          dictOrderAdd['side'], dictOrderAdd['price'], dictOrderAdd['quantity'])
            self._addOrder(order)
        elif dictOrder['action'] == 'c':
            self._cancelOrder(dictOrder['orderId'])
        elif dictOrder['action'] == 'u':
            self._updateOrder(data.split('|'))
        else:
            customValueError('action', dictOrder['action'], "a, u and c are the allowable actions.")


def processOrder(orderbook, order):
    """
    Public function to process order to orderbook.
    """
    orderbook.processOrder(order)


def getBestBidAndAsk(orderbook, ticker):
    """
    Public function fetch and return string of bid and ask price.
    """
    return '/'.join([orderbook.maxBid(ticker), orderbook.minAsk(ticker)])
