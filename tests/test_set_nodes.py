#import pytest
from src.basic_data_handling.set_nodes import (
    SetAdd,
    SetRemove,
    SetDiscard,
    SetPop,
    SetUnion,
    SetIntersection,
    SetDifference,
    SetSymmetricDifference,
    SetIsSubset,
    SetIsSuperset,
    SetIsDisjoint,
    SetContains,
    SetLength,
    SetToList
)

def test_set_add():
    node = SetAdd()
    assert node.add({1, 2}, 3) == ({1, 2, 3},)
    assert node.add({1, 2}, 1) == ({1, 2},)  # Adding an existing item


def test_set_remove():
    node = SetRemove()
    assert node.remove({1, 2, 3}, 2) == ({1, 3}, True)  # Successful removal
    assert node.remove({1, 2, 3}, 4) == ({1, 2, 3}, False)  # Item not in set


def test_set_discard():
    node = SetDiscard()
    assert node.discard({1, 2, 3}, 2) == ({1, 3},)  # Successful removal
    assert node.discard({1, 2, 3}, 4) == ({1, 2, 3},)  # No error for missing item


def test_set_pop():
    node = SetPop()
    input_set = {1, 2, 3}
    result_set, removed_item = node.pop(input_set)
    assert result_set != input_set  # Arbitrary item removed
    assert removed_item in input_set  # Removed item was part of original set

    empty_set = set()
    assert node.pop(empty_set) == (set(), None)  # Handle empty set


def test_set_union():
    node = SetUnion()
    assert node.union({1, 2}, {3, 4}) == ({1, 2, 3, 4},)
    assert node.union({1}, {2}, {3}, {4}) == ({1, 2, 3, 4},)
    assert node.union({1, 2}, set()) == ({1, 2},)  # Union with empty set


def test_set_intersection():
    node = SetIntersection()
    assert node.intersection({1, 2, 3}, {2, 3, 4}) == ({2, 3},)
    assert node.intersection({1, 2, 3}, {4, 5}) == (set(),)  # No common elements
    assert node.intersection({1, 2, 3}, {2, 3}, {3, 4}) == ({3},)  # Multiple sets


def test_set_difference():
    node = SetDifference()
    assert node.difference({1, 2, 3}, {2, 3, 4}) == ({1},)
    assert node.difference({1, 2, 3}, {4, 5}) == ({1, 2, 3},)  # Nothing to remove


def test_set_symmetric_difference():
    node = SetSymmetricDifference()
    assert node.symmetric_difference({1, 2, 3}, {3, 4, 5}) == ({1, 2, 4, 5},)
    assert node.symmetric_difference({1, 2, 3}, {1, 2, 3}) == (set(),)  # No unique elements


def test_set_is_subset():
    node = SetIsSubset()
    assert node.is_subset({1, 2}, {1, 2, 3}) == (True,)
    assert node.is_subset({1, 4}, {1, 2, 3}) == (False,)
    assert node.is_subset(set(), {1, 2, 3}) == (True,)  # Empty set is subset of all sets


def test_set_is_superset():
    node = SetIsSuperset()
    assert node.is_superset({1, 2, 3}, {1, 2}) == (True,)
    assert node.is_superset({1, 2}, {1, 2, 3}) == (False,)
    assert node.is_superset(set(), set()) == (True,)  # Empty set is a superset of itself


def test_set_is_disjoint():
    node = SetIsDisjoint()
    assert node.is_disjoint({1, 2}, {3, 4}) == (True,)  # No common elements
    assert node.is_disjoint({1, 2}, {2, 3}) == (False,)  # Common element


def test_set_contains():
    node = SetContains()
    assert node.contains({1, 2, 3}, 2) == (True,)
    assert node.contains({1, 2, 3}, 4) == (False,)


def test_set_length():
    node = SetLength()
    assert node.length({1, 2, 3}) == (3,)
    assert node.length(set()) == (0,)  # Empty set


def test_set_to_list():
    node = SetToList()
    result = node.convert({1, 2, 3})
    assert isinstance(result, tuple)
    assert sorted(result[0]) == [1, 2, 3]  # Validate conversion to list
