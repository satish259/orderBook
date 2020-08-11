# coding=utf-8
import pytest
from Order import Order


def test_order():
    """
    This is a perfect case!
    A new order initialOrder is created an then used to create updatedOrder in perfect use case. No errors.
    Asserts to check updating is happening correctly.
    """
    initialOrder = Order(1568390243, 'abbb11', 'AAPL', 'B', 209.00000, 100)
    updatedOrder = Order(1568390247, 'abbb11', quantity=101, orgOrder=initialOrder)
    assert updatedOrder.ticker == 'AAPL'
    assert updatedOrder.quantity == 101
    assert updatedOrder.side == 'B'


def test_order_side_error():
    """
    Incorrect side A
    """
    with pytest.raises(ValueError,
                       match="Incorrect/invalid side with value A. B for Buy or S for Sell are the allowable values."):
        Order(1568390243, 'abbb11', 'AAPL', 'A', 209.00000, 100)


def test_order_complex_price_error():
    """
    Incorrect price complex number 3+4j
    """
    with pytest.raises(TypeError):
        Order(1568390243, 'abbb11', 'AAPL', 'B', complex(3 + 4j), 100)


def test_order_long_price_error():
    """
    Incorrect price too long
    """
    with pytest.raises(ValueError,
                       match="Incorrect/invalid price with value 3.141576. Price must be float, positive, "
                             "of 5 decimal places or fewer ,and greater than zero."):
        Order(1568390243, 'abbb11', 'AAPL', 'B', 3.141576, 100)


def test_order_negative_price_error():
    """
    Incorrect negative price
    """
    with pytest.raises(ValueError,
                       match="Incorrect/invalid price with value -1. Price must be float, positive, of 5 decimal "
                             "places or fewer ,and greater than zero."):
        Order(1568390243, 'abbb11', 'AAPL', 'B', -1, 100)


def test_order_negative_quantity_error():
    """
    Incorrect negative quantity
    """
    with pytest.raises(ValueError,
                       match="Incorrect/invalid quantity with value -100. Quantity must be float, positive, a whole "
                             "numeric and greater than zero."):
        Order(1568390243, 'abbb11', 'AAPL', 'B', 1.0, -100)
