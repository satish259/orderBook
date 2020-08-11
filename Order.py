# coding=utf-8
from Utils.constants import BuySell
from Utils.errors import customValueError


class Order(object):
    """
    Orders represent the core piece of the instruction. Every bid/ask is an Order.
    Notes: orgOrder is used for updating orders. A new order with orgOrder values if missing are provided.
    """

    def __init__(self, timestamp, orderId, ticker=None, side=None, price=None, quantity=None, orgOrder=None):
        self.timestamp = timestamp
        self.orderId = orderId
        self.ticker = ticker or orgOrder.ticker
        self.side = side or orgOrder.side
        self.price = price or orgOrder.price
        self.quantity = quantity or orgOrder.quantity

    @property
    def side(self):
        """
        Fetch side attribute of order
        """
        return self._side

    @side.setter
    def side(self, value):
        """
        Set side attribute of order. Can be B for Buy or S for Sell only.
        """
        if value in BuySell:
            self._side = value
        else:
            customValueError('side', value, 'B for Buy or S for Sell are the allowable values.')

    @property
    def price(self):
        """
        Fetch price attribute of order
        """
        return self._price

    @price.setter
    def price(self, value):
        """
        Set price attribute of order. Checks price is a float, positive, greater than zero (technicality) and of 5dp or
        fewer.
        """
        try:
            if float(value) > 0:
                if len(str(value).split('.')[1]) <= 5:
                    self._price = float(value)
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            customValueError('price', value, 'Price must be float, positive, of 5 decimal places or fewer ,'
                                             'and greater than zero.')

    @property
    def quantity(self):
        """
        Fetch quantity attribute of order
        """
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        """
        Set quantity attribute of order. Checks price is a float, positive and  greater than zero (technicality).
        """
        if int(value) > 0 and '.' not in str(value):
            self._quantity = int(value)
        else:
            customValueError('quantity', value, 'Quantity must be float, positive, a whole numeric and greater than '
                                                'zero.')

    def __str__(self):
        """
        Printable string representation of trade
        """
        return r'timestamp: {timestamp}, orderId: {orderId}, ticker: {ticker}, side: {side}, ' \
               'price: {price}, quantity: {quantity}'.format(timestamp=self.timestamp,
                                                             orderId=self.orderId,
                                                             ticker=self.ticker,
                                                             side=self.side, price=self.price, quantity=self.quantity)

    def __lt__(self, other):
        """
        Comparing prices of objects for sorting.
        Not used: proposed use for a list of orders for matching.
        """
        return self.price < other.price

    def __gt__(self, other):
        """
        Comparing prices of objects for sorting.
        Not used: propose used for a list of orders for matching.
        """
        return self.price > other.price
