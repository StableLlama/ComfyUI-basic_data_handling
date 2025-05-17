import math
import pytest
from src.basic_data_handling.float_nodes import (
    FloatCreate,
    FloatAdd,
    FloatSubtract,
    FloatMultiply,
    FloatDivide,
    FloatDivideSafe,
    FloatPower,
    FloatRound,
    FloatIsInteger,
    FloatAsIntegerRatio,
    FloatHex,
    FloatFromHex,
)

def test_float_create():
    node = FloatCreate()
    assert node.create("3.14") == (3.14,)
    assert node.create("-2.5") == (-2.5,)
    assert node.create("0.0") == (0.0,)
    with pytest.raises(ValueError):
        node.create("not a number")


def test_float_add():
    node = FloatAdd()
    assert node.add(2.2, 2.2) == (4.4,)
    assert node.add(-1.5, 1.5) == (0.0,)
    assert node.add(0.0, 0.0) == (0.0,)


def test_float_subtract():
    node = FloatSubtract()
    assert node.subtract(5.5, 2.2) == (3.3,)
    assert node.subtract(-1.5, 1.5) == (-3.0,)
    assert node.subtract(0.0, 0.0) == (0.0,)


def test_float_multiply():
    node = FloatMultiply()
    assert node.multiply(2.0, 3.5) == (7.0,)
    assert node.multiply(-2.0, 3.0) == (-6.0,)
    assert node.multiply(0.0, 5.0) == (0.0,)


def test_float_divide():
    node = FloatDivide()
    assert node.divide(7.0, 2.0) == (3.5,)
    assert node.divide(-6.0, 3.0) == (-2.0,)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        node.divide(5.0, 0.0)


def test_float_divide_safe():
    node = FloatDivideSafe()

    assert node.divide(7.0, 2.0) == (3.5,)
    assert node.divide(-6.0, 3.0) == (-2.0,)
    assert node.divide(5.0, 0.0) == (float('inf'),)
    assert node.divide(-5.0, 0.0) == (float('-inf'),)

    # Special handling for NaN because NaN != NaN
    result = node.divide(0.0, 0.0)
    assert len(result) == 1
    assert math.isnan(result[0])


def test_float_power():
    node = FloatPower()
    assert node.power(2.0, 3.0) == (8.0,)
    assert node.power(5.0, 0.0) == (1.0,)
    assert node.power(-2.0, 3.0) == (-8.0,)


def test_float_round():
    node = FloatRound()
    assert node.round(3.14159, 2) == (3.14,)
    assert node.round(2.71828, 3) == (2.718,)
    assert node.round(-1.2345, 1) == (-1.2,)
    assert node.round(0.0, 0) == (0.0,)


def test_float_is_integer():
    node = FloatIsInteger()
    assert node.is_integer(3.0) == (True,)
    assert node.is_integer(3.14) == (False,)
    assert node.is_integer(-2.0) == (True,)
    assert node.is_integer(0.0) == (True,)


def test_float_as_integer_ratio():
    node = FloatAsIntegerRatio()
    assert node.as_integer_ratio(3.5) == (7, 2)
    assert node.as_integer_ratio(2.0) == (2, 1)
    assert node.as_integer_ratio(-1.25) == (-5, 4)


def test_float_hex():
    node = FloatHex()
    assert node.to_hex(3.5) == ("0x1.c000000000000p+1",)
    assert node.to_hex(0.0) == ("0x0.0p+0",)
    assert node.to_hex(-2.5) == ("-0x1.4000000000000p+1",)


def test_float_from_hex():
    node = FloatFromHex()
    assert node.from_hex("0x1.c000000000000p+1") == (3.5,)
    assert node.from_hex("0x0.0p+0") == (0.0,)
    assert node.from_hex("-0x1.4000000000000p+1") == (-2.5,)
