from frozendict import frozendict
import pytest
from src.basic_data_handling.dict_nodes import (
    DictCompare,
    DictContainsKey,
    DictCreate,
    DictCreateFromBoolean,
    DictCreateFromFloat,
    DictCreateFromInt,
    DictCreateFromItemsDataList,
    DictCreateFromItemsList,
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


# frozendict - as an example of not-a-dict-subclass-yet-mapping class:
_tested_dict_types = (dict, frozendict)

_dict_x1 = {"key1": "value1"}
_dict_x2 = {"key1": "value1", "key2": "value2"}
_dict_x3 = {"key1": "value1", "key2": "value2", "key3": "value3"}
_dict_b = {"key2": "value2"}


def test_dict_create():
    node = DictCreate()
    assert node.create() == ({},)  # Creates an empty dictionary


@pytest.mark.parametrize(
    "in_dict, key, default, expected, message", [
        (_dict_x3, "key1", None, "value1", "existing key"),
        (_dict_x3, "non_existent", None, None, "missing key, no default"),
        (_dict_x3, "key99", "default_value", "default_value", "missing key with default"),
    ]
)
@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_get(dict_type, in_dict, key, default, expected, message):
    node = DictGet()
    my_dict = dict_type(in_dict)
    assert node.get(my_dict, key, default=default) == (expected,), f"Wrong result: {message}"


@pytest.mark.parametrize(
    "in_dict, key, value, expected, message", [
        (_dict_x1, "key2", "value2", _dict_x2, "base case"),
        (_dict_x1, "key1", "new_value", {"key1": "new_value"}, "overwriting existing key"),
        ({}, "key", "value", {"key": "value"}, "empty dict"),
    ]
)
@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_set(dict_type, in_dict, key, value, expected, message):
    node = DictSet()
    my_dict = dict_type(in_dict)
    result = node.set(my_dict, key, value)
    assert result == (dict_type(expected),), f"Wrong result: {message}"
    assert type(result[0]) == dict_type, f"Wrong type: {message}"

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
    assert result == (_dict_x2,)
    # Test with empty inputs
    assert node.create() == ({},)


def test_dict_create_from_items_datalist():
    node = DictCreateFromItemsDataList()
    assert node.create_from_items(item=[("key1", "value1"), ("key2", "value2")]) == (_dict_x2,)
    with pytest.raises(ValueError):
        node.create_from_items(item=[("key1", "value1", "extra")])


def test_dict_create_from_items_list():
    node = DictCreateFromItemsList()
    assert node.create_from_items(items=[("key1", "value1"), ("key2", "value2")]) == (_dict_x2,)
    with pytest.raises(ValueError):
        node.create_from_items(items=[("key1", "value1", "extra")])


@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_pop_random(dict_type):
    node = DictPopRandom()
    # Test with non-empty dictionary
    my_dict = dict_type(_dict_x2)
    result_dict, key, value, success = node.pop_random(my_dict)

    # Check that operation was successful
    assert success is True
    # Check that one item was removed
    assert len(result_dict) == len(my_dict) - 1
    # Check that removed key is not in result dict
    assert key not in result_dict
    assert type(result_dict) == dict_type
    # Check that the original key-value pair matches
    assert my_dict[key] == value

    # Test with empty dictionary
    empty_result_dict, empty_key, empty_value, empty_success = node.pop_random(dict_type({}))
    assert empty_result_dict == dict_type({})
    assert type(empty_result_dict) == dict_type
    assert empty_key == ""
    assert empty_value is None
    assert empty_success is False

    # Same seed should produce the same popped key/value
    result1 = node.pop_random(my_dict, seed=42)
    result2 = node.pop_random(my_dict, seed=42)
    assert result1 == result2


@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_keys(dict_type):
    node = DictKeys()
    my_dict = dict_type(_dict_x2)
    assert node.keys(my_dict) == (["key1", "key2"],)
    # Test with empty dict
    assert node.keys(dict_type({})) == ([],)


@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_values(dict_type):
    node = DictValues()
    assert node.values(dict_type(_dict_x2)) == (["value1", "value2"],)
    # Test with empty dict
    assert node.values(dict_type({})) == ([],)


@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_items(dict_type):
    node = DictItems()
    my_dict = dict_type(_dict_x2)
    # Note that the order might not be preserved, so we check if items are in the result
    items = node.items(my_dict)[0]
    assert len(items) == 2
    assert ("key1", "value1") in items
    assert ("key2", "value2") in items
    # Test with empty dict
    assert node.items(dict_type({})) == ([],)


@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_contains_key(dict_type):
    node = DictContainsKey()
    my_dict = dict_type(_dict_x1)
    assert node.contains_key(my_dict, "key1") == (True,)
    assert node.contains_key(my_dict, "key2") == (False,)
    # Test with empty dict
    assert node.contains_key(dict_type({}), "any_key") == (False,)


def test_dict_from_keys():
    node = DictFromKeys()
    keys = ["key1", "key2"]
    assert node.from_keys(keys, value="value") == ({"key1": "value", "key2": "value"},)
    # Test without value (should use None)
    assert node.from_keys(keys) == ({"key1": None, "key2": None},)
    # Test with empty keys list
    assert node.from_keys([]) == ({},)


@pytest.mark.parametrize(
    "in_dict, key, default, out_dict, pop_value, message", [
        (_dict_x2, "key1", None, _dict_b, "value1", "base case"),
        (_dict_x2, "non_existent", "default", _dict_x2, "default", "non-existent key (with default)"),
        ({"a": 1}, "b", None, {"a": 1}, None, "non-existent key (no default)"),
        ({}, "key", None, {}, None, "empty dict"),
    ]
)
@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_pop(dict_type, in_dict, key, default, out_dict, pop_value, message):
    node = DictPop()
    my_dict = dict_type(in_dict)
    result = node.pop(my_dict, key, default_value=default)
    assert result == (dict_type(out_dict), pop_value), f"Wrong result: {message}"
    assert type(result[0]) == dict_type, f"Wrong type: {message}"


@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_pop_item(dict_type):
    node = DictPopItem()
    my_dict = dict_type(_dict_x1)
    result = node.popitem(my_dict)
    # Since we only have one item, we know what should be popped
    assert result[0] == dict_type({})  # remaining dict is empty
    assert type(result[0]) == dict_type
    assert result[1] == "key1"  # popped key
    assert result[2] == "value1"  # popped value
    assert result[3] is True  # success
    # Test with empty dict
    assert node.popitem({}) == ({}, "", None, False)


@pytest.mark.parametrize(
    "in_dict, key, default, out_dict, out_value, message", [
        (_dict_x1, "key2", "default", {"key1": "value1", "key2": "default"}, "default", "key that doesn't exist"),
        (_dict_x1, "key1", "new_default", _dict_x1, "value1", "key that already exists"),
        ({}, "key", "value", {"key": "value"}, "value", "empty dict"),
    ]
)
@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_set_default(dict_type, in_dict, key, default, out_dict, out_value, message):
    node = DictSetDefault()
    my_dict = dict_type(in_dict)
    result = node.setdefault(my_dict, key, default)
    assert result == (dict_type(out_dict), out_value), f"Wrong result: {message}"
    assert type(result[0]) == dict_type, f"Wrong type: {message}"


@pytest.mark.parametrize(
    "in_dict, update_dict, expected, message", [
        (_dict_x1, _dict_b, _dict_x2, "base case"),
        ({"a": 1, "b": 2}, {"b": 3, "c": 4}, {"a": 1, "b": 3, "c": 4}, "overlapping keys"),
        (_dict_x1, {}, _dict_x1, "empty update dict"),
        ({}, _dict_b, _dict_b, "empty original dict"),
    ]
)
@pytest.mark.parametrize("update_type", _tested_dict_types)
@pytest.mark.parametrize("in_type", _tested_dict_types)
def test_dict_update(in_type, update_type, in_dict, update_dict, expected, message):
    node = DictUpdate()
    result = node.update(in_type(in_dict), update_type(update_dict))
    assert result == (in_type(expected),), f"Wrong result: {message}"
    assert type(result[0]) == in_type, f"Wrong type: {message}"


@pytest.mark.parametrize("num", [0, 3, 6, 9, 12, 15])
@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_length(dict_type, num):
    node = DictLength()
    my_dict = dict_type({f"key{x}": f"value{x}" for x in range(1, num+1)})
    assert node.length(my_dict) == (num,)


@pytest.mark.parametrize(
    "dict_a, other_dicts, expected, message", [
        (_dict_x1, [_dict_b], _dict_x2, "basic merge"),
        ({"a": 1}, [{"a": 2}], {"a": 2}, "overlapping keys (later dicts override earlier ones)"),
        ({"a": 1}, [{"b": 2}, {"c": 3}], {"a": 1, "b": 2, "c": 3}, "more than two dicts"),
        ({}, [], {}, "empty dict - v1"),
        (_dict_x1, [], _dict_x1, "empty dict - v2"),
        (_dict_x1, [{}], _dict_x1, "empty dict - v3"),
        (_dict_x1, [{}, {}, {}], _dict_x1, "empty dict - v4"),
        ({}, [_dict_x1], _dict_x1, "empty dict - v5"),
        ({}, [_dict_x1, _dict_b], _dict_x2, "empty first dict"),
    ]
)
@pytest.mark.parametrize("type_b", _tested_dict_types)
@pytest.mark.parametrize("type_a", _tested_dict_types)
def test_dict_merge(type_a, type_b, dict_a, other_dicts, expected, message):
    node = DictMerge()
    dict1 = type_a(dict_a)
    dicts_extra = tuple(type_b(d) for d in other_dicts)
    result = node.merge(dict1, *dicts_extra)
    assert result == (type_a(expected),), f"Wrong result: {message}"
    assert type(result[0]) == type_a, f"Wrong type: {message}"


@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_get_keys_values(dict_type):
    node = DictGetKeysValues()
    my_dict = dict_type(_dict_x2)
    keys, values = node.get_keys_values(my_dict)
    # Check keys and values contents (order may vary)
    assert set(keys) == {"key1", "key2"}
    assert set(values) == {"value1", "value2"}
    # Test with empty dict
    assert node.get_keys_values(dict_type({})) == ([], [])


@pytest.mark.parametrize(
    "in_dict, key, expected, success, message", [
        (_dict_x2, "key1", _dict_b, True, "successful removal"),
        (_dict_x2, "non_existent", _dict_x2, False, "removal of non-existent key"),
        ({}, "any_key", {}, False, "empty dict"),
    ]
)
@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_remove(dict_type, in_dict, key, expected, success, message):
    node = DictRemove()
    my_dict = dict_type(in_dict)
    result = node.remove(my_dict, key)
    assert result == (dict_type(expected), success), f"Wrong result: {message}"
    assert type(result[0]) == dict_type, f"Wrong type: {message}"


@pytest.mark.parametrize(
    "in_dict, keys, expected, message", [
        (_dict_x3, ["key1", "key3"], {"key1": "value1", "key3": "value3"}, "subset of keys"),
        (_dict_x3, ["key1", "non_existent"], _dict_x1, "non-existent keys"),
        (_dict_x3, [], {}, "empty keys list"),
        (_dict_x3, list(_dict_x3.keys()), _dict_x3, "all keys"),
        ({}, ["any_key"], {}, "empty dict"),
    ]
)
@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_filter_by_keys(dict_type, in_dict, keys, expected, message):
    node = DictFilterByKeys()
    my_dict = dict_type(in_dict)
    result = node.filter_by_keys(my_dict, keys)
    assert result == (dict_type(expected),), f"Wrong result: {message}"
    assert type(result[0]) == dict_type, f"Wrong type: {message}"


@pytest.mark.parametrize(
    "in_dict, keys, expected, message", [
        (_dict_x3, ["key1", "key3"], _dict_b, "excluding some keys"),
        (_dict_x3, list(_dict_x3.keys()), {}, "excluding all keys"),
        (_dict_x3, ["non_existent"], _dict_x3, "excluding non-existent keys"),
        (_dict_x3, [], _dict_x3, "empty exclude list"),
        ({}, ["any_key"], {}, "empty dict"),
    ]
)
@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_exclude_keys(dict_type, in_dict, keys, expected, message):
    node = DictExcludeKeys()
    my_dict = dict_type(in_dict)
    result = node.exclude_keys(my_dict, keys)
    assert result == (dict_type(expected),), f"Wrong result: {message}"
    assert type(result[0]) == dict_type, f"Wrong type: {message}"


@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_get_multiple(dict_type):
    node = DictGetMultiple()
    my_dict = dict_type(_dict_x2)
    # Test getting existing keys
    assert node.get_multiple(my_dict, ["key1", "key2"]) == (["value1", "value2"],)
    # Test with mix of existing and non-existent keys
    assert node.get_multiple(my_dict, ["key1", "key3"], default="default") == (["value1", "default"],)
    # Test with only non-existent keys
    assert node.get_multiple(my_dict, ["key3", "key4"], default="default") == (["default", "default"],)
    # Test with empty keys list
    assert node.get_multiple(my_dict, []) == ([],)
    # Test with empty dict
    assert node.get_multiple(dict_type({}), ["key1"], default="default") == (["default"],)


@pytest.mark.parametrize(
    "in_dict, out_dict, success, message", [
        (_dict_x2, {"value1": "key1", "value2": "key2"}, True, "basic inversion"),
        ({"key1": "value", "key2": "value"}, {"value": "key2"}, True, "duplicated values - last key wins"),
        ({}, {}, True, "empty dict"),
        # TODO: `False` success
    ]
)
@pytest.mark.parametrize("dict_type", _tested_dict_types)
def test_dict_invert(dict_type, in_dict, out_dict, success, message):
    node = DictInvert()
    result = node.invert(dict_type(in_dict))
    assert result == (dict_type(out_dict), success), f"Wrong result: {message}"
    assert type(result[0]) == dict_type, f"Wrong type: {message}"


def test_dict_invert_unhashable_values():
    node = DictInvert()
    my_dict = {"key1": [1], "key2": [2]}
    result, success = node.invert(my_dict)
    assert result == my_dict
    assert success is False


def test_dict_create_from_lists():
    node = DictCreateFromLists()
    keys = ["key1", "key2", "key3"]
    values = ["value1", "value2", "value3"]
    # Test with matching length lists
    assert node.create_from_lists(keys, values) == (_dict_x3,)
    # Test with more keys than values
    assert node.create_from_lists(keys, ["value1", "value2"]) == (_dict_x2,)
    # Test with more values than keys
    assert node.create_from_lists(["key1", "key2"], values) == (_dict_x2,)
    # Test with empty lists
    assert node.create_from_lists([], []) == ({},)


@pytest.mark.parametrize("b_type", _tested_dict_types)
@pytest.mark.parametrize("a_type", _tested_dict_types)
def test_dict_compare(a_type, b_type):
    node = DictCompare()
    # Test identical dictionaries
    dict_a = a_type(_dict_x2)
    dict_b = b_type(_dict_x2)
    assert node.compare(dict_a, dict_b) == (True, [], [], [])

    # Test dictionaries with different values
    dict_b = b_type({"key1": "value1", "key2": "different"})
    are_equal, only_in_1, only_in_2, diff_values = node.compare(dict_a, dict_b)
    assert are_equal is False
    assert only_in_1 == []
    assert only_in_2 == []
    assert "key2" in diff_values

    # Test dictionaries with different keys
    dict_b = b_type({"key1": "value1", "key3": "value3"})
    are_equal, only_in_1, only_in_2, diff_values = node.compare(dict_a, dict_b)
    assert are_equal is False
    assert "key2" in only_in_1
    assert "key3" in only_in_2
    assert diff_values == []

    # Test empty dictionaries
    assert node.compare(a_type({}), b_type({})) == (True, [], [], [])
