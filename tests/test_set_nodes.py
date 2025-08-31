#import pytest
from src.basic_data_handling.set_nodes import (
    SetAdd,
    SetAll,
    SetAny,
    SetContains,
    SetCreate,
    SetCreateFromBoolean,
    SetCreateFromFloat,
    SetCreateFromInt,
    SetCreateFromString,
    SetDifference,
    SetDiscard,
    SetEnumerate,
    SetIntersection,
    SetIsDisjoint,
    SetIsSubset,
    SetIsSuperset,
    SetLength,
    SetPop,
    SetPopRandom,
    SetRemove,
    SetSum,
    SetSymmetricDifference,
    SetToDataList,
    SetToList,
    SetUnion,
)

def test_set_create():
    node = SetCreate()
    # Testing with kwargs to simulate dynamic inputs
    assert node.create_set(item_0=1, item_1=2, item_2=3, item_3="") == ({1, 2, 3},)
    assert node.create_set(item_0="a", item_1="b", item_2="") == ({"a", "b"},)
    assert node.create_set() == (set(),)  # Empty set with no arguments
    # Mixed types
    assert node.create_set(item_0=1, item_1="b", item_2=True, item_3="") == ({1, "b", True},)


def test_set_create_from_int():
    node = SetCreateFromInt()
    assert node.create_set(item_0=1, item_1=2, item_2=3, item_3="") == ({1, 2, 3},)
    assert node.create_set(item_0=5, item_1="") == ({5},)  # Single item set
    assert node.create_set(item_0=1, item_1=1, item_2="") == ({1},)  # Duplicate items become single item
    assert node.create_set() == (set(),)  # Empty set with no arguments


def test_set_create_from_string():
    node = SetCreateFromString()
    result = node.create_set(item_0="apple", item_1="banana", item_2="")
    assert isinstance(result[0], set)
    assert result[0] == {"apple", "banana"}

    # Duplicate strings
    result = node.create_set(item_0="apple", item_1="apple", item_2="")
    assert result[0] == {"apple"}

    # Empty set
    assert node.create_set() == (set(),)


def test_set_create_from_float():
    node = SetCreateFromFloat()
    assert node.create_set(item_0=1.5, item_1=2.5, item_2="") == ({1.5, 2.5},)
    assert node.create_set(item_0=3.14, item_1="") == ({3.14},)  # Single item set
    assert node.create_set(item_0=1.0, item_1=1.0, item_2="") == ({1.0},)  # Duplicate items
    assert node.create_set() == (set(),)  # Empty set with no arguments


def test_set_create_from_boolean():
    node = SetCreateFromBoolean()
    assert node.create_set(item_0=True, item_1=False, item_2="") == ({True, False},)
    assert node.create_set(item_0=True, item_1=True, item_2="") == ({True},)  # Duplicate booleans
    assert node.create_set() == (set(),)  # Empty set with no arguments
    # Test conversion from non-boolean values
    assert node.create_set(item_0=1, item_1=0, item_2="") == ({True, False},)


def test_set_add():
    node = SetAdd()
    assert node.add({1, 2}, 3) == ({1, 2, 3},)
    assert node.add({1, 2}, 1) == ({1, 2},)  # Adding an existing item
    assert node.add(set(), "first") == ({"first"},)  # Adding to empty set
    assert node.add({1, 2}, "string") == ({1, 2, "string"},)  # Adding different type


def test_set_remove():
    node = SetRemove()
    assert node.remove({1, 2, 3}, 2) == ({1, 3}, True)  # Successful removal
    assert node.remove({1, 2, 3}, 4) == ({1, 2, 3}, False)  # Item not in set
    assert node.remove({1}, 1) == (set(), True)  # Removing the only element
    assert node.remove(set(), 1) == (set(), False)  # Removing from empty set


def test_set_discard():
    node = SetDiscard()
    assert node.discard({1, 2, 3}, 2) == ({1, 3},)  # Successful removal
    assert node.discard({1, 2, 3}, 4) == ({1, 2, 3},)  # No error for missing item
    assert node.discard({1}, 1) == (set(),)  # Discarding the only element
    assert node.discard(set(), 1) == (set(),)  # Discarding from empty set


def test_set_pop():
    node = SetPop()
    input_set = {1, 2, 3}
    result_set, removed_item = node.pop(input_set)
    assert result_set != input_set  # Arbitrary item removed
    assert removed_item in input_set  # Removed item was part of original set
    assert len(result_set) == len(input_set) - 1  # One item was removed
    assert removed_item not in result_set  # Removed item is not in result set

    empty_set = set()
    assert node.pop(empty_set) == (set(), None)  # Handle empty set


def test_set_pop_random():
    node = SetPopRandom()
    # Test with single item - must remove that item
    single_item_set = {42}
    result_set, removed_item = node.pop_random_element(single_item_set)
    assert result_set == set() and removed_item == 42

    # Test with multiple items - can't predict which one will be popped
    # but we can check the result set size and that the popped item was from the original set
    original_set = {1, 2, 3, 4}
    result_set, removed_item = node.pop_random_element(original_set)
    assert len(result_set) == len(original_set) - 1
    assert removed_item in original_set
    assert removed_item not in result_set

    # Test with empty set
    empty_set = set()
    assert node.pop_random_element(empty_set) == (set(), None)


def test_set_union():
    node = SetUnion()
    assert node.union({1, 2}, {3, 4}) == ({1, 2, 3, 4},)
    assert node.union({1}, {2}, {3}, {4}) == ({1, 2, 3, 4},)
    assert node.union({1, 2}, set()) == ({1, 2},)  # Union with empty set
    assert node.union(set(), set()) == (set(),)  # Union of empty sets
    assert node.union({1, 2}, {2, 3}) == ({1, 2, 3},)  # Overlapping sets


def test_set_intersection():
    node = SetIntersection()
    assert node.intersection({1, 2, 3}, {2, 3, 4}) == ({2, 3},)
    assert node.intersection({1, 2, 3}, {4, 5}) == (set(),)  # No common elements
    assert node.intersection({1, 2, 3}, {2, 3}, {3, 4}) == ({3},)  # Multiple sets
    assert node.intersection({1, 2, 3}, {1, 2, 3}) == ({1, 2, 3},)  # Identical sets
    assert node.intersection(set(), {1, 2, 3}) == (set(),)  # Empty set intersection


def test_set_difference():
    node = SetDifference()
    assert node.difference({1, 2, 3}, {2, 3, 4}) == ({1},)
    assert node.difference({1, 2, 3}, {4, 5}) == ({1, 2, 3},)  # Nothing to remove
    assert node.difference({1, 2, 3}, {1, 2, 3}) == (set(),)  # Identical sets
    assert node.difference(set(), {1, 2, 3}) == (set(),)  # Empty set difference
    assert node.difference({1, 2, 3}, set()) == ({1, 2, 3},)  # Difference with empty set


def test_set_symmetric_difference():
    node = SetSymmetricDifference()
    assert node.symmetric_difference({1, 2, 3}, {3, 4, 5}) == ({1, 2, 4, 5},)
    assert node.symmetric_difference({1, 2, 3}, {1, 2, 3}) == (set(),)  # No unique elements
    assert node.symmetric_difference(set(), {1, 2, 3}) == ({1, 2, 3},)  # Empty set symmetric difference
    assert node.symmetric_difference({1, 2, 3}, set()) == ({1, 2, 3},)  # Symmetric difference with empty set


def test_set_is_subset():
    node = SetIsSubset()
    assert node.is_subset({1, 2}, {1, 2, 3}) == (True,)
    assert node.is_subset({1, 4}, {1, 2, 3}) == (False,)
    assert node.is_subset(set(), {1, 2, 3}) == (True,)  # Empty set is subset of all sets
    assert node.is_subset({1, 2}, {1, 2}) == (True,)  # Set is subset of itself
    assert node.is_subset({1, 2, 3}, {1, 2}) == (False,)  # Superset is not a subset


def test_set_is_superset():
    node = SetIsSuperset()
    assert node.is_superset({1, 2, 3}, {1, 2}) == (True,)
    assert node.is_superset({1, 2}, {1, 2, 3}) == (False,)
    assert node.is_superset(set(), set()) == (True,)  # Empty set is a superset of itself
    assert node.is_superset({1, 2}, {1, 2}) == (True,)  # Set is superset of itself
    assert node.is_superset({1, 2}, set()) == (True,)  # Any set is superset of empty set


def test_set_is_disjoint():
    node = SetIsDisjoint()
    assert node.is_disjoint({1, 2}, {3, 4}) == (True,)  # No common elements
    assert node.is_disjoint({1, 2}, {2, 3}) == (False,)  # Common element
    assert node.is_disjoint(set(), {1, 2, 3}) == (True,)  # Empty set is disjoint with any set
    assert node.is_disjoint({1, 2}, set()) == (True,)  # Empty set is disjoint with any set
    assert node.is_disjoint(set(), set()) == (True,)  # Empty sets are disjoint


def test_set_contains():
    node = SetContains()
    assert node.contains({1, 2, 3}, 2) == (True,)
    assert node.contains({1, 2, 3}, 4) == (False,)
    assert node.contains(set(), 1) == (False,)  # Empty set contains nothing
    assert node.contains({1, "string", True}, "string") == (True,)  # Mixed type set
    assert node.contains({1, "string", True}, False) == (False,)  # Boolean check


def test_set_length():
    node = SetLength()
    assert node.length({1, 2, 3}) == (3,)
    assert node.length(set()) == (0,)  # Empty set
    assert node.length({1, 1, 1, 1}) == (1,)  # Set with duplicate values (only counts unique)
    assert node.length({12, "string", True, 3.14}) == (4,)  # Mixed types


def test_set_to_list():
    node = SetToList()
    result = node.convert({1, 2, 3})
    assert isinstance(result, tuple)
    assert isinstance(result[0], list)
    assert sorted(result[0]) == [1, 2, 3]  # Validate conversion to list

    # Empty set
    result = node.convert(set())
    assert result[0] == []

    # Mixed types
    result = node.convert({1, "string", True})
    assert set(result[0]) == {1, "string", True}  # Can't check order, just content


def test_set_to_data_list():
    node = SetToDataList()
    result = node.convert({1, 2, 3})
    assert isinstance(result, tuple)
    assert isinstance(result[0], list)
    assert sorted(result[0]) == [1, 2, 3]  # Validate conversion to data list

    # Empty set
    result = node.convert(set())
    assert result[0] == []

    # Mixed types
    result = node.convert({1, "string", True})
    assert set(result[0]) == {1, "string", True}  # Can't check order, just content

    # Empty set
    result = node.convert(set())
    assert result[0] == []

    # Mixed types
    result = node.convert({1, "string", True})
    assert set(result[0]) == {1, "string", True}  # Can't check order, just content


def test_set_all():
    node = SetAll()

    # Test with all truthy values
    assert node.check_all({1, True, "string", 3.14}) == (True,)

    # Test with one falsy value
    assert node.check_all({1, False, "string"}) == (False,)

    # Test with all falsy values
    assert node.check_all({False, 0, "", None}) == (False,)

    # Test with empty set (should return True per Python's all() behavior)
    assert node.check_all(set()) == (True,)


def test_set_any():
    node = SetAny()

    # Test with all truthy values
    assert node.check_any({1, True, "string", 3.14}) == (True,)

    # Test with one truthy value
    assert node.check_any({0, False, "", 1}) == (True,)

    # Test with all falsy values
    assert node.check_any({False, 0, "", None}) == (False,)

    # Test with empty set (should return False per Python's any() behavior)
    assert node.check_any(set()) == (False,)


def test_set_enumerate():
    node = SetEnumerate()

    # Basic test with default start=0
    result = node.enumerate_set({10, 20, 30})
    assert isinstance(result, tuple)
    assert isinstance(result[0], list)

    # Convert to set of tuples for comparison (order may vary)
    result_set = {tuple(item) for item in result[0]}
    assert result_set == {(0, 10), (1, 20), (2, 30)}

    # Test with custom start value
    result = node.enumerate_set({10, 20, 30}, start=5)
    result_set = {tuple(item) for item in result[0]}
    assert result_set == {(5, 10), (6, 20), (7, 30)}

    # Test with empty set
    result = node.enumerate_set(set())
    assert result[0] == []

    # Test with mixed types
    result = node.enumerate_set({1, "string", False})
    assert len(result[0]) == 3
    # Check format but not exact values due to arbitrary order
    for item in result[0]:
        assert isinstance(item, tuple)
        assert len(item) == 2
        assert isinstance(item[0], int)


def test_set_sum():
    node = SetSum()

    # Test with integer set
    int_result, float_result = node.sum_set({1, 2, 3})
    assert int_result == 6
    assert float_result == 6.0

    # Test with float set
    int_result, float_result = node.sum_set({1.5, 2.5, 3.0})
    assert int_result == 7.0
    assert float_result == 7.0

    # Test with mixed numeric types
    int_result, float_result = node.sum_set({1, 2.5, 3})
    assert int_result == 6.5
    assert float_result == 6.5

    # Test with custom start value
    int_result, float_result = node.sum_set({1, 2, 3}, start=10)
    assert int_result == 16
    assert float_result == 16.0

    # Test with empty set
    int_result, float_result = node.sum_set(set(), start=5)
    assert int_result == 5
    assert float_result == 5.0
