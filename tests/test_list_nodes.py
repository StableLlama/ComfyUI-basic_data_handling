import pytest
from ..src.basic_data_handling.list_nodes import (
    ListAll,
    ListAny,
    ListAppend,
    ListContains,
    ListCount,
    ListCreate,
    ListCreateFromBoolean,
    ListCreateFromFloat,
    ListCreateFromInt,
    ListCreateFromString,
    ListEnumerate,
    ListExtend,
    ListFirst,
    ListGetItem,
    ListIndex,
    ListInsert,
    ListLast,
    ListLength,
    ListMax,
    ListMin,
    ListPop,
    ListPopRandom,
    ListRange,
    ListRemove,
    ListReverse,
    ListSetItem,
    ListSlice,
    ListSort,
    ListSum,
    ListToDataList,
    ListToSet,
)


def test_list_append():
    node = ListAppend()
    assert node.append([1, 2, 3], 4) == ([1, 2, 3, 4],)
    assert node.append([], "item") == (["item"],)
    assert node.append(["a", "b"], {"key": "value"}) == (["a", "b", {"key": "value"}],)


def test_list_extend():
    node = ListExtend()
    assert node.extend([1, 2], [3, 4]) == ([1, 2, 3, 4],)
    assert node.extend([], [1, 2, 3]) == ([1, 2, 3],)
    assert node.extend([1, 2], []) == ([1, 2],)


def test_list_insert():
    node = ListInsert()
    assert node.insert([1, 3, 4], 1, 2) == ([1, 2, 3, 4],)
    assert node.insert([], 0, "first") == (["first"],)
    assert node.insert([1, 2], 10, "out_of_bounds") == ([1, 2, "out_of_bounds"],)


def test_list_remove():
    node = ListRemove()
    assert node.remove([1, 2, 3, 2], 2) == ([1, 3, 2], True)
    assert node.remove([1, 2, 3], 4) == ([1, 2, 3], False)
    assert node.remove([], "not_in_list") == ([], False)


def test_list_pop():
    node = ListPop()
    assert node.pop([1, 2, 3], 1) == ([1, 3], 2)
    assert node.pop([1, 2, 3]) == ([1, 2], 3)  # Default: last item
    assert node.pop([], 0) == ([], None)  # Empty list pop


def test_list_pop_random():
    node = ListPopRandom()
    # Test with single item - must remove that item
    result, item = node.pop_random_element([42])
    assert result == [] and item == 42

    # Test with multiple items - can't predict which one will be popped
    # but we can check the result list length and that the popped item was from the original list
    original_list = [1, 2, 3, 4]
    result, item = node.pop_random_element(original_list)
    assert len(result) == len(original_list) - 1
    assert item in original_list
    assert item not in result

    # Test with empty list
    assert node.pop_random_element([]) == ([], None)


def test_list_first():
    node = ListFirst()
    assert node.get_first_element([1, 2, 3]) == (1,)
    assert node.get_first_element(["a", "b", "c"]) == ("a",)
    assert node.get_first_element([]) == (None,)  # Empty list


def test_list_last():
    node = ListLast()
    assert node.get_last_element([1, 2, 3]) == (3,)
    assert node.get_last_element(["a", "b", "c"]) == ("c",)
    assert node.get_last_element([]) == (None,)  # Empty list


def test_list_index():
    node = ListIndex()
    assert node.index([1, 2, 3, 2], 2) == (1,)
    assert node.index([1, 2, 3, 2], 2, 2) == (3,)
    assert node.index([1, 2, 3, 2], 4) == (-1,)


def test_list_count():
    node = ListCount()
    assert node.count([1, 2, 3, 2], 2) == (2,)
    assert node.count([], 1) == (0,)
    assert node.count(["a", "b", "a"], "a") == (2,)


def test_list_sort():
    node = ListSort()
    assert node.sort([3, 1, 2]) == ([1, 2, 3],)
    assert node.sort([3, 1, 2], "True") == ([3, 2, 1],)  # Reverse
    assert node.sort(["b", "a", "c"]) == (["a", "b", "c"],)
    assert node.sort([1, "a"]) == ([1, "a"],)  # Unsortable list


def test_list_reverse():
    node = ListReverse()
    assert node.reverse([1, 2, 3]) == ([3, 2, 1],)
    assert node.reverse([]) == ([],)
    assert node.reverse(["a", "b", "c"]) == (["c", "b", "a"],)


def test_list_length():
    node = ListLength()
    assert node.length([1, 2, 3]) == (3,)
    assert node.length([]) == (0,)
    assert node.length(["a", "b", "c", "d"]) == (4,)


def test_list_slice():
    node = ListSlice()
    assert node.slice([1, 2, 3, 4], 1, 3) == ([2, 3],)
    assert node.slice([1, 2, 3, 4], 0, -1) == ([1, 2, 3],)
    assert node.slice([1, 2, 3, 4], 0, 4, 2) == ([1, 3],)


def test_list_get_item():
    node = ListGetItem()
    assert node.get_item([1, 2, 3], 0) == (1,)
    assert node.get_item([1, 2, 3], -1) == (3,)
    assert node.get_item([], 0) == (None,)


def test_list_set_item():
    node = ListSetItem()
    assert node.set_item([1, 2, 3], 1, 42) == ([1, 42, 3],)
    with pytest.raises(IndexError):
        node.set_item([1, 2, 3], 3, 42) == ([1, 2, 3],)  # Out of range


def test_list_contains():
    node = ListContains()
    assert node.contains([1, 2, 3], 2) == (True,)
    assert node.contains([1, 2, 3], 4) == (False,)
    assert node.contains([], "value") == (False,)


def test_list_min():
    node = ListMin()
    assert node.find_min([1, 2, 3]) == (1,)
    assert node.find_min(["b", "a", "c"]) == ("a",)
    assert node.find_min([]) == (None,)


def test_list_max():
    node = ListMax()
    assert node.find_max([1, 2, 3]) == (3,)
    assert node.find_max(["b", "a", "c"]) == ("c",)
    assert node.find_max([]) == (None,)


def test_list_create():
    node = ListCreate()
    assert node.create_list(item_0=1, item_1=2, item_2=3, item_3="") == ([1, 2, 3],)
    assert node.create_list() == ([],)  # Empty list
    assert node.create_list(item_0="test", item_1="") == (["test"],)


def test_list_create_from_boolean():
    node = ListCreateFromBoolean()
    assert node.create_list(item_0=True, item_1=False, item_2=True, item_3="") == ([True, False, True],)
    assert node.create_list(item_0=True, item_1="") == ([True],)
    assert node.create_list() == ([],)


def test_list_create_from_float():
    node = ListCreateFromFloat()
    assert node.create_list(item_0=1.1, item_1=2.2, item_2=3.3, item_3="") == ([1.1, 2.2, 3.3],)
    assert node.create_list(item_0=0.0, item_1="") == ([0.0],)
    assert node.create_list() == ([],)


def test_list_create_from_int():
    node = ListCreateFromInt()
    assert node.create_list(item_0=1, item_1=2, item_2=3, item_3="") == ([1, 2, 3],)
    assert node.create_list(item_0=0, item_1="") == ([0],)
    assert node.create_list() == ([],)


def test_list_create_from_string():
    node = ListCreateFromString()
    assert node.create_list(item_0="a", item_1="b", item_2="c", item_3="") == (["a", "b", "c"],)
    assert node.create_list(item_0="test", item_1="") == (["test"],)
    assert node.create_list() == ([],)


def test_list_to_data_list():
    node = ListToDataList()
    input_list = [1, 2, 3]
    # The output should be the same list but marked as a data list by the OUTPUT_IS_LIST = (True,) flag
    assert node.convert(input_list) == (input_list,)


def test_list_to_set():
    node = ListToSet()
    assert node.convert([1, 2, 3, 2, 1]) == ({1, 2, 3},)
    assert node.convert([]) == (set(),)
    assert node.convert(["a", "b", "a", "c"]) == ({"a", "b", "c"},)


def test_list_range():
    node = ListRange()
    # Basic range with default step=1
    assert node.create_range(start=0, stop=5) == ([0, 1, 2, 3, 4],)

    # Range with custom step
    assert node.create_range(start=0, stop=10, step=2) == ([0, 2, 4, 6, 8],)

    # Negative step (counting down)
    assert node.create_range(start=5, stop=0, step=-1) == ([5, 4, 3, 2, 1],)

    # Start > stop with positive step (empty list)
    assert node.create_range(start=10, stop=5) == ([],)

    # Empty range
    assert node.create_range(start=0, stop=0) == ([],)

    # Test with negative indices
    assert node.create_range(start=-5, stop=0) == ([-5, -4, -3, -2, -1],)

    # Test error case: step=0
    with pytest.raises(ValueError, match="Step cannot be zero"):
        node.create_range(start=0, stop=5, step=0)


def test_list_all():
    node = ListAll()
    # All true values
    assert node.check_all([True, True, True]) == (True,)

    # Mixed values (all truthy)
    assert node.check_all([1, "text", [1, 2]]) == (True,)

    # Contains a false value
    assert node.check_all([True, False, True]) == (False,)

    # Contains a falsy value
    assert node.check_all([True, 0, True]) == (False,)

    # Empty list (returns True according to Python's all() behavior)
    assert node.check_all([]) == (True,)


def test_list_any():
    node = ListAny()
    # All true values
    assert node.check_any([True, True, True]) == (True,)

    # Mixed values with at least one true
    assert node.check_any([False, True, False]) == (True,)

    # Mixed values with at least one truthy
    assert node.check_any([0, "", 1]) == (True,)

    # All false values
    assert node.check_any([False, False, False]) == (False,)

    # All falsy values
    assert node.check_any([0, "", []]) == (False,)

    # Empty list (returns False according to Python's any() behavior)
    assert node.check_any([]) == (False,)


def test_list_enumerate():
    node = ListEnumerate()

    # Basic enumeration with default start=0
    result = node.enumerate_list(["a", "b", "c"])
    assert result == ([[(0, "a"), (1, "b"), (2, "c")]],)

    # Enumeration with custom start
    result = node.enumerate_list(["x", "y", "z"], start=10)
    assert result == ([[(10, "x"), (11, "y"), (12, "z")]],)

    # Enumeration of empty list
    result = node.enumerate_list([])
    assert result == ([[]],)

    # Enumeration of list with mixed types
    result = node.enumerate_list([1, "text", True])
    assert result == ([[(0, 1), (1, "text"), (2, True)]],)


def test_list_sum():
    node = ListSum()

    # Sum of integers
    int_result, float_result = node.sum_list([1, 2, 3, 4])
    assert int_result == 10
    assert float_result == 10.0

    # Sum with default start value (0)
    int_result, float_result = node.sum_list([5, 10, 15])
    assert int_result == 30
    assert float_result == 30.0

    # Sum with custom start value
    int_result, float_result = node.sum_list([1, 2, 3], start=10)
    assert int_result == 16
    assert float_result == 16.0

    # Sum of floats (should still return both int and float)
    int_result, float_result = node.sum_list([1.5, 2.5, 3.0])
    assert int_result == 7.0  # Note: This will be a float, but returned as first value
    assert float_result == 7.0

    # Sum of empty list
    int_result, float_result = node.sum_list([])
    assert int_result == 0
    assert float_result == 0.0

    # Sum of mixed numbers
    int_result, float_result = node.sum_list([1, 2.5, 3])
    assert int_result == 6.5
    assert float_result == 6.5
