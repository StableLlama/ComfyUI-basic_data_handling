from typing import Any
from inspect import cleandoc
from comfy.comfy_types.node_typing import IO, ComfyNodeABC

INT_MAX = 2**15-1 # the computer can do more but be nice to the eyes

class DataListAppend(ComfyNodeABC):
    """
    Adds an item to the end of a list.

    This node takes a list and any item as inputs, then returns the modified
    list with the new item appended.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "list":(IO.ANY,{}),
                "item":(IO.ANY,{}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "append"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def append(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        result = kwargs.get('list', []).copy()
        item = kwargs.get('item', [])
        if len(item) > 0:
            result.append(item[0])
        return (result,)


class DataListContains(ComfyNodeABC):
    """
    Checks if a list contains a specified value.

    This node takes a list and a value as inputs, then returns True if the value
    is present in the list, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.ANY,),
                "value": (IO.ANY,),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("contains",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "contains"
    INPUT_IS_LIST = True

    def contains(self, **kwargs: list[Any]) -> tuple[bool]:
        value = kwargs.get('value', [])
        if len(value) == 0:
            return (False,)
        return (value[0] in kwargs.get('list', []),)


class DataListCount(ComfyNodeABC):
    """
    Counts the number of occurrences of a value in a list.

    This node takes a list and a value as inputs, then returns the number of times
    the value appears in the list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.ANY,),
                "value": (IO.ANY,),
            }
        }

    RETURN_TYPES = (IO.INT,)
    RETURN_NAMES = ("count",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "count"
    INPUT_IS_LIST = True

    def count(self, **kwargs: list[Any]) -> tuple[int]:
        value = kwargs.get('value', [None])[0]
        return (kwargs.get('list', []).count(value),)


class DataListCreateEmpty(ComfyNodeABC):
    """
    Creates a new empty list.

    This node creates and returns an empty list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_empty"
    OUTPUT_IS_LIST = (True,)

    def create_empty(self) -> tuple[list]:
        return ([],)


class DataListExtend(ComfyNodeABC):
    """
    Extends a list by appending elements from another list.

    This node takes two lists as input and returns a new list that contains
    all elements from both lists.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "list_a": (IO.ANY,{}),
                "list_b": (IO.ANY,{}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "extend"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def extend(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        return (kwargs.get('list_a', []) + kwargs.get('list_b', []),)


class DataListFilter(ComfyNodeABC):
    """
    Filters a data list using boolean values.

    This node takes a value data list and a filter data list (containing only boolean values).
    It returns a new data list containing only the elements from the value list where the
    corresponding element in the filter list is False.

    If the lists have different lengths, the last element of the shorter list is repeated
    till the lengths are matching.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.ANY, {}),
                "filter": (IO.BOOLEAN, {"forceInput": True}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("filtered_list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "filter_data"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def filter_data(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        values = kwargs.get('value', [])
        filters = kwargs.get('filter', [])

        # Create a new list with only items where the filter is False
        result = [_val for _val, _filter in zip(values, filters) if not _filter]

        return (result,)


class DataListGetItem(ComfyNodeABC):
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
                "list": (IO.ANY,),
                "index": (IO.INT, {"default": 0}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("item",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_item"
    INPUT_IS_LIST = True

    def get_item(self, **kwargs: list[Any]) -> tuple[Any]:
        index = kwargs.get('index', [0])[0]
        try:
            return (kwargs.get('list', [])[index],)
        except IndexError:
            return (None,)


class DataListIndex(ComfyNodeABC):
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
                "list": (IO.ANY,),
                "value": (IO.ANY,),
            },
            "optional": {
                "start": (IO.INT, {"default": 0}),
                "end": (IO.INT, {"default": -1}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    RETURN_NAMES = ("index",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "list_index"
    INPUT_IS_LIST = True

    def list_index(self, **kwargs: list[Any]) -> tuple[int]:
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


class DataListInsert(ComfyNodeABC):
    """
    Inserts an item at a specified position in a list.

    This node takes a list, an index, and any item as inputs, then returns a new
    list with the item inserted at the specified index.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.ANY,),
                "index": (IO.INT, {"default": 0}),
                "item": (IO.ANY,),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "insert"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def insert(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        result = kwargs.get('list', []).copy()
        result.insert(kwargs.get('index', [0])[0], kwargs.get('item', [None])[0])
        return (result,)


class DataListLength(ComfyNodeABC):
    """
    Counts the number of items in a list.

    This node takes a list as input and returns its length as an integer.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.ANY,),
            }
        }

    RETURN_TYPES = (IO.INT,)
    RETURN_NAMES = ("length",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "length"
    INPUT_IS_LIST = True

    def length(self, **kwargs: list[Any]) -> tuple[int]:
        return (len(kwargs.get('list', [])),)


class DataListMax(ComfyNodeABC):
    """
    Finds the maximum value in a list of numbers.

    This node takes a list of numbers (either FLOAT or INT) and returns
    the maximum value. Returns None if the list is empty or if it contains
    non-numeric values.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.NUMBER, {}),
            }
        }

    RETURN_TYPES = (IO.NUMBER,)
    RETURN_NAMES = ("max",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "find_max"
    INPUT_IS_LIST = True

    def find_max(self, **kwargs: list[Any]) -> tuple[Any]:
        values = kwargs.get('list', [])
        if not values:
            return (None,)

        try:
            # Return the same type as found in the maximum value
            return (max(values),)
        except (TypeError, ValueError):
            # Handle case where list contains non-comparable elements
            return (None,)


class DataListMin(ComfyNodeABC):
    """
    Finds the minimum value in a list of numbers.

    This node takes a list of numbers (either FLOAT or INT) and returns
    the minimum value. Returns None if the list is empty or if it contains
    non-numeric values.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.NUMBER, {}),
            }
        }

    RETURN_TYPES = (IO.NUMBER,)
    RETURN_NAMES = ("min",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "find_min"
    INPUT_IS_LIST = True

    def find_min(self, **kwargs: list[Any]) -> tuple[Any]:
        values = kwargs.get('list', [])
        if not values:
            return (None,)

        try:
            # Return the same type as found in the minimum value
            return (min(values),)
        except (TypeError, ValueError):
            # Handle case where list contains non-comparable elements
            return (None,)


class DataListPop(ComfyNodeABC):
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
                "list": (IO.ANY,),
            },
            "optional": {
                "index": (IO.INT, {"default": -1}),
            }
        }

    RETURN_TYPES = (IO.ANY, IO.ANY)
    RETURN_NAMES = ("list", "item")
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True, False)

    def pop(self, **kwargs: list[Any]) -> tuple[list[Any], Any]:
        result = kwargs.get('list', []).copy()
        index = kwargs.get('index', [-1])[0]
        try:
            item = result.pop(index)
            return result, item
        except IndexError:
            return result, None


class DataListRemove(ComfyNodeABC):
    """
    Removes the first occurrence of a specified value from a list.

    This node takes a list and a value as inputs, then returns a new list with
    the first occurrence of the value removed. Raises a ValueError if the value is not present.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.ANY,),
                "value": (IO.ANY,),
            }
        }

    RETURN_TYPES = (IO.ANY, IO.BOOLEAN,)
    RETURN_NAMES = ("list", "success",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "remove"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True, False,)

    def remove(self, **kwargs: list[Any]) -> tuple[list[Any], bool]:
        result = kwargs.get('list', []).copy()
        value = kwargs.get('value', [])
        try:
            result.remove(value[0])
            return result, True
        except ValueError:
            return result, False


class DataListReverse(ComfyNodeABC):
    """
    Reverses the order of items in a list.

    This node takes a list as input and returns a new list with the items in reversed order.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.ANY,),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "reverse"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def reverse(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        result = kwargs.get('list', []).copy()
        result.reverse()
        return (result,)


class DataListSetItem(ComfyNodeABC):
    """
    Sets an item at a specified position in a list.

    This node takes a list, an index, and a value, then returns a new list with
    the item at the specified index replaced by the value.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.ANY,),
                "index": (IO.INT, {"default": 0}),
                "value": (IO.ANY,),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "set_item"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def set_item(self, **kwargs: list[Any]) -> tuple[Any]:
        input_list = kwargs.get('list', [])
        index = kwargs.get('index', [0])[0]
        value = kwargs.get('value', [None])[0]
        try:
            result = input_list.copy()
            result[index] = value
            return (result,)
        except IndexError:
            raise IndexError(f"Index {index} out of range for list of length {len(input_list)}")


class DataListSlice(ComfyNodeABC):
    """
    Creates a slice of a list.

    This node takes a list and start/stop/step parameters, and returns a new list
    containing the specified slice of the original list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.ANY,),
            },
            "optional": {
                "start": (IO.INT, {"default": 0}),
                "stop": (IO.INT, {"default": INT_MAX}),
                "step": (IO.INT, {"default": 1}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "slice"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def slice(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        input_list = kwargs.get('list', [])
        start = kwargs.get('start', [0])[0]
        stop = kwargs.get('stop', [INT_MAX])[0]
        step = kwargs.get('step', [1])[0]
        print(f"start: {start}, stop: {stop}, step: {step}; input_list: {input_list}")

        return (input_list[start:stop:step],)


class DataListSort(ComfyNodeABC):
    """
    Sorts the items in a list.

    This node takes a list as input and returns a new sorted list.
    Options include sorting in reverse order and using a key function.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.ANY,),
            },
            "optional": {
                "reverse": (["False", "True"], {"default": "False"}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "sort"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def sort(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        # Convert string to boolean
        reverse = kwargs.get('reverse', ["False"])[0] == "True"

        result = sorted(kwargs.get('list', []), reverse=reverse)
        return (result,)


class DataListZip(ComfyNodeABC):
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
                "list1": (IO.ANY,),
                "list2": (IO.ANY,),
            },
            "optional": {
                "list3": (IO.ANY,),
                "list4": (IO.ANY,),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("list",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "zip_lists"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def zip_lists(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        lists = [kwargs.get('list1', []), kwargs.get('list2', [])]

        if 'list3' in kwargs:
            lists.append(kwargs['list3'])

        if 'list4' in kwargs:
            lists.append(kwargs['list4'])

        # Zip the lists together and convert each tuple to a list
        result = [list(item) for item in zip(*lists)]
        return (result,)


class DataListToList(ComfyNodeABC):
    """
    Converts a ComfyUI data list into a LIST object.

    This node takes a data list input (which is typically a list of items with the same type)
    and converts it to a LIST object (a Python list as a single variable).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"
    INPUT_IS_LIST = True

    def convert(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        return (kwargs.get('list', []).copy(),)


class DataListToSet(ComfyNodeABC):
    """
    Converts a ComfyUI data list into a LIST object.

    This node takes a data list input (which is typically a list of items with the same type)
    and converts it to a LIST object (a Python list as a single variable).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("SET",)
    CATEGORY = "Basic/data list"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"
    INPUT_IS_LIST = True

    def convert(self, **kwargs: list[Any]) -> tuple[set[Any]]:
        return (set(kwargs.get('list', [])),)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: DataListAppend": DataListAppend,
    "Basic data handling: DataListContains": DataListContains,
    "Basic data handling: DataListCount": DataListCount,
    "Basic data handling: DataListCreateEmpty": DataListCreateEmpty,
    "Basic data handling: DataListExtend": DataListExtend,
    "Basic data handling: DataListFilter": DataListFilter,
    "Basic data handling: DataListGetItem": DataListGetItem,
    "Basic data handling: DataListIndex": DataListIndex,
    "Basic data handling: DataListInsert": DataListInsert,
    "Basic data handling: DataListLength": DataListLength,
    "Basic data handling: DataListMax": DataListMax,
    "Basic data handling: DataListMin": DataListMin,
    "Basic data handling: DataListPop": DataListPop,
    "Basic data handling: DataListRemove": DataListRemove,
    "Basic data handling: DataListReverse": DataListReverse,
    "Basic data handling: DataListSetItem": DataListSetItem,
    "Basic data handling: DataListSlice": DataListSlice,
    "Basic data handling: DataListSort": DataListSort,
    "Basic data handling: DataListZip": DataListZip,
    "Basic data handling: DataListToList": DataListToList,
    "Basic data handling: DataListToSet": DataListToSet,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: DataListAppend": "append",
    "Basic data handling: DataListContains": "contains",
    "Basic data handling: DataListCount": "count",
    "Basic data handling: DataListCreateEmpty": "create empty",
    "Basic data handling: DataListExtend": "extend",
    "Basic data handling: DataListFilter": "filter",
    "Basic data handling: DataListGetItem": "get item",
    "Basic data handling: DataListIndex": "index",
    "Basic data handling: DataListInsert": "insert",
    "Basic data handling: DataListLength": "length",
    "Basic data handling: DataListMax": "max",
    "Basic data handling: DataListMin": "min",
    "Basic data handling: DataListPop": "pop",
    "Basic data handling: DataListRemove": "remove",
    "Basic data handling: DataListReverse": "reverse",
    "Basic data handling: DataListSetItem": "set item",
    "Basic data handling: DataListSlice": "slice",
    "Basic data handling: DataListSort": "sort",
    "Basic data handling: DataListZip": "zip",
    "Basic data handling: DataListToList": "convert to LIST",
    "Basic data handling: DataListToSet": "convert to SET",
}
