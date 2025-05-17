import pytest
from src.basic_data_handling.list_nodes import (
    ListCreate,
    ListCreateFromBoolean,
    ListCreateFromFloat,
    ListCreateFromInt,
    ListCreateFromString,
    ListAppend,
    ListExtend,
    ListInsert,
    ListRemove,
    ListPop,
    ListIndex,
    ListCount,
    ListSort,
    ListReverse,
    ListLength,
    ListSlice,
    ListGetItem,
    ListSetItem,
    ListContains,
    ListMin,
    ListMax,
    ListToDataList,
    ListToSet
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
    assert node.create_list(item_0=1, item_1=2, item_2=3) == ([1, 2, 3],)
    assert node.create_list() == ([],)  # Empty list
    assert node.create_list(item_0="test") == (["test"],)


def test_list_create_from_boolean():
    node = ListCreateFromBoolean()
    assert node.create_list(item_0=True, item_1=False, item_2=True) == ([True, False, True],)
    assert node.create_list(item_0=True) == ([True],)
    assert node.create_list() == ([],)


def test_list_create_from_float():
    node = ListCreateFromFloat()
    assert node.create_list(item_0=1.1, item_1=2.2, item_2=3.3) == ([1.1, 2.2, 3.3],)
    assert node.create_list(item_0=0.0) == ([0.0],)
    assert node.create_list() == ([],)


def test_list_create_from_int():
    node = ListCreateFromInt()
    assert node.create_list(item_0=1, item_1=2, item_2=3) == ([1, 2, 3],)
    assert node.create_list(item_0=0) == ([0],)
    assert node.create_list() == ([],)


def test_list_create_from_string():
    node = ListCreateFromString()
    assert node.create_list(item_0="a", item_1="b", item_2="c") == (["a", "b", "c"],)
    assert node.create_list(item_0="test") == (["test"],)
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
