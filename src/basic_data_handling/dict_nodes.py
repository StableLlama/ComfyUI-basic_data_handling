from typing import (
    Any, Dict, List, Mapping, Tuple, Type, TypeVar,
    Union as _U, Optional as _O
)

from inspect import cleandoc
import random

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


T = TypeVar('T')  # Any type.

KT = TypeVar('KT')  # Key type.
KT2 = TypeVar('KT2')
KT3 = TypeVar('KT3')
KT4 = TypeVar('KT4')

VT = TypeVar('VT')  # Value type.
VT2 = TypeVar('VT2')
VT3 = TypeVar('VT3')
VT4 = TypeVar('VT4')


def _output_dict_preserving_type(result: Dict[KT, VT], in_type: Type[Mapping]) -> _U[Dict[KT, VT], Mapping[KT, VT]]:
    """Internal function:
    try returning the output dict as an instance of the same class as input dict.
    """
    if in_type is dict:
        return result

    # Support other dict-like classes:
    # noinspection PyBroadException
    try:
        return in_type(result)
    except Exception:
        pass

    # noinspection PyBroadException
    try:
        return in_type(result.items())
    except Exception:
        return result


class DictCreate(ComfyNodeABC):
    """
    Creates a new empty dictionary.

    This node creates and returns a new empty dictionary object.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "key_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0, "widgetType": "STRING", "tooltip": "Key for a key-value pair. Connect more keys to add more pairs."}),
                "value_0": (IO.ANY, {"_dynamic": "number", "_dynamicGroup": 0, "widgetType": "STRING", "tooltip": "Value paired with the key of the same index."}),
            })
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("The created DICT.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, **kwargs: list[Any]) -> tuple[dict]:
        result = {}
        # Process all key_X/value_X pairs from dynamic inputs
        for i in range(len(kwargs) // 2 - 1):  # Divide by 2 since we have key/value pairs
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
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "key_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0, "widgetType": "STRING", "tooltip": "Key for a key-value pair. Connect more keys to add more pairs."}),
               "value_0": (IO.BOOLEAN, {"_dynamic": "number", "_dynamicGroup": 0, "widgetType": "STRING", "tooltip": "Boolean value paired with the key of the same index."}),
            })
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("The created DICT.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, **kwargs: list[Any]) -> tuple[dict]:
        result = {}
        # Process all key_X/value_X pairs from dynamic inputs
        for i in range(len(kwargs) // 2 - 1):  # Divide by 2 since we have key/value pairs
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
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "key_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0, "widgetType": "STRING", "tooltip": "Key for a key-value pair. Connect more keys to add more pairs."}),
                "value_0": (IO.FLOAT, {"_dynamic": "number", "_dynamicGroup": 0, "widgetType": "STRING", "tooltip": "Float value paired with the key of the same index."}),
            })
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("The created DICT.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, **kwargs: list[Any]) -> tuple[dict]:
        result = {}
        # Process all key_X/value_X pairs from dynamic inputs
        for i in range(len(kwargs) // 2 - 1):  # Divide by 2 since we have key/value pairs
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
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "key_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0, "widgetType": "STRING", "tooltip": "Key for a key-value pair. Connect more keys to add more pairs."}),
                "value_0": (IO.INT, {"_dynamic": "number", "_dynamicGroup": 0, "widgetType": "STRING", "tooltip": "Integer value paired with the key of the same index."}),
            })
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("The created DICT.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, **kwargs: list[Any]) -> tuple[dict]:
        result = {}
        # Process all key_X/value_X pairs from dynamic inputs
        for i in range(len(kwargs) // 2 - 1):  # Divide by 2 since we have key/value pairs
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
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "key_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0, "widgetType": "STRING", "tooltip": "Key for a key-value pair. Connect more keys to add more pairs."}),
                "value_0": (IO.STRING, {"_dynamic": "number", "_dynamicGroup": 0, "widgetType": "STRING", "tooltip": "String value paired with the key of the same index."}),
            })
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("The created DICT.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, **kwargs: list[Any]) -> tuple[dict]:
        result = {}
        # Process all key_X/value_X pairs from dynamic inputs
        for i in range(len(kwargs) // 2 - 1):  # Divide by 2 since we have key/value pairs
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
                "item": (IO.ANY, {"tooltip": "A data list of (key, value) pairs to build the DICT from."}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("The created DICT.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_from_items"
    INPUT_IS_LIST = True

    def create_from_items(self, **kwargs: list[Any]) -> tuple[dict]:
        try:
            # Check if items are valid (key-value pairs)
            items = kwargs.get('item', [])
            for item in items:
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
                "items": ("LIST", {"tooltip": "A LIST of (key, value) pairs to build the DICT from."}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("The created DICT.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_from_items"

    def create_from_items(self, items: list) -> tuple[dict]:
        try:
            # Check if items are valid (key-value pairs)
            for item in items:
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
                "keys": ("LIST", {"tooltip": "The keys of the DICT."}),
                "values": ("LIST", {"tooltip": "The values paired with the keys by position."}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("The DICT created by pairing the two lists (up to the shorter length).",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_from_lists"

    def create_from_lists(self, keys: List[KT], values: List[VT]) -> tuple[Dict[KT, VT]]:
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
                "dict1": ("DICT", {"tooltip": "First DICT to compare."}),
                "dict2": ("DICT", {"tooltip": "Second DICT to compare."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN, "LIST", "LIST", "LIST")
    RETURN_NAMES = ("are_equal", "only_in_dict1", "only_in_dict2", "different_values")
    OUTPUT_TOOLTIPS = ("True when the two DICTs are equal.", "Keys present only in the first DICT.", "Keys present only in the second DICT.", "Shared keys whose values differ.")
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
                "input_dict": ("DICT", {"tooltip": "The DICT to search."}),
                "key": (IO.STRING, {"default": "", "tooltip": "The key to look for."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("contains",)
    OUTPUT_TOOLTIPS = ("True when the key exists in the DICT.",)
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
                "input_dict": ("DICT", {"tooltip": "The DICT to copy from."}),
                "keys_to_exclude": ("LIST", {"tooltip": "Keys to drop from the result."}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("A new DICT without the excluded keys.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "exclude_keys"

    def exclude_keys(self, input_dict: Mapping[KT, VT], keys_to_exclude: list) -> tuple[Mapping[KT, VT]]:
        if not(input_dict and keys_to_exclude):
            return (input_dict,)

        # `in` check is faster with sets + remove duplicates:
        keys_to_exclude_set = set(keys_to_exclude)

        if len(input_dict) <= len(keys_to_exclude_set):
            # It's faster to rebuild the dict with filter.
            result = {
                k: v for k, v in input_dict.items()
                if k not in keys_to_exclude_set
            }
        else:
            # It's faster to duplicate the dict, then pop all the exclusions one-by-one.
            result = dict(input_dict)
            for key in keys_to_exclude_set:
                if key in result:
                    result.pop(key)

        if len(result) == len(input_dict):
            # No changes made
            return (input_dict,)

        result = _output_dict_preserving_type(result, type(input_dict))
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
                "input_dict": ("DICT", {"tooltip": "The DICT to filter."}),
                "keys": ("LIST", {"tooltip": "Keys to keep in the result."}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("A new DICT containing only the selected keys.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "filter_by_keys"

    def filter_by_keys(self, input_dict: Mapping[KT, VT], keys: list) -> tuple[Mapping[KT, VT]]:
        if not input_dict:
            return (input_dict,)
        if not keys:
            return (_output_dict_preserving_type({}, type(input_dict)),)

        # `in` check is faster with sets + remove duplicates:
        keys_set = set(keys)

        if len(keys_set) <= len(input_dict):
            # It's faster to iterate over preserved keys
            result = {
                k: input_dict[k] for k in keys_set
                if k in input_dict
            }
        else:
            # It's faster to iterate over the input dict items
            result = {
                k: v for k, v in input_dict.items()
                if k in keys_set
            }

        if len(result) == len(input_dict):
            # No changes made
            return (input_dict,)

        result = _output_dict_preserving_type(result, type(input_dict))
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
                "keys": ("LIST", {"tooltip": "The keys of the new DICT."}),
            },
            "optional": {
                "value": (IO.ANY, {"tooltip": "Default value assigned to every key (None when not provided)."}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("A DICT mapping each key to the given value.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "from_keys"

    def from_keys(self, keys: List[KT], value: VT = None) -> tuple[Dict[KT, VT]]:
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
                "input_dict": ("DICT", {"tooltip": "The DICT to read from."}),
                "key": (IO.STRING, {"default": "", "tooltip": "The key whose value is retrieved."}),
            },
            "optional": {
                "default": (IO.ANY, {"tooltip": "Value returned when the key is missing (None when not provided)."}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("value",)
    OUTPUT_TOOLTIPS = ("The value for the key, or the default when the key is absent.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get"

    def get(self, input_dict: Mapping[Any, VT], key: Any, default: T = None) -> tuple[_U[VT, T]]:
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
                "input_dict": ("DICT", {"tooltip": "The DICT to decompose."}),
            }
        }

    RETURN_TYPES = ("LIST", "LIST")
    RETURN_NAMES = ("keys", "values")
    OUTPUT_TOOLTIPS = ("All keys of the DICT.", "All values of the DICT, in the same order as the keys.")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_keys_values"

    def get_keys_values(self, input_dict: Mapping[KT, VT]) -> tuple[List[KT], List[VT]]:
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
                "input_dict": ("DICT", {"tooltip": "The DICT to read from."}),
                "keys": ("LIST", {"tooltip": "The keys whose values are retrieved."}),
            },
            "optional": {
                "default": (IO.ANY, {"tooltip": "Value used for keys that are missing (None when not provided)."}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("values",)
    OUTPUT_TOOLTIPS = ("The value for each requested key, using the default for missing keys.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_multiple"

    def get_multiple(
        self,
        input_dict: Mapping[Any, VT], keys: list, default: T = None
    ) -> tuple[List[_U[VT, T]]]:
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
                "input_dict": ("DICT", {"tooltip": "The DICT whose keys and values are swapped."}),
            }
        }

    RETURN_TYPES = ("DICT", IO.BOOLEAN)
    RETURN_NAMES = ("inverted_dict", "success")
    OUTPUT_TOOLTIPS = ("The DICT with keys and values swapped.", "True when the inversion succeeded (values were hashable).")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "invert"

    def invert(self, input_dict: Mapping[KT, VT]) -> tuple[Mapping[VT, KT], bool]:
        try:
            inverted = {v: k for k, v in input_dict.items()}
        except Exception:
            # Return original dictionary if inversion fails (e.g., unhashable values)
            return input_dict, False

        inverted = _output_dict_preserving_type(inverted, type(input_dict))
        return inverted, True


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
                "input_dict": ("DICT", {"tooltip": "The DICT to read."}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("items",)
    OUTPUT_TOOLTIPS = ("A LIST of (key, value) tuples, one per entry.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "items"

    def items(self, input_dict: Mapping[KT, VT]) -> tuple[List[Tuple[KT, VT]]]:
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
                "input_dict": ("DICT", {"tooltip": "The DICT to read."}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("keys",)
    OUTPUT_TOOLTIPS = ("A LIST of all keys in the DICT.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "keys"

    def keys(self, input_dict: Mapping[KT, Any]) -> tuple[List[KT]]:
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
                "input_dict": ("DICT", {"tooltip": "The DICT to measure."}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("length",)
    OUTPUT_TOOLTIPS = ("The number of key-value pairs in the DICT.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "length"

    def length(self, input_dict: Mapping) -> tuple[int]:
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
                "dict1": ("DICT", {"tooltip": "First DICT to merge."}),
            },
            "optional": {
                "dict2": ("DICT", {"tooltip": "Optional DICT to merge; its values win over dict1."}),
                "dict3": ("DICT", {"tooltip": "Optional DICT to merge; its values win over earlier ones."}),
                "dict4": ("DICT", {"tooltip": "Optional DICT to merge; its values win over earlier ones."}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("The merged DICT; later inputs take precedence on duplicate keys.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "merge"

    def merge(
        self,
        dict1: Mapping[KT, VT],
        dict2: Mapping[KT2, VT2] = None,
        dict3: Mapping[KT3, VT3] = None,
        dict4: Mapping[KT4, VT4] = None,
    ) -> tuple[Mapping[_U[KT, KT2, KT3, KT4], _U[VT, VT2, VT3, VT4]]]:
        extra_dicts = [x for x in (dict2, dict3, dict4) if x is not None]
        if not extra_dicts:
            return (dict1,)

        # dict1 might be something like `frozendict` or other immutable mapping class.
        # Thus, we shouldn't do `dict.copy()`,
        # we must explicitly construct a `dict` object:
        result = dict(dict1)
        for extra in extra_dicts:
            result.update(extra)

        result = _output_dict_preserving_type(result, type(dict1))
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
                "input_dict": ("DICT", {"tooltip": "The DICT to pop from."}),
                "key": (IO.STRING, {"default": "", "tooltip": "The key whose entry is removed."}),
            },
            "optional": {
                "default_value": (IO.ANY, {"tooltip": "Value returned when the key is absent (None when not provided)."}),
            }
        }

    RETURN_TYPES = ("DICT", IO.ANY)
    RETURN_NAMES = ("dict", "value")
    OUTPUT_TOOLTIPS = ("The DICT with the key removed.", "The removed value (or the default when the key was absent).")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop"

    def pop(self, input_dict: Mapping[KT, VT], key: Any, default_value: T = None) -> tuple[Mapping[KT, VT], _U[VT, T]]:
        if key not in input_dict:
            return input_dict, default_value

        # input_dict might be something like `frozendict` or other immutable mapping class.
        # Thus, we shouldn't do `dict.copy()`,
        # we must explicitly construct a `dict` object:
        result = dict(input_dict)
        try:
            value = result.pop(key)
        except Exception as e:
            raise ValueError(f"Error popping key from dictionary: {str(e)}")

        result = _output_dict_preserving_type(result, type(input_dict))
        return result, value


class DictPopItem(ComfyNodeABC):
    """
    Removes and returns an arbitrary key-value pair from a dictionary.

    This node takes a dictionary as input, removes an arbitrary key-value pair,
    and returns the modified dictionary along with the removed key and value.
    If operation fails, no error is thrown, but the last argument is `False`,
    and the dictionary is returned intact.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {"tooltip": "The DICT to pop an entry from."}),
            }
        }

    RETURN_TYPES = ("DICT", IO.STRING, IO.ANY, IO.BOOLEAN)
    RETURN_NAMES = ("dict", "key", "value", "success")
    OUTPUT_TOOLTIPS = ("The DICT with one entry removed.", "The removed key.", "The removed value.", "False when the DICT was empty or the operation failed.")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "popitem"

    def popitem(self, input_dict: Mapping[KT, VT]) -> tuple[Mapping[KT, VT], _U[KT, str], _O[VT], bool]:
        if not input_dict:
            return input_dict, "", None, False

        result = dict(input_dict)
        # noinspection PyBroadException
        try:
            key, value = result.popitem()
        except Exception:
            return input_dict, "", None, False

        result = _output_dict_preserving_type(result, type(input_dict))
        return result, key, value, True


class DictPopRandom(ComfyNodeABC):
    """
    Removes and returns a random key-value pair from a dictionary.

    This node takes a dictionary as input, removes a random key-value pair,
    and returns the modified dictionary along with the removed key and value.
    If the dictionary is empty, it returns empty values.
    An optional seed can be provided for reproducible selection.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": ("DICT", {"tooltip": "The DICT to pop a random entry from."}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": True, "tooltip": "Seed for reproducible selection. Leave empty to pick randomly each run."}),
            },
        }

    RETURN_TYPES = ("DICT", IO.STRING, IO.ANY, IO.BOOLEAN)
    RETURN_NAMES = ("dict", "key", "value", "success")
    OUTPUT_TOOLTIPS = ("The DICT with a random entry removed.", "The removed key.", "The removed value.", "False when the DICT was empty or the operation failed.")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop_random"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        seed = kwargs.get("seed")
        if seed is None:
            return float("NaN")  # Not equal to anything -> trigger recalculation
        return seed

    def pop_random(self, input_dict: Mapping[KT, VT], seed: _O[int] = None) -> tuple[Mapping[KT, VT], _U[KT, str], _O[VT], bool]:
        if not input_dict:
            return input_dict, "", None, False

        rng = random.Random(seed) if seed is not None else random
        result = dict(input_dict)
        try:
            random_key = rng.choice(list(result.keys()))
            random_value = result.pop(random_key)
        except Exception:
            return input_dict, "", None, False

        result = _output_dict_preserving_type(result, type(input_dict))
        return result, random_key, random_value, True


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
                "input_dict": ("DICT", {"tooltip": "The DICT to remove from."}),
                "key": (IO.STRING, {"default": "", "tooltip": "The key to remove."}),
            }
        }

    RETURN_TYPES = ("DICT", IO.BOOLEAN)
    RETURN_NAMES = ("dict", "key_removed")
    OUTPUT_TOOLTIPS = ("The DICT with the key removed (unchanged when it was absent).", "True when the key existed and was removed.")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "remove"

    def remove(self, input_dict: Mapping[KT, VT], key: Any) -> tuple[Mapping[KT, VT], bool]:
        if key not in input_dict:
            return input_dict, False

        result = dict(input_dict)
        del result[key]

        result = _output_dict_preserving_type(result, type(input_dict))
        return result, True


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
                "input_dict": ("DICT", {"tooltip": "The DICT to modify."}),
                "key": (IO.STRING, {"default": "", "tooltip": "The key to add or update."}),
                "value": (IO.ANY, {"tooltip": "The value to store under the key."}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("A new DICT with the key set to the given value.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "set"

    def set(self, input_dict: Mapping[KT, VT], key: KT2, value: VT2) -> tuple[Mapping[_U[KT, KT2], _U[VT, VT2]]]:
        result = dict(input_dict)
        result[key] = value

        result = _output_dict_preserving_type(result, type(input_dict))
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
                "input_dict": ("DICT", {"tooltip": "The DICT to read or modify."}),
                "key": (IO.STRING, {"default": "", "tooltip": "The key to look up."}),
                "default_value": (IO.ANY, {"tooltip": "Value inserted and returned when the key is missing."}),
            }
        }

    RETURN_TYPES = ("DICT", IO.ANY)
    RETURN_NAMES = ("DICT", "value")
    OUTPUT_TOOLTIPS = ("The DICT, with the default inserted when the key was missing.", "The value for the key (existing or the inserted default).")
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "setdefault"

    def setdefault(self, input_dict: Mapping[KT, VT], key: KT2, default_value: VT2 = None) -> tuple[Mapping[_U[KT, KT2], _U[VT, VT2]], _U[VT, VT2]]:
        result = dict(input_dict)
        value = result.setdefault(key, default_value)

        result = _output_dict_preserving_type(result, type(input_dict))
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
                "dict1": ("DICT", {"tooltip": "Base DICT to update."}),
                "dict2": ("DICT", {"tooltip": "DICT whose entries are added; it wins on duplicate keys."}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("The merged DICT with dict2's entries applied to dict1.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "update"

    def update(self, dict1: Mapping[KT, VT], dict2: Mapping[KT2, VT2]) -> tuple[Mapping[_U[KT, KT2], _U[VT, VT2]]]:
        if not dict2:
            return (dict1,)

        result = dict(dict1)
        result.update(dict2)

        result = _output_dict_preserving_type(result, type(dict1))
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
                "input_dict": ("DICT", {"tooltip": "The DICT to read."}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("values",)
    OUTPUT_TOOLTIPS = ("A LIST of all values in the DICT.",)
    CATEGORY = "Basic/DICT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "values"

    def values(self, input_dict: Mapping[Any, VT]) -> tuple[List[VT]]:
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
