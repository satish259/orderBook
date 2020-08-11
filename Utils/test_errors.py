# coding=utf-8
import pytest
from Utils.errors import customValueError


def test_custom_value_error():
    with pytest.raises(ValueError, match=r"Incorrect/invalid key with value value. More Error detail."):
        customValueError('key', 'value', 'More Error detail.')
