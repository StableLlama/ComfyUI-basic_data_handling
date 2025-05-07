from typing import Any

from inspect import cleandoc

class DataListAppend:
    """
    Adds an item to the end of a list.

    This node takes a list and any item as inputs, then returns the modified
    list with the new item appended.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "list":("*",{}),
                "item":("*",{}),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "append"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def append(self, **kwargs: dict[str, list]) -> tuple[list[Any]]:
        result = kwargs.get('list', []).copy()
        item = kwargs.get('item', [])
        if len(item) > 0:
            result.append(item[0])
        return (result,)


class DataListExtend:
    """
    Extends a list by appending elements from another list.

    This node takes two lists as input and returns a new list that contains
    all elements from both lists.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "list_a": ("*",{}),
                "list_b": ("*",{}),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "extend"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def extend(self, **kwargs: dict[str, list]) -> tuple[list[Any]]:
        return (kwargs.get('list_a', []) + kwargs.get('list_b', []),)


class DataListInsert:
    """
    Inserts an item at a specified position in a list.

    This node takes a list, an index, and any item as inputs, then returns a new
    list with the item inserted at the specified index.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*",),
                "index": ("INT", {"default": 0}),
                "item": ("*",),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "insert"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def insert(self, **kwargs: dict[str, list]) -> tuple[list[Any]]:
        result = kwargs.get('list', []).copy()
        result.insert(kwargs.get('index', [0])[0], kwargs.get('item', [None])[0])
        return (result,)


class DataListRemove:
    """
    Removes the first occurrence of a specified value from a list.

    This node takes a list and a value as inputs, then returns a new list with
    the first occurrence of the value removed. Raises a ValueError if the value is not present.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*",),
                "value": ("*",),
            }
        }

    RETURN_TYPES = ("*", "BOOLEAN",)
    RETURN_NAMES = ("list", "success",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "remove"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True, False,)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def remove(self, **kwargs: dict[str, list]) -> tuple[list[Any], bool]:
        result = kwargs.get('list', []).copy()
        value = kwargs.get('value', [])
        try:
            result.remove(value[0])
            return result, True
        except ValueError:
            return result, False


class DataListPop:
    """
    Removes and returns an item at a specified position in a list.

    This node takes a list and an index as inputs, then returns both the new list
    with the item removed and the removed item. If no index is specified,
    removes and returns the last item.
    When the list is empty, the item is None.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*",),
            },
            "optional": {
                "index": ("INT", {"default": -1}),
            }
        }

    RETURN_TYPES = ("*", "*")
    RETURN_NAMES = ("list", "item")
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True, False)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool|str:
        if input_types["index"] not in ("INT"):
            return "index must be an INT type"
        return True

    def pop(self, **kwargs: dict[str, list]) -> tuple[list[Any], Any]:
        result = kwargs.get('list', []).copy()
        index = kwargs.get('index', [-1])[0]
        try:
            item = result.pop(index)
            return result, item
        except IndexError:
            return result, None


class DataListClear:
    """
    Removes all items from a list.

    This node takes a list as input and returns a new empty list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "list": ("*",),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "clear"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def clear(self, **kwargs: dict[str, list]) -> tuple[[]]:
        # Return a new empty list rather than modifying the input
        return ([],)


class DataListIndex:
    """
    Returns the index of the first occurrence of a value in a list.

    This node takes a list and a value as inputs, then returns the index of the first
    occurrence of the value. Optional start and end parameters limit the search to a slice
    of the list. Returns -1 if the value is not present.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*",),
                "value": ("*",),
            },
            "optional": {
                "start": ("INT", {"default": 0}),
                "end": ("INT", {"default": -1}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("index",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "list_index"
    INPUT_IS_LIST = True

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def list_index(self, **kwargs: dict[str, list]) -> tuple[int]:
        input_list = kwargs.get('list', [])
        value = kwargs.get('value', [None])[0]
        start = kwargs.get('start', [0])[0]
        end = kwargs.get('end', [-1])[0]
        if end == -1:
            end = len(input_list)

        try:
            return (input_list.index(value, start, end),)
        except ValueError:
            return (-1,)


class DataListCount:
    """
    Counts the number of occurrences of a value in a list.

    This node takes a list and a value as inputs, then returns the number of times
    the value appears in the list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*",),
                "value": ("*",),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("count",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "count"
    INPUT_IS_LIST = True

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def count(self, **kwargs: dict[str, list]) -> tuple[int]:
        value = kwargs.get('value', [None])[0]
        return (kwargs.get('list', []).count(value),)


class DataListSort:
    """
    Sorts the items in a list.

    This node takes a list as input and returns a new sorted list.
    Options include sorting in reverse order and using a key function.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*",),
            },
            "optional": {
                "reverse": (["False", "True"], {"default": "False"}),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "sort"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def sort(self, **kwargs: dict[str, list]) -> tuple[list[Any]]:
        # Convert string to boolean
        reverse = kwargs.get('reverse', ["False"])[0] == "True"

        result = sorted(kwargs.get('list', []), reverse=reverse)
        return (result,)


class DataListReverse:
    """
    Reverses the order of items in a list.

    This node takes a list as input and returns a new list with the items in reversed order.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*",),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "reverse"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def reverse(self, **kwargs: dict[str, list]) -> tuple[list[Any]]:
        result = kwargs.get('list', []).copy()
        result.reverse()
        return (result,)


class DataListCopy:
    """
    Creates a shallow copy of a list.

    This node takes a list as input and returns a new list that is a shallow copy of the original.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*",),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "copy"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def copy(self, **kwargs: dict[str, list]) -> tuple[list[Any]]:
        return (kwargs.get('list', []).copy(),)


class DataListLength:
    """
    Counts the number of items in a list.

    This node takes a list as input and returns its length as an integer.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*",),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("length",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "length"
    INPUT_IS_LIST = True

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def length(self, **kwargs: dict[str, list]) -> tuple[int]:
        return (len(kwargs.get('list', [])),)


class DataListSlice:
    """
    Creates a slice of a list.

    This node takes a list and start/stop/step parameters, and returns a new list
    containing the specified slice of the original list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*",),
            },
            "optional": {
                "start": ("INT", {"default": 0}),
                "stop": ("INT", {"default": -1}),
                "step": ("INT", {"default": 1}),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "slice"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def slice(self, **kwargs: dict[str, list]) -> tuple[list[Any]]:
        input_list = kwargs.get('list', [])
        start = kwargs.get('start', [0])[0]
        stop = kwargs.get('stop', [-1])[0]
        step = kwargs.get('step', [1])[0]

        if stop == -1:
            stop = len(input_list)

        return (input_list[start:stop:step],)


class DataListGetItem:
    """
    Retrieves an item at a specified position in a list.

    This node takes a list and an index as inputs, then returns the item at the specified index.
    Negative indices count from the end of the list.
    Out of range indices return None.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_list": ("*",),
                "index": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("item",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_item"
    INPUT_IS_LIST = True

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def get_item(self, **kwargs: dict[str, list]) -> tuple[Any]:
        index = kwargs.get('index', [0])[0]
        try:
            return (kwargs.get('list', [])[index],)
        except IndexError:
            return (None,)


class DataListSetItem:
    """
    Sets an item at a specified position in a list.

    This node takes a list, an index, and a value, then returns a new list with
    the item at the specified index replaced by the value.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*",),
                "index": ("INT", {"default": 0}),
                "value": ("*",),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "set_item"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def set_item(self, **kwargs: dict[str, list]) -> tuple[Any]:
        input_list = kwargs.get('list', [])
        index = kwargs.get('index', [0])[0]
        value = kwargs.get('value', [None])[0]
        try:
            result = input_list.copy()
            result[index] = value
            return (result,)
        except IndexError:
            raise IndexError(f"Index {index} out of range for list of length {len(input_list)}")


class DataListContains:
    """
    Checks if a list contains a specified value.

    This node takes a list and a value as inputs, then returns True if the value
    is present in the list, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_list": ("*",),
                "value": ("*",),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("contains",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "contains"
    INPUT_IS_LIST = True

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def contains(self, **kwargs: dict[str, list]) -> tuple[bool]:
        value = kwargs.get('value', [])
        if len(value) == 0:
            return (False,)
        return (value[0] in kwargs.get('list', []),)


class DataListCreateEmpty:
    """
    Creates a new empty list.

    This node creates and returns an empty list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_empty"
    OUTPUT_IS_LIST = (True,)

    def create_empty(self) -> tuple[[]]:
        return ([],)


class DataListZip:
    """
    Combines multiple lists element-wise.

    This node takes multiple data lists as input and returns a new data list
    where each item is a list containing the corresponding elements from the input lists.
    The length of the output list will be equal to the length of the shortest input list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list1": ("*",),
                "list2": ("*",),
            },
            "optional": {
                "list3": ("*",),
                "list4": ("*",),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "zip_lists"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def zip_lists(self, **kwargs: dict[str, list]) -> tuple[list[Any]]:
        lists = [kwargs.get('list1', []), kwargs.get('list2', [])]

        if 'list3' in kwargs:
            lists.append(kwargs['list3'])

        if 'list4' in kwargs:
            lists.append(kwargs['list4'])

        # Zip the lists together and convert each tuple to a list
        result = [list(item) for item in zip(*lists)]
        return (result,)


class DataListToList:
    """
    Converts a ComfyUI data list into a LIST object.

    This node takes a data list input (which is typically a list of items with the same type)
    and converts it to a LIST object (a Python list as a single variable).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("*", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"
    INPUT_IS_LIST = True

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def convert(self, **kwargs: dict[str, list]) -> tuple[list[Any]]:
        return (kwargs.get('list', []).copy(),)


NODE_CLASS_MAPPINGS = {
    "DataListAppend": DataListAppend,
    "DataListExtend": DataListExtend,
    "DataListInsert": DataListInsert,
    "DataListRemove": DataListRemove,
    "DataListPop": DataListPop,
    "DataListClear": DataListClear,
    "DataListIndex": DataListIndex,
    "DataListCount": DataListCount,
    "DataListSort": DataListSort,
    "DataListReverse": DataListReverse,
    "DataListCopy": DataListCopy,
    "DataListLength": DataListLength,
    "DataListSlice": DataListSlice,
    "DataListGetItem": DataListGetItem,
    "DataListSetItem": DataListSetItem,
    "DataListContains": DataListContains,
    "DataListCreateEmpty": DataListCreateEmpty,
    "DataListZip": DataListZip,
    "DataListToList": DataListToList,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DataListAppend": "append",
    "DataListExtend": "extend",
    "DataListInsert": "insert",
    "DataListRemove": "remove",
    "DataListPop": "pop",
    "DataListClear": "clear",
    "DataListIndex": "index",
    "DataListCount": "count",
    "DataListSort": "sort",
    "DataListReverse": "reverse",
    "DataListCopy": "copy",
    "DataListLength": "length",
    "DataListSlice": "slice",
    "DataListGetItem": "get_item",
    "DataListSetItem": "set_item",
    "DataListContains": "contains",
    "DataListCreateEmpty": "create_empty",
    "DataListZip": "zip",
    "DataListToList": "convert to LIST",
}
