#import pytest
from src.basic_data_handling.dict_nodes import (
    DictCompare,
    DictContainsKey,
    DictCreate,
    DictCreateFromBoolean,
    DictCreateFromFloat,
    DictCreateFromInt,
    DictCreateFromLists,
    DictCreateFromString,
    DictExcludeKeys,
    DictFilterByKeys,
    DictFromKeys,
    DictGet,
    DictGetKeysValues,
    DictGetMultiple,
    DictInvert,
    DictItems,
    DictKeys,
    DictLength,
    DictMerge,
    DictPop,
    DictPopItem,
    DictPopRandom,
    DictRemove,
    DictSet,
    DictSetDefault,
    DictUpdate,
    DictValues,
)

def test_dict_create():
    node = DictCreate()
    assert node.create() == ({},)  # Creates an empty dictionary


def test_dict_get():
    node = DictGet()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.get(my_dict, "key1") == ("value1",)
    assert node.get(my_dict, "key3", default="default_value") == ("default_value",)
    # Test with no default specified
    assert node.get(my_dict, "non_existent") == (None,)


def test_dict_set():
    node = DictSet()
    my_dict = {"key1": "value1"}
    assert node.set(my_dict, "key2", "value2") == ({"key1": "value1", "key2": "value2"},)
    # Test overwriting existing key
    assert node.set(my_dict, "key1", "new_value") == ({"key1": "new_value"},)
    # Test with empty dict
    assert node.set({}, "key", "value") == ({"key": "value"},)

def test_dict_create_from_boolean():
    node = DictCreateFromBoolean()
    # Test with dynamic inputs
    result = node.create(key_0="key1", value_0=True, key_1="key2", value_1=False, key_2="", value_2="")
    assert result == ({"key1": True, "key2": False},)
    # Test with empty inputs
    assert node.create() == ({},)


def test_dict_create_from_float():
    node = DictCreateFromFloat()
    # Test with dynamic inputs
    result = node.create(key_0="key1", value_0=1.5, key_1="key2", value_1=2.5, key_2="", value_2="")
    assert result == ({"key1": 1.5, "key2": 2.5},)
    # Test with empty inputs
    assert node.create() == ({},)


def test_dict_create_from_int():
    node = DictCreateFromInt()
    # Test with dynamic inputs
    result = node.create(key_0="key1", value_0=1, key_1="key2", value_1=2, key_2="", value_2="")
    assert result == ({"key1": 1, "key2": 2},)
    # Test with empty inputs
    assert node.create() == ({},)


def test_dict_create_from_string():
    node = DictCreateFromString()
    # Test with dynamic inputs
    result = node.create(key_0="key1", value_0="value1", key_1="key2", value_1="value2", key_2="", value_2="")
    assert result == ({"key1": "value1", "key2": "value2"},)
    # Test with empty inputs
    assert node.create() == ({},)


def test_dict_pop_random():
    node = DictPopRandom()
    # Test with non-empty dictionary
    my_dict = {"key1": "value1", "key2": "value2"}
    result_dict, key, value, success = node.pop_random(my_dict)

    # Check that operation was successful
    assert success is True
    # Check that one item was removed
    assert len(result_dict) == len(my_dict) - 1
    # Check that removed key is not in result dict
    assert key not in result_dict
    # Check that the original key-value pair matches
    assert my_dict[key] == value

    # Test with empty dictionary
    empty_result_dict, empty_key, empty_value, empty_success = node.pop_random({})
    assert empty_result_dict == {}
    assert empty_key == ""
    assert empty_value is None
    assert empty_success is False



def test_dict_keys():
    node = DictKeys()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.keys(my_dict) == (["key1", "key2"],)
    # Test with empty dict
    assert node.keys({}) == ([],)


def test_dict_values():
    node = DictValues()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.values(my_dict) == (["value1", "value2"],)
    # Test with empty dict
    assert node.values({}) == ([],)


def test_dict_items():
    node = DictItems()
    my_dict = {"key1": "value1", "key2": "value2"}
    # Note that the order might not be preserved, so we check if items are in the result
    items = node.items(my_dict)[0]
    assert len(items) == 2
    assert ("key1", "value1") in items
    assert ("key2", "value2") in items
    # Test with empty dict
    assert node.items({}) == ([],)


def test_dict_contains_key():
    node = DictContainsKey()
    my_dict = {"key1": "value1"}
    assert node.contains_key(my_dict, "key1") == (True,)
    assert node.contains_key(my_dict, "key2") == (False,)
    # Test with empty dict
    assert node.contains_key({}, "any_key") == (False,)


def test_dict_from_keys():
    node = DictFromKeys()
    keys = ["key1", "key2"]
    assert node.from_keys(keys, value="value") == ({"key1": "value", "key2": "value"},)
    # Test without value (should use None)
    assert node.from_keys(keys) == ({"key1": None, "key2": None},)
    # Test with empty keys list
    assert node.from_keys([]) == ({},)


def test_dict_pop():
    node = DictPop()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.pop(my_dict, "key1") == ({"key2": "value2"}, "value1")
    # Test with default value for non-existent key
    assert node.pop(my_dict, "non_existent", default_value="default") == (my_dict, "default")
    # Test with no default for non-existent key - should not modify dict
    assert node.pop({"a": 1}, "b") == ({"a": 1}, None)


def test_dict_pop_item():
    node = DictPopItem()
    my_dict = {"key1": "value1"}
    result = node.popitem(my_dict)
    # Since we only have one item, we know what should be popped
    assert result[0] == {}  # remaining dict is empty
    assert result[1] == "key1"  # popped key
    assert result[2] == "value1"  # popped value
    assert result[3] is True  # success
    # Test with empty dict
    assert node.popitem({}) == ({}, "", None, False)


def test_dict_set_default():
    node = DictSetDefault()
    my_dict = {"key1": "value1"}
    # Test setting a key that doesn't exist
    assert node.setdefault(my_dict, "key2", "default") == ({"key1": "value1", "key2": "default"}, "default")
    # Test with a key that already exists
    assert node.setdefault(my_dict, "key1", "new_default") == ({"key1": "value1"}, "value1")
    # Test with empty dict
    assert node.setdefault({}, "key", "value") == ({"key": "value"}, "value")


def test_dict_update():
    node = DictUpdate()
    my_dict = {"key1": "value1"}
    update_dict = {"key2": "value2"}
    assert node.update(my_dict, update_dict) == ({"key1": "value1", "key2": "value2"},)
    # Test updating with overlapping keys
    assert node.update({"a": 1, "b": 2}, {"b": 3, "c": 4}) == ({"a": 1, "b": 3, "c": 4},)
    # Test with empty update dict
    assert node.update(my_dict, {}) == (my_dict,)
    # Test with empty original dict
    assert node.update({}, update_dict) == (update_dict,)


def test_dict_length():
    node = DictLength()
    my_dict = {"key1": "value1", "key2": "value2"}
    assert node.length(my_dict) == (2,)
    # Test with empty dict
    assert node.length({}) == (0,)


def test_dict_merge():
    node = DictMerge()
    dict1 = {"key1": "value1"}
    dict2 = {"key2": "value2"}
    # Test basic merge
    assert node.merge(dict1, dict2) == ({"key1": "value1", "key2": "value2"},)
    # Test with overlapping keys (later dicts override earlier ones)
    assert node.merge({"a": 1}, {"a": 2}) == ({"a": 2},)
    # Test with more than two dicts
    result = node.merge({"a": 1}, {"b": 2}, {"c": 3})
    assert result == ({"a": 1, "b": 2, "c": 3},)
    # Test with empty dicts
    assert node.merge(dict1, {}) == (dict1,)
    assert node.merge({}, dict1) == (dict1,)


def test_dict_get_keys_values():
    node = DictGetKeysValues()
    my_dict = {"key1": "value1", "key2": "value2"}
    keys, values = node.get_keys_values(my_dict)
    # Check keys and values contents (order may vary)
    assert set(keys) == {"key1", "key2"}
    assert set(values) == {"value1", "value2"}
    # Test with empty dict
    assert node.get_keys_values({}) == ([], [])


def test_dict_remove():
    node = DictRemove()
    my_dict = {"key1": "value1", "key2": "value2"}
    # Test successful removal
    assert node.remove(my_dict, "key1") == ({"key2": "value2"}, True)
    # Test removal of non-existent key
    assert node.remove(my_dict, "non_existent") == (my_dict, False)
    # Test with empty dict
    assert node.remove({}, "any_key") == ({}, False)


def test_dict_filter_by_keys():
    node = DictFilterByKeys()
    my_dict = {"key1": "value1", "key2": "value2", "key3": "value3"}
    # Test with subset of keys
    assert node.filter_by_keys(my_dict, ["key1", "key3"]) == ({"key1": "value1", "key3": "value3"},)
    # Test with non-existent keys
    assert node.filter_by_keys(my_dict, ["key1", "non_existent"]) == ({"key1": "value1"},)
    # Test with empty keys list
    assert node.filter_by_keys(my_dict, []) == ({},)
    # Test with empty dict
    assert node.filter_by_keys({}, ["any_key"]) == ({},)


def test_dict_exclude_keys():
    node = DictExcludeKeys()
    my_dict = {"key1": "value1", "key2": "value2", "key3": "value3"}
    # Test excluding some keys
    assert node.exclude_keys(my_dict, ["key1", "key3"]) == ({"key2": "value2"},)
    # Test excluding non-existent keys
    assert node.exclude_keys(my_dict, ["non_existent"]) == (my_dict,)
    # Test excluding all keys
    assert node.exclude_keys(my_dict, ["key1", "key2", "key3"]) == ({},)
    # Test with empty exclude list
    assert node.exclude_keys(my_dict, []) == (my_dict,)
    # Test with empty dict
    assert node.exclude_keys({}, ["any_key"]) == ({},)


def test_dict_get_multiple():
    node = DictGetMultiple()
    my_dict = {"key1": "value1", "key2": "value2"}
    # Test getting existing keys
    assert node.get_multiple(my_dict, ["key1", "key2"]) == (["value1", "value2"],)
    # Test with mix of existing and non-existent keys
    assert node.get_multiple(my_dict, ["key1", "key3"], default="default") == (["value1", "default"],)
    # Test with only non-existent keys
    assert node.get_multiple(my_dict, ["key3", "key4"], default="default") == (["default", "default"],)
    # Test with empty keys list
    assert node.get_multiple(my_dict, []) == ([],)
    # Test with empty dict
    assert node.get_multiple({}, ["key1"], default="default") == (["default"],)


def test_dict_invert():
    node = DictInvert()
    my_dict = {"key1": "value1", "key2": "value2"}
    # Test basic inversion
    assert node.invert(my_dict) == ({"value1": "key1", "value2": "key2"}, True)
    # Test with duplicated values
    result, success = node.invert({"key1": "value", "key2": "value"})
    # With duplicate values, the last key wins
    assert result == {"value": "key2"}
    assert success is True
    # Test with empty dict
    assert node.invert({}) == ({}, True)


def test_dict_create_from_lists():
    node = DictCreateFromLists()
    keys = ["key1", "key2", "key3"]
    values = ["value1", "value2", "value3"]
    # Test with matching length lists
    assert node.create_from_lists(keys, values) == ({"key1": "value1", "key2": "value2", "key3": "value3"},)
    # Test with more keys than values
    assert node.create_from_lists(keys, ["value1", "value2"]) == ({"key1": "value1", "key2": "value2"},)
    # Test with more values than keys
    assert node.create_from_lists(["key1", "key2"], values) == ({"key1": "value1", "key2": "value2"},)
    # Test with empty lists
    assert node.create_from_lists([], []) == ({},)


def test_dict_compare():
    node = DictCompare()
    # Test identical dictionaries
    dict1 = {"key1": "value1", "key2": "value2"}
    dict2 = {"key1": "value1", "key2": "value2"}
    assert node.compare(dict1, dict2) == (True, [], [], [])

    # Test dictionaries with different values
    dict3 = {"key1": "value1", "key2": "different"}
    are_equal, only_in_1, only_in_2, diff_values = node.compare(dict1, dict3)
    assert are_equal is False
    assert only_in_1 == []
    assert only_in_2 == []
    assert "key2" in diff_values

    # Test dictionaries with different keys
    dict4 = {"key1": "value1", "key3": "value3"}
    are_equal, only_in_1, only_in_2, diff_values = node.compare(dict1, dict4)
    assert are_equal is False
    assert "key2" in only_in_1
    assert "key3" in only_in_2
    assert diff_values == []

    # Test empty dictionaries
    assert node.compare({}, {}) == (True, [], [], [])
