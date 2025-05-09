import pytest
from src.basic_data_handling.comparison_nodes import (
    Equal,
    NotEqual,
    GreaterThan,
    LessThan,
    GreaterThanOrEqual,
    LessThanOrEqual,
    StringComparison,
    NumberInRange,
    IsNull,
    CompareLength,
)


def test_equal():
    node = Equal()
    assert node.compare(10, 10) == (True,)
    assert node.compare(10, 20) == (False,)
    assert node.compare("hello", "hello") == (True,)
    assert node.compare([1, 2], [1, 2]) == (True,)
    assert node.compare(None, None) == (True,)


def test_not_equal():
    node = NotEqual()
    assert node.compare(10, 10) == (False,)
    assert node.compare(10, 20) == (True,)
    assert node.compare("hello", "world") == (True,)
    assert node.compare([1, 2], [1, 3]) == (True,)
    assert node.compare(None, []) == (True,)


def test_greater_than():
    node = GreaterThan()
    assert node.compare(10, 5) == (True,)
    assert node.compare(5, 10) == (False,)
    assert node.compare(10, 10) == (False,)
    assert node.compare(5.6, 2.3) == (True,)


def test_less_than():
    node = LessThan()
    assert node.compare(5, 10) == (True,)
    assert node.compare(10, 5) == (False,)
    assert node.compare(10, 10) == (False,)
    assert node.compare(2.3, 5.6) == (True,)


def test_greater_than_or_equal():
    node = GreaterThanOrEqual()
    assert node.compare(10, 10) == (True,)
    assert node.compare(15, 10) == (True,)
    assert node.compare(5, 10) == (False,)
    assert node.compare(5.5, 5.5) == (True,)


def test_less_than_or_equal():
    node = LessThanOrEqual()
    assert node.compare(10, 10) == (True,)
    assert node.compare(5, 15) == (True,)
    assert node.compare(15, 5) == (False,)
    assert node.compare(3.1, 3.1) == (True,)


def test_string_comparison():
    node = StringComparison()

    # Case-sensitive tests
    assert node.compare("hello", "hello", "==", "True") == (True,)
    assert node.compare("apple", "banana", "<", "True") == (True,)
    assert node.compare("apple", "banana", ">", "True") == (False,)
    assert node.compare("apple", "apple", "!=", "True") == (False,)

    # Case-insensitive tests
    assert node.compare("Hello", "hello", "==", "False") == (True,)
    assert node.compare("Apple", "BANANA", "<", "False") == (True,)
    assert node.compare("Grape", "GRAPE", ">=", "False") == (True,)


def test_number_in_range():
    node = NumberInRange()

    # Inclusive range tests
    assert node.check_range(50, 0, 100) == (True,)
    assert node.check_range(0, 0, 100) == (True,)

    # Exclusive range tests
    assert node.check_range(0, 0, 100, include_min="False") == (False,)
    assert node.check_range(100, 0, 100, include_max="False") == (False,)

    # Out of range tests
    assert node.check_range(-1, 0, 100) == (False,)
    assert node.check_range(101, 0, 100) == (False,)


def test_is_null():
    node = IsNull()
    assert node.check_null(None) == (True,)
    assert node.check_null(0) == (False,)
    assert node.check_null("") == (False,)
    assert node.check_null([]) == (False,)


def test_compare_length():
    node = CompareLength()

    # Valid comparisons
    assert node.compare_length([1, 2, 3], "==", 3) == (True, 3)
    assert node.compare_length("hello", "!=", 4) == (True, 5)
    assert node.compare_length((1, 2), ">", 1) == (True, 2)

    # Invalid comparisons
    assert node.compare_length({"key": "value"}, "<", 1) == (False, 1)
    assert node.compare_length(123, "==", 0) == (False, -1)  # Non-container input edge case
