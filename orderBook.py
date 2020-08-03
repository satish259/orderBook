import six

orderKeys= ['timestamp', 'orderId', 'action'] # mimimum required order fields to handle cancel and update
orderKeysA= ['timestamp', 'orderId', 'action', 'ticker', 'side','price','quantity'] # Fields for an new order


class OrderBook(object):

    def __init__(self):
        self._orderHistory=[] # list of orders history
        self._activeOrders={} # dictonary of active orders
        self._bidPrices={}
        self._bidQuantity={}
        self._bidOrders={}
        self._askPrices={}
        self._askQuantity={}
        self._askOrders={}

    def _remove(self, dOrder):
        '''
        Removes price, quantity and order from cancelled order from list.
        '''
        if dOrder['side'] == 'B':
            price=self._bidPrices
            quantity=self._bidQuantity
            order=self._bidOrders
        else:
            price=self._askPrices
            quantity=self._askQuantity
            order=self._askOrders
        # Remove Price
        d=price.get(dOrder['ticker'])
        if d and float(dOrder['price']) in d:
            d.remove(float(dOrder['price']))
            if d:
                price[dOrder['ticker']]=d
            else:
                del price[dOrder['ticker']]
        # Remove Order
        d=order.get(dOrder['ticker'],{})
        if d and (dOrder['price'],dOrder['quantity']) in d:
            d1=d[(dOrder['price'],dOrder['quantity'])]
            d1.remove(dOrder['orderId'])
            if d1:
                d[(dOrder['price'],dOrder['quantity'])]=d1
                order[dOrder['ticker']]=d
            else:
                del d[(dOrder['price'],dOrder['quantity'])]
                if not order.get(dOrder['ticker'],{}): del order[dOrder['ticker']]
        # Remove Quantity
        quantity[dOrder['ticker']]=max(quantity.get(dOrder['ticker'],0) - int(dOrder['quantity']),0)

    def _add(self, dOrder):
        '''
        Add price, quantity and order for new order to list.
        '''
        if dOrder['side'] == 'B':
            price=self._bidPrices
            quantity=self._bidQuantity
            order=self._bidOrders
        else:
            price=self._askPrices
            quantity=self._askQuantity
            order=self._askOrders
        # Add Price
        d=price.get(dOrder['ticker'],[])
        d.append(float(dOrder['price']))
        price[dOrder['ticker']]=d
        # Add Order
        d=order.get(dOrder['ticker'],{})
        d1=d.get((dOrder['price'],dOrder['quantity']),[])
        d1.append(dOrder['orderId'])
        d[(dOrder['price'],dOrder['quantity'])]=d1
        order[dOrder['ticker']]=d
        # Add Quantity
        quantity[dOrder['ticker']]=quantity.get(dOrder['ticker'],0) + int(dOrder['quantity'])

    def _addOrder(self, dOrder):
        '''
        Insert a new order to order book history and add prices.
        '''
        self._activeOrders[dOrder['orderId']]=dOrder
        self._add(dOrder) #add price from bid/ask dictonary


    def _cancelOrder(self, dOrder):
        '''
        Cancel an order from order book history and remove price.
        '''
        if dOrder['orderId'] in self._activeOrders: # if trade exists
            self._remove(self._activeOrders[dOrder['orderId']]) #remove price from bid/ask dictonary
            del self._activeOrders[dOrder['orderId']]
        else: #possible alternative it to ignore the order
            raise ValueError('Unable find trade ID ' + dOrder['orderId'])

    def _updateOrder(self, dOrder):
        '''
        update an order to order book history, update active order and price.
        '''
        if dOrder['orderId'] in self._activeOrders: # if trade exists
            newOrder=dict(self._activeOrders[dOrder['orderId']], **dOrder)
            self._cancelOrder(dOrder) #cancel old order
            self._addOrder(newOrder) #add new order
        else: # possible anternative is to add a new trade instead
            raise ValueError('Unable find trade ID ' + dOrder['orderId'])

    def _validate(self, dOrder):
        '''
        Validate all fields of Order are valid.
        '''
        valid=True
        for k, v in six.iteritems(dOrder):
            if k == 'side' and v not in ['B','S']:
                self._valueError(k,v)
            elif k == 'action' and v not in ['a','u','c']:
                self._valueError(k,v)
            elif k=='price' and (float(v)<0 or '.' not in v):
                self._valueError(k,v)
            elif k in ['quantity','timestamp']  and (int(v)<0 or '.'  in v):
                valid=False
        return valid

    def _formatAdd(self, lOrder):
        '''
        Formats add instructions and validates resulting dictonary.
        All columns are required.
        '''
        d= dict(zip(orderKeysA, lOrder))
        if self._validate(d):
            return d
        else:
            return None

    def _formatCancel(self, lOrder):
        '''
        Formats cancel instructions and validates resulting dictonary.
        Just 3 fields are required and all others are ignored.
        '''
        d= dict(zip(orderKeys, lOrder))
        if self._validate(d):
            return d
        else:
            return None

    def _formatUpdate(self, lOrder):
        '''
        Formats update instructions and validates resulting dictonary.
        Identifies field based on B/S, alpha, numeric or decimal.
        '''
        d= dict(zip(orderKeys, lOrder[:len(orderKeys)]))
        if len(lOrder)>len(orderKeys)-1:
            for n in lOrder[len(orderKeys):]:
                if n in ['B','S']:
                    d['side']=n
                elif n.isalpha():
                    d['ticker']=n
                elif n.isdigit():
                    d['quantity']=n
                else:
                    d['price']=n
        if self._validate(d):
            return d
        else:
            return None

    def _valueError(self, k, v):
        '''
        Simple value error for key, value pairs from order.
        '''
        raise ValueError('Incorrect {} with value {}'.format(k,v))

    def _maxBid(self, ticker):
        '''
        Max Bid price as best to sell to them.
        '''
        return  max(self._bidPrices.get(ticker,[0]))

    def _minAsk(self, ticker):
        '''
        Min Ask price as best to buy from them.
        '''
        return min(self._askPrices.get(ticker,[0]))

    def processOrder(self, order):
        '''
        Splits incomming order and passed it to be processed based on action.
        '''
        lOrder=order.split('|')
        if lOrder[2]=='a':
            dOrder=self._formatAdd(lOrder)
            self._orderHistory.append(dOrder)
            self._addOrder(dOrder)
        elif lOrder[2]=='u':
            dOrder=self._formatUpdate(lOrder)
            self._orderHistory.append(dOrder)
            self._updateOrder(dOrder)
        elif lOrder[2]=='c':
            dOrder=self._formatCancel(lOrder)
            self._orderHistory.append(dOrder)
            self._cancelOrder(dOrder)
        else:
            raise ValueError('Incorrect action ' + lOrder[2])

    def bestBidAndAsk(self, ticker):
        return '{}: Best Bid {} - Best Ask {}.'.format(ticker,self._maxBid(ticker), self._minAsk(ticker))

def processOrder(orderbook, order):
    '''
    Public function to process order to orderbook.
    '''
    orderbook.processOrder(order)

def getBestBidAndAsk(orderbook, ticker):
    '''
    Public function fetch and return string of bid and ask price.
    '''
    return orderbook.bestBidAndAsk(ticker)