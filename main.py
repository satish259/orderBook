# coding=utf-8
import logging
from OrderBook import OrderBook, processOrder, getBestBidAndAsk

logger = logging.getLogger(__name__)


def main():
    out = []
    ob = OrderBook()
    dataStream = ['1568390243|abbb11|a|AAPL|B|209.00000|100', '1568390244|abbb11|u|101', '1568390245|abbb11|c']
    for data in dataStream:
        processOrder(ob, data)
        out.append(getBestBidAndAsk(ob, 'AAPL'))

    assert out == ['209.0/0.0', '209.0/0.0', '0.0/0.0']
    # Explaination:
    #   When initial order with ID abbb11 is added, the price is the best Bid price as it is  the only order.
    #   The quantity of order ID abbb11 is amended in the next run, but the prices remain unchanged.
    #   Order ID abbb11 is cancelled, resulting in no order to traverse to calculate bid/ask price, hence  0.0/0.0.

    out = []
    orders = ['1568390201|abbb11|a|AAPL|B|209.00000|100', '1568390202|abbb12|a|AAPL|S|210.00000|10',
              '1568390204|abbb11|u|10', '1568390203|abbb12|u|101', '1568390243|abbb11|c']
    for order in orders:
        processOrder(ob, order)
        out.append(getBestBidAndAsk(ob, 'AAPL'))

    assert out == ['209.0/0.0', '209.0/210.0', '209.0/210.0', '209.0/210.0', '0.0/210.0']
    # Explaination:
    #   When initial order with ID abbb11 is added, the price is the best Bid price as it is  the only order.
    #   When order abbb12 ia added, its price is the best ask price as only ask order.
    #   The quantity of order ID abbb11 is amended in the next run, but the prices remain unchanged.
    #   The quantity of order ID abbb12 is amended in the next run, but the prices remain unchanged.
    #   Order ID abbb11 is cancelled, resulting in no bid order to traverse to calculate bid, hence  0.0.


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger("").setLevel(logging.INFO)
    main()
