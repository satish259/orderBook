import unittest
from orderBook import OrderBook, processOrder, getBestBidAndAsk

class TestOrders(unittest.TestCase):

    def test_oneOrder(self):
        out=[]
        o=OrderBook()
        orders=['1568390243|abbb11|a|AAPL|B|209.00000|100', '1568390244|abbb11|u|101', '1568390245|abbb11|c']
        for order in orders:
            processOrder(o,order)
            out.append(getBestBidAndAsk(o,'AAPL'))
        self.assertEqual(out, ['AAPL: Best Bid 209.0 - Best Ask 0.', 'AAPL: Best Bid 209.0 - Best Ask 0.', 'AAPL: Best Bid 0 - Best Ask 0.'])

    def test_twoOrder(self):
        out=[]
        o=OrderBook()
        orders=['1568390201|abbb11|a|AAPL|B|209.00000|100', '1568390202|abbb12|a|AAPL|S|210.00000|10', '1568390204|abbb11|u|10', '1568390203|abbb12|u|101','1568390243|abbb11|c']
        for order in orders:
            processOrder(o,order)
            out.append(getBestBidAndAsk(o,'AAPL'))
        self.assertEqual(out, ['AAPL: Best Bid 209.0 - Best Ask 0.', 'AAPL: Best Bid 209.0 - Best Ask 210.0.', 'AAPL: Best Bid 209.0 - Best Ask 210.0.','AAPL: Best Bid 209.0 - Best Ask 210.0.','AAPL: Best Bid 0 - Best Ask 210.0.'])

    def test_incorrectAction(self):
        # Test againt incorrect action k
        o=OrderBook()
        with self.assertRaises(ValueError):
            processOrder(o,'1568390243|abbb11|k')

    def test_incorrectQuantity(self):
        # Test againt incorrect quantity ?
        o=OrderBook()
        with self.assertRaises(ValueError):
            processOrder(o,'1568390201|abbb11|a|AAPL|B|209.00000|?')

    def test_incorrectPrice(self):
        # Test againt incorrect price f
        o=OrderBook()
        with self.assertRaises(ValueError):
            processOrder(o,'1568390201|abbb11|a|AAPL|B|f|1')

    def test_incorrectSide(self):
        # Test againt incorrect side L
        o=OrderBook()
        with self.assertRaises(ValueError):
            processOrder(o,'1568390201|abbb11|a|AAPL|L|209.00000|100')

if __name__ == '__main__':
    unittest.main()
