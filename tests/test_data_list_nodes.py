import pytest
from src.basic_data_handling.data_list_nodes import (
    DataListAppend,
    #DataListCreate,
    #DataListCreateFromBoolean,
    #DataListCreateFromFloat,
    #DataListCreateFromInt,
    #DataListCreateFromString,
    DataListExtend,
    DataListInsert,
    DataListRemove,
    DataListPop,
    DataListPopRandom,
    DataListIndex,
    DataListCount,
    DataListSort,
    DataListReverse,
    DataListLength,
    DataListSlice,
    DataListGetItem,
    DataListSetItem,
    DataListContains,
    DataListZip,
    DataListFilter,
    DataListFilterSelect,
    DataListFirst,
    DataListLast,
    DataListMin,
    DataListMax,
    #DataListToList,
    #DataListToSet,
)


def test_append():
    node = DataListAppend()
    assert node.append(list=[1, 2, 3], item=[4]) == ([1, 2, 3, 4],)
    assert node.append(list=[], item=["test"]) == (["test"],)
    assert node.append(list=[1, 2, 3], item=[]) == ([1, 2, 3],)


def test_extend():
    node = DataListExtend()
    assert node.extend(list_a=[1, 2], list_b=[3, 4]) == ([1, 2, 3, 4],)
    assert node.extend(list_a=[], list_b=["a", "b"]) == (["a", "b"],)
    assert node.extend(list_a=[1], list_b=[]) == ([1],)


def test_insert():
    node = DataListInsert()
    assert node.insert(list=[1, 2, 4], index=[2], item=[3]) == ([1, 2, 3, 4],)
    assert node.insert(list=[], index=[0], item=["a"]) == (["a"],)
    assert node.insert(list=[1, 2], index=[5], item=[3]) == ([1, 2, 3],)  # Out-of-range insert


def test_remove():
    node = DataListRemove()
    assert node.remove(list=[1, 2, 3], value=[2]) == ([1, 3], True)
    assert node.remove(list=["a", "b", "a"], value=["a"]) == (["b", "a"], True)
    assert node.remove(list=[1, 2, 3], value=[5]) == ([1, 2, 3], False)  # Value not found


def test_pop():
    node = DataListPop()
    assert node.pop(list=[1, 2, 3], index=[1]) == ([1, 3], 2)
    assert node.pop(list=["a", "b", "c"], index=[-1]) == (["a", "b"], "c")  # Negative index
    assert node.pop(list=[], index=[0]) == ([], None)  # Pop from empty list


def test_index():
    node = DataListIndex()
    assert node.list_index(list=["a", "b", "c"], value=["b"]) == (1,)
    assert node.list_index(list=[1, 2, 3], value=[5]) == (-1,)  # Value not found
    assert node.list_index(list=[1, 2, 1, 2], value=[1], start=[1]) == (2,)


def test_count():
    node = DataListCount()
    assert node.count(list=[1, 2, 1, 2], value=[1]) == (2,)
    assert node.count(list=["a", "b", "a"], value=["a"]) == (2,)
    assert node.count(list=[], value=["x"]) == (0,)


def test_sort():
    node = DataListSort()
    assert node.sort(list=[3, 2, 1]) == ([1, 2, 3],)
    assert node.sort(list=["c", "a", "b"]) == (["a", "b", "c"],)
    assert node.sort(list=[3, 1, 2], reverse=["True"]) == ([3, 2, 1],)  # Reverse sort


def test_reverse():
    node = DataListReverse()
    assert node.reverse(list=[1, 2, 3]) == ([3, 2, 1],)
    assert node.reverse(list=[]) == ([],)


def test_length():
    node = DataListLength()
    assert node.length(list=[1, 2, 3]) == (3,)
    assert node.length(list=[]) == (0,)


def test_slice():
    node = DataListSlice()
    assert node.slice(list=[1, 2, 3, 4, 5], start=[1], stop=[4]) == ([2, 3, 4],)
    assert node.slice(list=[1, 2, 3], start=[0], stop=[2], step=[2]) == ([1],)
    assert node.slice(list=["a", "b", "c"], start=[-2], stop=[3]) == (["b", "c"],)


def test_get_item():
    node = DataListGetItem()
    assert node.get_item(list=[1, 2, 3], index=[1]) == (2,)
    assert node.get_item(list=["a", "b", "c"], index=[-1]) == ("c",)  # Negative index
    assert node.get_item(list=[], index=[0]) == (None,)  # Out of range


def test_set_item():
    node = DataListSetItem()
    assert node.set_item(list=[1, 2, 3], index=[1], value=[9]) == ([1, 9, 3],)
    assert node.set_item(list=["a", "b", "c"], index=[-1], value=["z"]) == (["a", "b", "z"],)
    with pytest.raises(IndexError):
        node.set_item(list=[], index=[0], value=["test"])  # Out of range


def test_contains():
    node = DataListContains()
    assert node.contains(list=[1, 2, 3], value=[2]) == (True,)
    assert node.contains(list=["a", "b"], value=["c"]) == (False,)
    assert node.contains(list=[], value=["x"]) == (False,)


def test_zip():
    node = DataListZip()
    assert node.zip_lists(list1=[1, 2], list2=["a", "b"]) == ([[1, "a"], [2, "b"]],)
    assert node.zip_lists(list1=[1], list2=["a", "b"]) == ([[1, "a"]],)  # Shortest list length
    assert node.zip_lists(list1=[1, 2, 3], list2=["a", "b"]) == ([[1, "a"], [2, "b"]],)  # Different lengths


def test_filter():
    node = DataListFilter()
    assert node.filter_data(value=[1, 2, 3], filter=[False, True, False]) == ([1, 3],)
    assert node.filter_data(value=[1, 2], filter=[True, True]) == ([],)
    assert node.filter_data(value=[1, 2, 3], filter=[False, False, False]) == ([1, 2, 3],)


def test_min():
    node = DataListMin()
    assert node.find_min(list=[3, 1, 2]) == (1,)
    assert node.find_min(list=[-1, -5, 0]) == (-5,)
    assert node.find_min(list=[]) == (None,)


def test_max():
    node = DataListMax()
    assert node.find_max(list=[3, 1, 2]) == (3,)
    assert node.find_max(list=[-1, -5, 0]) == (0,)
    assert node.find_max(list=[]) == (None,)


def test_filter_select():
    node = DataListFilterSelect()
    true_list, false_list = node.select(value=[1, 2, 3], select=[True, False, True])
    assert true_list == [1, 3]
    assert false_list == [2]

    # All true case
    true_list, false_list = node.select(value=["a", "b"], select=[True, True])
    assert true_list == ["a", "b"]
    assert false_list == []

    # All false case
    true_list, false_list = node.select(value=[1, 2, 3], select=[False, False, False])
    assert true_list == []
    assert false_list == [1, 2, 3]


def test_pop_random():
    node = DataListPopRandom()
    result_list, item = node.pop_random_element(list=[1])
    assert result_list == [] and item == 1  # Only one item, so it must be chosen

    # With multiple items, we can't predict which one will be popped
    # But we can check that an item was removed and returned
    result_list, item = node.pop_random_element(list=[1, 2, 3])
    assert len(result_list) == 2 and item in [1, 2, 3]

    # Empty list case
    assert node.pop_random_element(list=[]) == ([], None)


def test_first():
    node = DataListFirst()
    assert node.get_first_element(list=[1, 2, 3]) == (1,)
    assert node.get_first_element(list=["a", "b", "c"]) == ("a",)
    assert node.get_first_element(list=[]) == (None,)  # Empty list


def test_last():
    node = DataListLast()
    assert node.get_last_element(list=[1, 2, 3]) == (3,)
    assert node.get_last_element(list=["a", "b", "c"]) == ("c",)
    assert node.get_last_element(list=[]) == (None,)  # Empty list

