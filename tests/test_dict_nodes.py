#import pytest
from src.basic_data_handling.dict_nodes import (
    DictCreate,
    DictCreateFromItems,
    DictGet,
    DictSet,
    DictKeys,
    DictValues,
    DictItems,
    DictContainsKey,
    DictClear,
    DictCopy,
    DictFromKeys,
    DictPop,
    DictPopItem,
    DictSetDefault,
    DictUpdate,
    DictLength,
    DictMerge,
    DictGetKeysValues,
    DictRemove,
    DictFilterByKeys,
    DictExcludeKeys,
    DictGetMultiple,
    DictInvert,
    DictCreateFromLists,
    DictCompare,
    AnyToDict,
)

def test_dict_create():
    node = DictCreate()
    assert node.create() == ({},)  # Creates an empty dictionary


def test_dict_create_from_items():
    node = DictCreateFromItems()
    items = [("key1", "value1"), ("key2", "value2")]
    assert node.create_from_items(items) == ({"key1": "value1", "key2": "value2"},)


def test_dict_get():
    node = DictGet()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.get(my_dict, "key1") == ("value1",)
    assert node.get(my_dict, "key3", default="default_value") == ("default_value",)


def test_dict_set():
    node = DictSet()
    my_dict = {"key1": "value1"}
    assert node.set(my_dict, "key2", "value2") == ({"key1": "value1", "key2": "value2"},)


def test_dict_keys():
    node = DictKeys()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.keys(my_dict) == (["key1", "key2"],)


def test_dict_values():
    node = DictValues()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.values(my_dict) == (["value1", "value2"],)


def test_dict_items():
    node = DictItems()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.items(my_dict) == ([("key1", "value1"), ("key2", "value2")],)


def test_dict_contains_key():
    node = DictContainsKey()
    my_dict = {"key1": "value1"}
    assert node.contains_key(my_dict, "key1") == (True,)
    assert node.contains_key(my_dict, "key2") == (False,)


def test_dict_clear():
    node = DictClear()
    my_dict = {"key1": "value1"}
    assert node.clear(my_dict) == ({},)


def test_dict_copy():
    node = DictCopy()
    my_dict = {"key1": "value1"}
    assert node.copy(my_dict) == ({"key1": "value1"},)


def test_dict_from_keys():
    node = DictFromKeys()
    keys = ["key1", "key2"]
    assert node.from_keys(keys, value="value") == ({"key1": "value", "key2": "value"},)


def test_dict_pop():
    node = DictPop()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.pop(my_dict, "key1") == ({"key2": "value2"}, "value1")


def test_dict_pop_item():
    node = DictPopItem()
    my_dict = {"key1": "value1"}
    assert node.popitem(my_dict) == ({}, "key1", "value1", True)
    assert node.popitem({}) == ({}, "", None, False)


def test_dict_set_default():
    node = DictSetDefault()
    my_dict = {"key1": "value1"}
    assert node.setdefault(my_dict, "key2", "default") == ({"key1": "value1", "key2": "default"}, "default")


def test_dict_update():
    node = DictUpdate()
    my_dict = {"key1": "value1"}
    update_dict = {"key2": "value2"}
    assert node.update(my_dict, update_dict) == ({"key1": "value1", "key2": "value2"},)


def test_dict_length():
    node = DictLength()
    my_dict = {"key1": "value1"}
    assert node.length(my_dict) == (1,)


def test_dict_merge():
    node = DictMerge()
    dict1 = {"key1": "value1"}
    dict2 = {"key2": "value2"}
    assert node.merge(dict1, dict2) == ({"key1": "value1", "key2": "value2"},)


def test_dict_get_keys_values():
    node = DictGetKeysValues()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.get_keys_values(my_dict) == (["key1", "key2"], ["value1", "value2"])


def test_dict_remove():
    node = DictRemove()
    my_dict = {"key1": "value1"}
    assert node.remove(my_dict, "key1") == ({}, True)


def test_dict_filter_by_keys():
    node = DictFilterByKeys()
    my_dict = {"key1": "value1", "key2": "value2"}
    keys = ["key1"]
    assert node.filter_by_keys(my_dict, keys) == ({"key1": "value1"},)


def test_dict_exclude_keys():
    node = DictExcludeKeys()
    my_dict = {"key1": "value1", "key2": "value2"}
    keys = ["key1"]
    assert node.exclude_keys(my_dict, keys) == ({"key2": "value2"},)


def test_dict_get_multiple():
    node = DictGetMultiple()
    my_dict = {"key1": "value1", "key2": "value2"}
    keys = ["key1", "key3"]
    assert node.get_multiple(my_dict, keys, default="default") == (["value1", "default"],)


def test_dict_invert():
    node = DictInvert()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.invert(my_dict) == ({"value1": "key1", "value2": "key2"}, True)


def test_dict_create_from_lists():
    node = DictCreateFromLists()
    keys = ["key1", "key2"]
    values = ["value1", "value2"]
    assert node.create_from_lists(keys, values) == ({"key1": "value1", "key2": "value2"},)


def test_dict_compare():
    node = DictCompare()
    dict1 = {"key1": "value1"}
    dict2 = {"key1": "value1"}
    assert node.compare(dict1, dict2) == (True, [], [], [])


def test_any_to_dict():
    node = AnyToDict()
    my_dict = {"key1": "value1"}
    assert node.convert(my_dict) == ({"key1": "value1"},)
