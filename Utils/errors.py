# coding=utf-8
def customValueError(k, v, moreDetail='') -> object:
    """
    Simple value error for key, value pairs from order.
    :rtype: object
    """
    raise ValueError('Incorrect/invalid {} with value {}. '.format(k, v) + moreDetail)
