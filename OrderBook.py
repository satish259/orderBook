# coding=utf-8
from Order import Order
from Utils.constants import orderKeysAdd, orderKeys, BuySell
from Utils.errors import customValueError
from Utils.db import dbORDERS, addOrder, cancelOrder


class OrderBook(object):

    def __init__(self):
        self.orders = {}
        self.bidPrices = {}
        self.askPrices = {}
        self.db=dbORDERS()

    def _addOrder(self, order):
        """
        Adds order to orderBook (orders dict)
        """
        self.orders[order.orderId] = order
        self._safeAddPrice(self._identifyPriceDictionary(order.side), order.ticker, order.price)
        addOrder(self.db,order)

    def _cancelOrder(self, order):
        """
        Remove order from orderBook (orders dict)
        """
        if order:
            if order.orderId in self.orders:
                self._safeRemovePrice(self._identifyPriceDictionary(order.side), order.ticker, order.price)
                self.orders.pop(order.orderId)
                cancelOrder(self.db, order)
            else:  # If order does not exists. One could consider ignoring it.
                customValueError('orderId', order.orderId, "Unable to cancel order as it does not exist.")
        else:  # If order does not exists. One could consider ignoring it.
            customValueError('orderId', 'None', "Unable to cancel order as it does not exist.")

    def _identifyPriceDictionary(self, side):
        """
        Simple check on side to identify the dictionary to update with price
        """
        if side == 'B':
            return self.bidPrices
        else:
            return self.askPrices

    def _safeAddPrice(self, priceDictonary, ticker, price):
        """
        Add a new price to the ticker list to enable faster return for best bid/ask
        """
        tickerList = priceDictonary.get(ticker, [])
        tickerList.append(price)
        priceDictonary[ticker] = tickerList

    def _safeRemovePrice(self, priceDictonary, ticker, price):
        """
        Remove price to the ticker list for cancelled trade
        """
        if ticker in priceDictonary:
            tickerList = priceDictonary[ticker]
            if price in tickerList:
                tickerList.remove(price)

    def maxBid(self, ticker):
        """
        Max Bid price as best to sell to them.
        """
        return str(max(self.bidPrices.get(ticker, []), default=0.0))

    def minAsk(self, ticker):
        """
        Min Ask price as best to buy from them.
        """
        return str(min(self.askPrices.get(ticker, []), default=0.0))

    def _updateOrder(self, lOrder):
        """
        Identifies field based on B/S, alpha, numeric or decimal.
        Processes update as a cancel followed by a new order.
        """
        dictOrderUpdate = dict(zip(orderKeys, lOrder[:len(orderKeys)]))
        # The unpolished code is to allow update of most fields
        if len(lOrder) > len(orderKeys) - 1:  # If there are any fields to update
            for n in lOrder[len(orderKeys):]:
                if n in BuySell:  # If it is B/S, it is a side.
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
                self._cancelOrder(orgOrder)  # Cancel original order
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
            self._cancelOrder(self.orders.get(dictOrder['orderId'], None))
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
