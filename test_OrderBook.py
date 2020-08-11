# coding=utf-8
import pytest
from OrderBook import OrderBook, processOrder, getBestBidAndAsk

ob = OrderBook()


def test__add_order():
    """
    This is a perfect case!
    New order gets created successfully.
    """

    processOrder(ob, '1568390243|abbb11|a|AAPL|B|209.00000|100')
    assert getBestBidAndAsk(ob, 'AAPL') == '209.0/0.0'


def test__cancel_order():
    """
    This is a perfect case!
    Order gets cancelled properly.
    """
    processOrder(ob, '1568390243|abbb11|a|AAPL|B|209.00000|100')
    # Intentional incorrect cancel order as other colmns are ignores
    processOrder(ob, '1568390245|abbb11|c|AAPL|B|209.00000|100')
    assert getBestBidAndAsk(ob, 'AAPL') == '0.0/0.0'


def test__cancel_order_error():
    """
    Cancelling an order that does not exist.
    I choose to throw an error but the code can be changed to ignore it too!
    """
    with pytest.raises(ValueError,
                       match="Incorrect/invalid orderId with value abbb11. Unable to cancel order as it does not exist."):
        processOrder(ob, '1568390247|abbb11|c|AAPL|B|209.00000|100')


def test_max_bid_ask():
    """
    The perfect case is covered by other tests so covering zero case.
    """
    assert getBestBidAndAsk(ob, '') == '0.0/0.0'


def test__update_order():
    processOrder(ob, '1568390243|abbb11|a|AAPL|B|209.00000|100')
    # This covers changing ticker, side, price and quantity
    processOrder(ob, '1568390247|abbb11|u|JPM|S|101.00000|1')
    assert ob.orders['abbb11'].ticker == 'JPM'
    assert ob.orders['abbb11'].side == 'S'
    assert ob.orders['abbb11'].price == 101.0
    assert ob.orders['abbb11'].quantity == 1


def test__update_order_error():
    """
    Updating an order that does not exist.
    I choose to throw an error but the code can be changed to treat an update without an add as an add!
    """
    with pytest.raises(ValueError,
                       match="Incorrect/invalid orderId with value abbb. Unable to amend order as it does not exist."):
        processOrder(ob, '1568390247|abbb|u|100')


def test_process_order_error():
    """
    The perfect case is covered by other tests so covering incorrect action only.
    """
    with pytest.raises(ValueError,
                       match="Incorrect/invalid action with value K. a, u and c are the allowable actions."):
        processOrder(ob, '1568390243|abbb11|K')
