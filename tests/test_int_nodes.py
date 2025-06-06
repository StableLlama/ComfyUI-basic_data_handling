import pytest
from src.basic_data_handling.int_nodes import (
    IntAdd,
    IntSubtract,
    IntMultiply,
    IntDivide,
    IntDivideSafe,
    IntModulus,
    IntPower,
    IntBitLength,
    IntToBytes,
    IntFromBytes,
    IntBitCount,
    IntCreate,
    IntCreateWithBase,
)


def test_int_add():
    node = IntAdd()
    assert node.add(10, 5) == (15,)
    assert node.add(-10, 5) == (-5,)
    assert node.add(0, 0) == (0,)


def test_int_subtract():
    node = IntSubtract()
    assert node.subtract(10, 5) == (5,)
    assert node.subtract(5, 10) == (-5,)
    assert node.subtract(0, 0) == (0,)


def test_int_multiply():
    node = IntMultiply()
    assert node.multiply(10, 5) == (50,)
    assert node.multiply(-1, 5) == (-5,)
    assert node.multiply(0, 5) == (0,)


def test_int_divide():
    node = IntDivide()
    assert node.divide(10, 2) == (5,)
    assert node.divide(9, 4) == (2,)  # Integer division
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        node.divide(10, 0)


def test_int_modulus():
    node = IntModulus()
    assert node.modulus(10, 3) == (1,)
    assert node.modulus(9, 9) == (0,)
    with pytest.raises(ValueError, match="Cannot perform modulus operation by zero."):
        node.modulus(10, 0)


def test_int_power():
    node = IntPower()
    assert node.power(2, 3) == (8,)
    assert node.power(10, 0) == (1,)  # Any number to the power 0 is 1
    assert node.power(-2, 3) == (-8,)


def test_int_bit_length():
    node = IntBitLength()
    assert node.bit_length(0) == (0,)  # Zero requires 0 bits
    assert node.bit_length(1) == (1,)
    assert node.bit_length(255) == (8,)  # 255 requires 8 bits
    assert node.bit_length(-255) == (8,)  # Negative numbers have the same bit length


def test_int_to_bytes():
    node = IntToBytes()
    assert node.to_bytes(255, 2, "big", "False") == (b"\x00\xff",)
    assert node.to_bytes(255, 2, "little", "False") == (b"\xff\x00",)
    assert node.to_bytes(-255, 2, "big", "True") == (b"\xff\x01",)


def test_int_from_bytes():
    node = IntFromBytes()
    assert node.from_bytes(b"\x00\xff", "big", "False") == (255,)
    assert node.from_bytes(b"\xff\x00", "little", "False") == (255,)
    assert node.from_bytes(b"\xff\x01", "big", "True") == (-255,)


def test_int_bit_count():
    node = IntBitCount()
    assert node.bit_count(0) == (0,)  # Zero has no 1 bits
    assert node.bit_count(255) == (8,)  # 255 is 11111111 (8 ones)
    assert node.bit_count(-255) == (8,)  # Negative integer has the same bit count


def test_int_create():
    node = IntCreate()
    assert node.create("42") == (42,)
    assert node.create("-100") == (-100,)
    assert node.create("0") == (0,)
    assert node.create("0xFF") == (255,)  # Hexadecimal
    assert node.create("0b1010") == (10,)  # Binary
    assert node.create("0o777") == (511,)  # Octal


def test_int_create_with_base():
    node = IntCreateWithBase()
    assert node.create("42", 10) == (42,)
    assert node.create("FF", 16) == (255,)
    assert node.create("1010", 2) == (10,)
    assert node.create("777", 8) == (511,)
    with pytest.raises(ValueError):
        node.create("FF", 10)  # Invalid characters for base 10


def test_int_divide_safe():
    node = IntDivideSafe()
    assert node.divide(10, 2, 9223372036854775807) == (5,)
    assert node.divide(9, 4, 9223372036854775807) == (2,)  # Integer division
    assert node.divide(10, 0, 9223372036854775807) == (9223372036854775807,)  # Positive infinity
    assert node.divide(-10, 0, 9223372036854775807) == (-9223372036854775807,)  # Negative infinity
