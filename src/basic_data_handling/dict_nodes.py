from typing import Any
from inspect import cleandoc

try:
    from comfy.comfy_types.node_typing import IO, ComfyNodeABC
except:
    class IO:
        BOOLEAN = "BOOLEAN"
        INT = "INT"
        FLOAT = "FLOAT"
        STRING = "STRING"
        NUMBER = "FLOAT,INT"
        ANY = "*"
    ComfyNodeABC = object

from ._dynamic_input import ContainsDynamicDict


class DictCreate(ComfyNodeABC):
    """
    Creates a new empty dictionary.

    This node creates and returns a new empty dictionary object.
    """
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "key_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0}),
                "value_0": (IO.ANY, {"_dynamic": "number", "_dynamicGroup": 0}),
            })
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, **kwargs: list[Any]) -> tuple[dict]:
        result = {}
        # Process all key_X/value_X pairs from dynamic inputs
        for i in range(len(kwargs) // 2):  # Divide by 2 since we have key/value pairs
            key_name = f"key_{i}"
            value_name = f"value_{i}"
            if key_name in kwargs and value_name in kwargs:
                result[kwargs[key_name]] = kwargs[value_name]
        return (result,)


class DictCreateFromBoolean(ComfyNodeABC):
    """
    Creates a new empty dictionary.

    This node creates and returns a new empty dictionary object.
    """
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "key_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0}),
               "value_0": (IO.BOOLEAN, {"_dynamic": "number", "_dynamicGroup": 0}),
            })
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, **kwargs: list[Any]) -> tuple[dict]:
        result = {}
        # Process all key_X/value_X pairs from dynamic inputs
        for i in range(len(kwargs) // 2):  # Divide by 2 since we have key/value pairs
            key_name = f"key_{i}"
            value_name = f"value_{i}"
            if key_name in kwargs and value_name in kwargs:
                result[kwargs[key_name]] = bool(kwargs[value_name])
        return (result,)


class DictCreateFromFloat(ComfyNodeABC):
    """
    Creates a new empty dictionary.

    This node creates and returns a new empty dictionary object.
    """
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "key_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0}),
                "value_0": (IO.FLOAT, {"_dynamic": "number", "_dynamicGroup": 0}),
            })
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, **kwargs: list[Any]) -> tuple[dict]:
        result = {}
        # Process all key_X/value_X pairs from dynamic inputs
        for i in range(len(kwargs) // 2):  # Divide by 2 since we have key/value pairs
            key_name = f"key_{i}"
            value_name = f"value_{i}"
            if key_name in kwargs and value_name in kwargs:
                result[kwargs[key_name]] = float(kwargs[value_name])
        return (result,)


class DictCreateFromInt(ComfyNodeABC):
    """
    Creates a new empty dictionary.

    This node creates and returns a new empty dictionary object.
    """
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "key_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0}),
                "value_0": (IO.INT, {"_dynamic": "number", "_dynamicGroup": 0}),
            })
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, **kwargs: list[Any]) -> tuple[dict]:
        result = {}
        # Process all key_X/value_X pairs from dynamic inputs
        for i in range(len(kwargs) // 2):  # Divide by 2 since we have key/value pairs
            key_name = f"key_{i}"
            value_name = f"value_{i}"
            if key_name in kwargs and value_name in kwargs:
                result[kwargs[key_name]] = int(kwargs[value_name])
        return (result,)


class DictCreateFromString(ComfyNodeABC):
    """
    Creates a new empty dictionary.

    This node creates and returns a new empty dictionary object.
    """
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "key_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0}),
                "value_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0}),
            })
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, **kwargs: list[Any]) -> tuple[dict]:
        result = {}
        # Process all key_X/value_X pairs from dynamic inputs
        for i in range(len(kwargs) // 2):  # Divide by 2 since we have key/value pairs
            key_name = f"key_{i}"
            value_name = f"value_{i}"
            if key_name in kwargs and value_name in kwargs:
                result[kwargs[key_name]] = str(kwargs[value_name])
        return (result,)


class DictCreateFromItemsDataList(ComfyNodeABC):
    """
    Creates a dictionary from a list of key-value pairs.

    This node takes a list of key-value pairs (tuples) and builds a dictionary from them.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "item": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_from_items"
    INPUT_IS_LIST = True

    def create_from_items(self, **kwargs: list[Any]) -> tuple[dict]:
        try:
            # Check if items are valid (key-value pairs)
            items = kwargs.get('item', [])
            for item in items:
                print(f'item: "{item}", len(item): {len(item)}, items: "{items}", len(items): {len(items)}')
                if not isinstance(item, tuple) and len(item) != 2:
                    raise ValueError("Each item must be a (key, value) pair")

            return (dict(items),)
        except Exception as e:
            raise ValueError(f"Error creating dictionary from items: {str(e)}")


class DictCreateFromItemsList(ComfyNodeABC):
    """
    Creates a dictionary from a list of key-value pairs.

    This node takes a list of key-value pairs (tuples) and builds a dictionary from them.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "items": ("LIST", {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_from_items"

    def create_from_items(self, items: list) -> tuple[dict]:
        try:
            # Check if items are valid (key-value pairs)
            for item in items:
                print(f'item: "{item}", len(item): {len(item)}, items: "{items}", len(items): {len(items)}')
                if not isinstance(item, tuple) and len(item) != 2:
                    raise ValueError("Each item must be a (key, value) pair")

            return (dict(items),)
        except Exception as e:
            raise ValueError(f"Error creating dictionary from items: {str(e)}")


class DictCreateFromLists(ComfyNodeABC):
    """
    Creates a dictionary from separate lists of keys and values.

    This node takes a list of keys and a list of values, then creates a dictionary
    by pairing corresponding elements from each list. If the lists are of different
    lengths, only pairs up to the length of the shorter list are used.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "keys": ("LIST", {}),
                "values": ("LIST", {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_from_lists"

    def create_from_lists(self, keys: list, values: list) -> tuple[dict]:
        # Pair keys with values up to the length of the shorter list
        result = dict(zip(keys, values))
        return (result,)


class DictCompare(ComfyNodeABC):
    """
    Compares two dictionaries and reports differences.

    This node takes two dictionaries and compares them, returning information about
    their equality, any keys that exist in only one dictionary, and any keys with
    different values.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dict1": ("DICT", {}),
                "dict2": ("DICT", {}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN, "LIST", "LIST", "LIST")
    RETURN_NAMES = ("are_equal", "only_in_dict1", "only_in_dict2", "different_values")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, dict1: dict, dict2: dict) -> tuple[bool, list, list, list]:
        are_equal = (dict1 == dict2)

        keys1 = set(dict1.keys())
        keys2 = set(dict2.keys())

        only_in_dict1 = list(keys1 - keys2)
        only_in_dict2 = list(keys2 - keys1)

        different_values = []
        for key in keys1 & keys2:
            if dict1[key] != dict2[key]:
                different_values.append(key)

        return are_equal, only_in_dict1, only_in_dict2, different_values


class DictContainsKey(ComfyNodeABC):
    """
    Checks if a key exists in a dictionary.

    This node takes a dictionary and a key as inputs, then returns True if the key
    exists in the dictionary, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
                "key": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "contains_key"

    def contains_key(self, input_dict: dict, key: str) -> tuple[bool]:
        return (key in input_dict,)


class DictExcludeKeys(ComfyNodeABC):
    """
    Creates a new dictionary excluding the specified keys.

    This node takes a dictionary and a list of keys, then returns a new dictionary
    containing all key-value pairs except those with keys in the provided list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
                "keys_to_exclude": ("LIST", {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "exclude_keys"

    def exclude_keys(self, input_dict: dict, keys_to_exclude: list) -> tuple[dict]:
        result = {k: v for k, v in input_dict.items() if k not in keys_to_exclude}
        return (result,)


class DictFilterByKeys(ComfyNodeABC):
    """
    Creates a new dictionary with only the specified keys.

    This node takes a dictionary and a list of keys, then returns a new dictionary
    containing only the key-value pairs for the keys that exist in the original dictionary.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
                "keys": ("LIST", {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "filter_by_keys"

    def filter_by_keys(self, input_dict: dict, keys: list) -> tuple[dict]:
        result = {k: input_dict[k] for k in keys if k in input_dict}
        return (result,)


class DictFromKeys(ComfyNodeABC):
    """
    Creates a dictionary from a list of keys and a default value.

    This node takes a list of keys and an optional value, then creates a new
    dictionary where each key is associated with the value. If no value is
    provided, None is used.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "keys": ("LIST", {}),
            },
            "optional": {
                "value": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "from_keys"

    def from_keys(self, keys: list, value=None) -> tuple[dict]:
        return (dict.fromkeys(keys, value),)


class DictGet(ComfyNodeABC):
    """
    Retrieves a value from a dictionary using the specified key.

    This node gets the value for the specified key from a dictionary.
    If the key is not found and a default value is provided, that default is returned.
    Otherwise, it returns None.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
                "key": (IO.STRING, {"default": ""}),
            },
            "optional": {
                "default": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("value",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get"

    def get(self, input_dict: dict, key: str, default=None) -> tuple[Any]:
        return (input_dict.get(key, default),)


class DictGetKeysValues(ComfyNodeABC):
    """
    Returns keys and values as separate lists.

    This node takes a dictionary and returns two lists: one containing
    all keys and another containing all corresponding values.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("LIST", "LIST")
    RETURN_NAMES = ("keys", "values")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_keys_values"

    def get_keys_values(self, input_dict: dict) -> tuple[list, list]:
        keys = list(input_dict.keys())
        values = list(input_dict.values())
        return keys, values


class DictGetMultiple(ComfyNodeABC):
    """
    Retrieves multiple values from a dictionary using a list of keys.

    This node takes a dictionary and a list of keys, then returns a list
    containing the corresponding values. If a key is not found, the default
    value is used for that position.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
                "keys": ("LIST", {}),
            },
            "optional": {
                "default": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("values",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_multiple"

    def get_multiple(self, input_dict: dict, keys: list, default=None) -> tuple[list]:
        values = [input_dict.get(key, default) for key in keys]
        return (values,)


class DictInvert(ComfyNodeABC):
    """
    Creates a new dictionary with keys and values swapped.

    This node takes a dictionary as input and returns a new dictionary where
    the keys become values and values become keys. Note that values must be
    hashable to be used as keys in the new dictionary.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("DICT", IO.BOOLEAN)
    RETURN_NAMES = ("inverted_dict", "success")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "invert"

    def invert(self, input_dict: dict) -> tuple[dict, bool]:
        try:
            inverted = {v: k for k, v in input_dict.items()}
            return inverted, True
        except Exception:
            # Return original dictionary if inversion fails (e.g., unhashable values)
            return input_dict, False


class DictItems(ComfyNodeABC):
    """
    Returns all key-value pairs in a dictionary.

    This node takes a dictionary and returns a list of tuples, where each tuple
    contains a key-value pair from the dictionary.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "items"

    def items(self, input_dict: dict) -> tuple[list]:
        return (list(input_dict.items()),)


class DictKeys(ComfyNodeABC):
    """
    Returns all keys in a dictionary.

    This node takes a dictionary and returns a list containing all of its keys.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "keys"

    def keys(self, input_dict: dict) -> tuple[list]:
        return (list(input_dict.keys()),)


class DictLength(ComfyNodeABC):
    """
    Returns the number of key-value pairs in a dictionary.

    This node takes a dictionary as input and returns its length (number of items).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("length",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "length"

    def length(self, input_dict: dict) -> tuple[int]:
        return (len(input_dict),)


class DictMerge(ComfyNodeABC):
    """
    Merges multiple dictionaries into a single dictionary.

    This node takes multiple dictionaries as input and combines them into a single
    dictionary. If there are duplicate keys, values from later dictionaries take precedence.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dict1": ("DICT", {}),
            },
            "optional": {
                "dict2": ("DICT", {}),
                "dict3": ("DICT", {}),
                "dict4": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "merge"

    def merge(self, dict1: dict, dict2=None, dict3=None, dict4=None) -> tuple[dict]:
        result = dict1.copy()

        if dict2 is not None:
            result.update(dict2)

        if dict3 is not None:
            result.update(dict3)

        if dict4 is not None:
            result.update(dict4)

        return (result,)


class DictPop(ComfyNodeABC):
    """
    Removes and returns a key-value pair from a dictionary.

    This node takes a dictionary and a key as inputs, removes the specified key
    from the dictionary, and returns both the modified dictionary and the value
    associated with the key. If the key is not found and a default value is provided,
    that default is returned. Otherwise, an error is raised.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
                "key": (IO.STRING, {"default": ""}),
            },
            "optional": {
                "default_value": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("DICT", IO.ANY)
    RETURN_NAMES = ("dict", "value")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop"

    def pop(self, input_dict: dict, key: str, default_value=None) -> tuple[dict, Any]:
        result = input_dict.copy()

        try:
            if key in result:
                value = result.pop(key)
                return result, value
            else:
                return result, default_value
        except Exception as e:
            raise ValueError(f"Error popping key from dictionary: {str(e)}")


class DictPopItem(ComfyNodeABC):
    """
    Removes and returns an arbitrary key-value pair from a dictionary.

    This node takes a dictionary as input, removes an arbitrary key-value pair,
    and returns the modified dictionary along with the removed key and value.
    If the dictionary is empty, returns an error.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("DICT", IO.STRING, IO.ANY, IO.BOOLEAN)
    RETURN_NAMES = ("dict", "key", "value", "success")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "popitem"

    def popitem(self, input_dict: dict) -> tuple[dict, str, Any, bool]:
        result = input_dict.copy()
        try:
            if result:
                key, value = result.popitem()
                return result, key, value, True
            else:
                return result, "", None, False
        except:
            return result, "", None, False


class DictPopRandom(ComfyNodeABC):
    """
    Removes and returns a random key-value pair from a dictionary.

    This node takes a dictionary as input, removes a random key-value pair,
    and returns the modified dictionary along with the removed key and value.
    If the dictionary is empty, it returns empty values.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("DICT", IO.STRING, IO.ANY, IO.BOOLEAN)
    RETURN_NAMES = ("dict", "key", "value", "success")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop_random"

    def pop_random(self, input_dict: dict) -> tuple[dict, str, Any, bool]:
        import random
        result = input_dict.copy()
        try:
            if result:
                random_key = random.choice(list(result.keys()))
                random_value = result.pop(random_key)
                return result, random_key, random_value, True
            else:
                return result, "", None, False
        except:
            return result, "", None, False


class DictRemove(ComfyNodeABC):
    """
    Removes a key-value pair from a dictionary.

    This node takes a dictionary and a key as inputs, then returns a new
    dictionary with the specified key removed. If the key doesn't exist,
    the dictionary remains unchanged.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
                "key": (IO.STRING, {"default": ""}),
            }
        }

    RETURN_TYPES = ("DICT", IO.BOOLEAN)
    RETURN_NAMES = ("dict", "key_removed")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "remove"

    def remove(self, input_dict: dict, key: str) -> tuple[dict, bool]:
        result = input_dict.copy()
        if key in result:
            del result[key]
            return result, True
        return result, False


class DictSet(ComfyNodeABC):
    """
    Adds or updates a key-value pair in a dictionary.

    This node takes a dictionary, key, and value as inputs, then returns
    a modified dictionary with the new key-value pair.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
                "key": (IO.STRING, {"default": ""}),
                "value": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "set"

    def set(self, input_dict: dict, key: str, value: Any) -> tuple[dict]:
        result = input_dict.copy()
        result[key] = value
        return (result,)


class DictSetDefault(ComfyNodeABC):
    """
    Returns the value for a key, setting a default if the key doesn't exist.

    This node takes a dictionary, a key, and a default value. If the key exists
    in the dictionary, the corresponding value is returned. If the key doesn't
    exist, the default value is inserted for the key and returned.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
                "key": (IO.STRING, {"default": ""}),
                "default_value": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("DICT", IO.ANY)
    RETURN_NAMES = ("DICT", "value")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "setdefault"

    def setdefault(self, input_dict: dict, key: str, default_value=None) -> tuple[dict, Any]:
        result = input_dict.copy()
        value = result.setdefault(key, default_value)
        return result, value


class DictUpdate(ComfyNodeABC):
    """
    Updates a dictionary with key-value pairs from another dictionary.

    This node takes two dictionaries as inputs and returns a new dictionary that
    contains all key-value pairs from both dictionaries. If there are duplicate
    keys, the values from the second dictionary take precedence.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dict1": ("DICT", {}),
                "dict2": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "update"

    def update(self, dict1: dict, dict2: dict) -> tuple[dict]:
        result = dict1.copy()
        result.update(dict2)
        return (result,)


class DictValues(ComfyNodeABC):
    """
    Returns all values in a dictionary.

    This node takes a dictionary and returns a list containing all of its values.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "values"

    def values(self, input_dict: dict) -> tuple[list]:
        return (list(input_dict.values()),)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: DictCreate": DictCreate,
    "Basic data handling: DictCreateFromBoolean": DictCreateFromBoolean,
    "Basic data handling: DictCreateFromFloat": DictCreateFromFloat,
    "Basic data handling: DictCreateFromInt": DictCreateFromInt,
    "Basic data handling: DictCreateFromString": DictCreateFromString,
    "Basic data handling: DictCreateFromItemsDataList": DictCreateFromItemsDataList,
    "Basic data handling: DictCreateFromItemsList": DictCreateFromItemsList,
    "Basic data handling: DictCreateFromLists": DictCreateFromLists,
    "Basic data handling: DictCompare": DictCompare,
    "Basic data handling: DictContainsKey": DictContainsKey,
    "Basic data handling: DictExcludeKeys": DictExcludeKeys,
    "Basic data handling: DictFilterByKeys": DictFilterByKeys,
    "Basic data handling: DictFromKeys": DictFromKeys,
    "Basic data handling: DictGet": DictGet,
    "Basic data handling: DictGetKeysValues": DictGetKeysValues,
    "Basic data handling: DictGetMultiple": DictGetMultiple,
    "Basic data handling: DictInvert": DictInvert,
    "Basic data handling: DictItems": DictItems,
    "Basic data handling: DictKeys": DictKeys,
    "Basic data handling: DictLength": DictLength,
    "Basic data handling: DictMerge": DictMerge,
    "Basic data handling: DictPop": DictPop,
    "Basic data handling: DictPopItem": DictPopItem,
    "Basic data handling: DictPopRandom": DictPopRandom,
    "Basic data handling: DictRemove": DictRemove,
    "Basic data handling: DictSet": DictSet,
    "Basic data handling: DictSetDefault": DictSetDefault,
    "Basic data handling: DictUpdate": DictUpdate,
    "Basic data handling: DictValues": DictValues,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: DictCreate": "create DICT",
    "Basic data handling: DictCreateFromBoolean": "create DICT from BOOLEANs",
    "Basic data handling: DictCreateFromFloat": "create DICT from FLOATs",
    "Basic data handling: DictCreateFromInt": "create DICT from INTs",
    "Basic data handling: DictCreateFromString": "create DICT from STRINGs",
    "Basic data handling: DictCreateFromItemsDataList": "create from items (data list)",
    "Basic data handling: DictCreateFromItemsList": "create from items (LIST)",
    "Basic data handling: DictCreateFromLists": "create from LISTs",
    "Basic data handling: DictCompare": "compare",
    "Basic data handling: DictContainsKey": "contains key",
    "Basic data handling: DictExcludeKeys": "exclude keys",
    "Basic data handling: DictFilterByKeys": "filter by keys",
    "Basic data handling: DictFromKeys": "from keys",
    "Basic data handling: DictGet": "get",
    "Basic data handling: DictGetKeysValues": "get keys values",
    "Basic data handling: DictGetMultiple": "get multiple",
    "Basic data handling: DictInvert": "invert",
    "Basic data handling: DictItems": "items",
    "Basic data handling: DictKeys": "keys",
    "Basic data handling: DictLength": "length",
    "Basic data handling: DictMerge": "merge",
    "Basic data handling: DictPop": "pop",
    "Basic data handling: DictPopItem": "pop item",
    "Basic data handling: DictPopRandom": "pop random",
    "Basic data handling: DictRemove": "remove",
    "Basic data handling: DictSet": "set",
    "Basic data handling: DictSetDefault": "setdefault",
    "Basic data handling: DictUpdate": "update",
    "Basic data handling: DictValues": "values",
}
