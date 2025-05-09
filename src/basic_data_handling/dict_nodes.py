from typing import Any
from inspect import cleandoc

class DictCreate:
    """
    Creates a new empty dictionary.

    This node creates and returns a new empty dictionary object.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self) -> tuple[dict]:
        return ({},)


class DictCreateFromItems:
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
                if not isinstance(item, tuple) or len(item) != 2:
                    raise ValueError("Each item must be a (key, value) pair")

            return (dict(items),)
        except Exception as e:
            raise ValueError(f"Error creating dictionary from items: {str(e)}")


class DictGet:
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
                "key": ("STRING", {"default": ""}),
            },
            "optional": {
                "default_value": ("*", {}),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("value",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get"

    def get(self, input_dict: dict, key: str, default_value=None) -> tuple[Any]:
        return (input_dict.get(key, default_value),)


class DictSet:
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
                "key": ("STRING", {"default": ""}),
                "value": ("*", {}),
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


class DictKeys:
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


class DictValues:
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


class DictItems:
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


class DictContainsKey:
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
                "key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "contains_key"

    def contains_key(self, input_dict: dict, key: str) -> tuple[bool]:
        return (key in input_dict,)


class DictClear:
    """
    Removes all items from a dictionary.

    This node takes a dictionary as input and returns a new empty dictionary.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "clear"

    def clear(self, input_dict: dict) -> tuple[dict]:
        return ({},)


class DictCopy:
    """
    Creates a shallow copy of a dictionary.

    This node takes a dictionary as input and returns a new dictionary that is
    a shallow copy of the original.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "copy"

    def copy(self, input_dict: dict) -> tuple[dict]:
        return (input_dict.copy(),)


class DictFromKeys:
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
                "value": ("*", {}),
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "from_keys"

    def from_keys(self, keys: list, value=None) -> tuple[dict]:
        return (dict.fromkeys(keys, value),)


class DictPop:
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
                "key": ("STRING", {"default": ""}),
            },
            "optional": {
                "default_value": ("*", {}),
                "has_default": (["False", "True"], {"default": "False"}),
            }
        }

    RETURN_TYPES = ("DICT", "*", "BOOLEAN")
    RETURN_NAMES = ("dict", "value", "key_found")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop"

    def pop(self, input_dict: dict, key: str, default_value=None, has_default: str = "False") -> tuple[dict, Any, bool]:
        result = input_dict.copy()
        has_default_bool = (has_default == "True")

        try:
            if key in result:
                value = result.pop(key)
                return result, value, True
            elif has_default_bool:
                return result, default_value, False
            else:
                raise KeyError(f"Key '{key}' not found in dictionary")
        except Exception as e:
            raise ValueError(f"Error popping key from dictionary: {str(e)}")


class DictPopItem:
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

    RETURN_TYPES = ("DICT", "STRING", "*", "BOOLEAN")
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


class DictSetDefault:
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
                "key": ("STRING", {"default": ""}),
                "default_value": ("*", {}),
            }
        }

    RETURN_TYPES = ("DICT", "*")
    RETURN_NAMES = ("dict", "value")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "setdefault"

    def setdefault(self, input_dict: dict, key: str, default_value=None) -> tuple[dict, Any]:
        result = input_dict.copy()
        value = result.setdefault(key, default_value)
        return result, value


class DictUpdate:
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


class DictLength:
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


class DictMerge:
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


class DictGetKeysValues:
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


class DictRemove:
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
                "key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("DICT", "BOOLEAN")
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


class DictFilterByKeys:
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


class DictExcludeKeys:
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


class DictGetMultiple:
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
                "default_value": ("*", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("values",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_multiple"

    def get_multiple(self, input_dict: dict, keys: list, default_value=None) -> tuple[list]:
        values = [input_dict.get(key, default_value) for key in keys]
        return (values,)


class DictInvert:
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

    RETURN_TYPES = ("DICT", "BOOLEAN")
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


class DictCreateFromLists:
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


class DictCompare:
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

    RETURN_TYPES = ("BOOLEAN", "LIST", "LIST", "LIST")
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


class AnyToDict:
    """
    Converts compatible data structures to a dictionary.

    This node attempts to convert an input value to a dictionary. Compatible
    inputs include sequences of key-value pairs, mapping objects, and objects
    with a to_dict() or as_dict() method.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("*", {}),
            }
        }

    RETURN_TYPES = ("DICT", "BOOLEAN")
    RETURN_NAMES = ("dict", "success")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"

    def convert(self, input: Any) -> tuple[dict, bool]:
        try:
            if isinstance(input, dict):
                return input.copy(), True

            # Try converting from items
            if hasattr(input, "items"):
                return dict(input.items()), True

            # Try converting from sequence of pairs
            if hasattr(input, "__iter__") and not isinstance(input, str):
                try:
                    result = dict(input)
                    return result, True
                except (TypeError, ValueError):
                    pass

            # Check for to_dict or as_dict methods
            if hasattr(input, "to_dict") and callable(getattr(input, "to_dict")):
                return input.to_dict(), True

            if hasattr(input, "as_dict") and callable(getattr(input, "as_dict")):
                return input.as_dict(), True

            # Failed to convert
            return {}, False

        except Exception:
            return {}, False


NODE_CLASS_MAPPINGS = {
    "DictCreate": DictCreate,
    "DictCreateFromItems": DictCreateFromItems,
    "DictGet": DictGet,
    "DictSet": DictSet,
    "DictKeys": DictKeys,
    "DictValues": DictValues,
    "DictItems": DictItems,
    "DictContainsKey": DictContainsKey,
    "DictClear": DictClear,
    "DictCopy": DictCopy,
    "DictFromKeys": DictFromKeys,
    "DictPop": DictPop,
    "DictPopItem": DictPopItem,
    "DictSetDefault": DictSetDefault,
    "DictUpdate": DictUpdate,
    "DictLength": DictLength,
    "DictMerge": DictMerge,
    "DictGetKeysValues": DictGetKeysValues,
    "DictRemove": DictRemove,
    "DictFilterByKeys": DictFilterByKeys,
    "DictExcludeKeys": DictExcludeKeys,
    "DictGetMultiple": DictGetMultiple,
    "DictInvert": DictInvert,
    "DictCreateFromLists": DictCreateFromLists,
    "DictCompare": DictCompare,
    "AnyToDict": AnyToDict,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DictCreate": "create",
    "DictCreateFromItems": "from_items",
    "DictGet": "get",
    "DictSet": "set",
    "DictKeys": "keys",
    "DictValues": "values",
    "DictItems": "items",
    "DictContainsKey": "contains_key",
    "DictClear": "clear",
    "DictCopy": "copy",
    "DictFromKeys": "fromkeys",
    "DictPop": "pop",
    "DictPopItem": "popitem",
    "DictSetDefault": "setdefault",
    "DictUpdate": "update",
    "DictLength": "length",
    "DictMerge": "merge",
    "DictGetKeysValues": "get_keys_values",
    "DictRemove": "remove",
    "DictFilterByKeys": "filter_by_keys",
    "DictExcludeKeys": "exclude_keys",
    "DictGetMultiple": "get_multiple",
    "DictInvert": "invert",
    "DictCreateFromLists": "from_lists",
    "DictCompare": "compare",
    "AnyToDict": "any_to_DICT",
}
