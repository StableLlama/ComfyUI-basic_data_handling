import pytest
from ..src.basic_data_handling.comparison_nodes import (
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
    # Test complex objects
    assert node.compare({"a": 1}, {"a": 1}) == (True,)
    assert node.compare({"a": 1}, {"a": 2}) == (False,)


def test_not_equal():
    node = NotEqual()
    assert node.compare(10, 10) == (False,)
    assert node.compare(10, 20) == (True,)
    assert node.compare("hello", "world") == (True,)
    assert node.compare([1, 2], [1, 3]) == (True,)
    assert node.compare(None, []) == (True,)
    # Test complex objects
    assert node.compare({"a": 1}, {"b": 1}) == (True,)
    assert node.compare({"a": 1}, {"a": 1}) == (False,)


def test_greater_than():
    node = GreaterThan()
    assert node.compare(10, 5) == (True,)
    assert node.compare(5, 10) == (False,)
    assert node.compare(10, 10) == (False,)
    assert node.compare(5.6, 2.3) == (True,)
    # Test negative numbers
    assert node.compare(-5, -10) == (True,)
    assert node.compare(-10, -5) == (False,)
    # Test zeroes
    assert node.compare(0, -1) == (True,)
    assert node.compare(0, 0) == (False,)


def test_less_than():
    node = LessThan()
    assert node.compare(5, 10) == (True,)
    assert node.compare(10, 5) == (False,)
    assert node.compare(10, 10) == (False,)
    assert node.compare(2.3, 5.6) == (True,)
    # Test negative numbers
    assert node.compare(-10, -5) == (True,)
    assert node.compare(-5, -10) == (False,)
    # Test zeroes
    assert node.compare(-1, 0) == (True,)
    assert node.compare(0, 0) == (False,)


def test_greater_than_or_equal():
    node = GreaterThanOrEqual()
    assert node.compare(10, 10) == (True,)
    assert node.compare(15, 10) == (True,)
    assert node.compare(5, 10) == (False,)
    assert node.compare(5.5, 5.5) == (True,)
    # Test negative numbers
    assert node.compare(-5, -10) == (True,)
    assert node.compare(-5, -5) == (True,)
    # Test zeroes
    assert node.compare(0, 0) == (True,)
    assert node.compare(0.0, -0.0) == (True,)


def test_less_than_or_equal():
    node = LessThanOrEqual()
    assert node.compare(10, 10) == (True,)
    assert node.compare(5, 15) == (True,)
    assert node.compare(15, 5) == (False,)
    assert node.compare(3.1, 3.1) == (True,)
    # Test negative numbers
    assert node.compare(-10, -5) == (True,)
    assert node.compare(-5, -5) == (True,)
    # Test zeroes
    assert node.compare(0, 0) == (True,)
    assert node.compare(-0.0, 0.0) == (True,)


def test_string_comparison():
    node = StringComparison()

    # Case-sensitive tests
    assert node.compare("hello", "hello", "==", "True") == (True,)
    assert node.compare("apple", "banana", "<", "True") == (True,)
    assert node.compare("apple", "banana", ">", "True") == (False,)
    assert node.compare("apple", "apple", "!=", "True") == (False,)
    assert node.compare("banana", "apple", ">=", "True") == (True,)
    assert node.compare("apple", "banana", "<=", "True") == (True,)

    # Case-insensitive tests
    assert node.compare("Hello", "hello", "==", "False") == (True,)
    assert node.compare("Apple", "BANANA", "<", "False") == (True,)
    assert node.compare("Grape", "GRAPE", ">=", "False") == (True,)
    assert node.compare("ZEBRA", "zoo", "<", "False") == (True,)
    assert node.compare("ZOO", "zebra", ">", "False") == (True,)

    # Empty string tests
    assert node.compare("", "hello", "<", "True") == (True,)
    assert node.compare("hello", "", ">", "True") == (True,)
    assert node.compare("", "", "==", "True") == (True,)


def test_number_in_range():
    node = NumberInRange()

    # Inclusive range tests
    assert node.check_range(50, 0, 100) == (True,)
    assert node.check_range(0, 0, 100) == (True,)
    assert node.check_range(100, 0, 100) == (True,)

    # Exclusive range tests
    assert node.check_range(0, 0, 100, include_min="False") == (False,)
    assert node.check_range(100, 0, 100, include_max="False") == (False,)
    assert node.check_range(50, 0, 100, include_min="False", include_max="False") == (True,)

    # Out of range tests
    assert node.check_range(-1, 0, 100) == (False,)
    assert node.check_range(101, 0, 100) == (False,)

    # Edge cases
    assert node.check_range(0, 0, 0) == (True,)
    assert node.check_range(0, 0, 0, include_min="False") == (False,)
    assert node.check_range(0, 0, 0, include_max="False") == (False,)

    # Negative range tests
    assert node.check_range(-50, -100, -10) == (True,)
    assert node.check_range(-10, -100, -10) == (True,)
    assert node.check_range(-100, -100, -10) == (True,)


def test_is_null():
    node = IsNull()
    assert node.check_null(None) == (True,)
    assert node.check_null(0) == (False,)
    assert node.check_null("") == (False,)
    assert node.check_null([]) == (False,)
    assert node.check_null(False) == (False,)
    # Additional edge cases
    assert node.check_null([None]) == (False,)  # List containing None
    assert node.check_null("None") == (False,)  # String "None"


def test_compare_length():
    node = CompareLength()

    # Valid comparisons with different operators
    assert node.compare_length([1, 2, 3], "==", 3) == (True, 3)
    assert node.compare_length("hello", "!=", 4) == (True, 5)
    assert node.compare_length((1, 2), ">", 1) == (True, 2)
    assert node.compare_length([1, 2, 3], "<", 4) == (True, 3)
    assert node.compare_length("test", ">=", 4) == (True, 4)
    assert node.compare_length([1], "<=", 1) == (True, 1)

    # Different container types
    assert node.compare_length({"a", "b", "c"}, "==", 3) == (True, 3)  # Set
    assert node.compare_length({"key1": 1, "key2": 2}, "==", 2) == (True, 2)  # Dict

    # Empty containers
    assert node.compare_length([], "==", 0) == (True, 0)
    assert node.compare_length("", "==", 0) == (True, 0)
    assert node.compare_length({}, "==", 0) == (True, 0)

    # Invalid comparisons
    assert node.compare_length({"key": "value"}, "<", 1) == (False, 1)  # Dict with 1 item
    assert node.compare_length(123, "==", 0) == (False, -1)  # Non-container input
    assert node.compare_length(None, "==", 0) == (False, -1)  # None

    # Error case with invalid operator
    with pytest.raises(ValueError):
        node.compare_length([1, 2, 3], "invalid", 3)
