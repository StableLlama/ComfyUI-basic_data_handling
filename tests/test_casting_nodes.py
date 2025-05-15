import pytest
from src.basic_data_handling.casting_nodes import (CastToString, CastToInt, CastToFloat, CastToBoolean,
                           CastToList, CastToSet, CastToDict)


def test_cast_to_string():
    node = CastToString()
    assert node.convert_to_string(123) == ("123",)
    assert node.convert_to_string(None) == ("None",)
    assert node.convert_to_string(True) == ("True",)
    assert node.convert_to_string("hello") == ("hello",)


def test_cast_to_int():
    node = CastToInt()
    assert node.convert_to_int("123") == (123,)
    assert node.convert_to_int(456) == (456,)
    with pytest.raises(ValueError):
        node.convert_to_int("abc")
    with pytest.raises(ValueError):
        node.convert_to_int(None)


def test_cast_to_float():
    node = CastToFloat()
    assert node.convert_to_float("123.45") == (123.45,)
    assert node.convert_to_float(67.89) == (67.89,)
    assert node.convert_to_float(123) == (123.0,)
    with pytest.raises(ValueError):
        node.convert_to_float("abc")
    with pytest.raises(ValueError):
        node.convert_to_float(None)


def test_cast_to_boolean():
    node = CastToBoolean()
    assert node.convert_to_boolean(0) == (False,)
    assert node.convert_to_boolean(1) == (True,)
    assert node.convert_to_boolean("") == (False,)
    assert node.convert_to_boolean("non_empty_string") == (True,)


def test_cast_to_list():
    node = CastToList()
    assert node.convert_to_list(123) == ([123],)
    assert node.convert_to_list([1, 2, 3]) == ([1, 2, 3],)
    assert node.convert_to_list("hello") == (["hello"],)
    assert node.convert_to_list(None) == ([None],)


def test_cast_to_set():
    node = CastToSet()
    assert node.convert_to_set(123) == ({123},)
    assert node.convert_to_set([1, 2, 2]) == ({1, 2},)
    assert node.convert_to_set("abc") == ({"abc"},)
    assert node.convert_to_set(None) == ({None},)


def test_cast_to_dict():
    node = CastToDict()
    assert node.convert_to_dict({"key": "value"}) == ({"key": "value"},)
    assert node.convert_to_dict([("key1", "value1"), ("key2", "value2")]) == ({"key1": "value1", "key2": "value2"},)
    with pytest.raises(ValueError):
        node.convert_to_dict(123)
    with pytest.raises(ValueError):
        node.convert_to_dict("string")
