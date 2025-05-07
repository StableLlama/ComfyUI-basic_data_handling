from typing import Any
from inspect import cleandoc

class ListAppend:
    """
    Adds an item to the end of a LIST.

    This node takes a LIST and any item as inputs, then returns a new LIST
    with the item appended to the end.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
                "item": ("*", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "append"

    def append(self, list: list[Any], item: Any) -> tuple[list[Any]]:
        result = list.copy()
        result.append(item)
        return (result,)


class ListExtend:
    """
    Extends a LIST by appending elements from another LIST.

    This node takes two LIST objects as input and returns a new LIST that contains
    all elements from both lists.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list1": ("LIST", {}),
                "list2": ("LIST", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "extend"

    def extend(self, list1: list[Any], list2: list[Any]) -> tuple[list[Any]]:
        result = list1.copy()
        result.extend(list2)
        return (result,)


class ListInsert:
    """
    Inserts an item at a specified position in a LIST.

    This node takes a LIST, an index, and any item as inputs, then returns a new
    LIST with the item inserted at the specified index.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
                "index": ("INT", {"default": 0}),
                "item": ("*", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "insert"

    def insert(self, list: list[Any], index: int, item: Any) -> tuple[list[Any]]:
        result = list.copy()
        result.insert(index, item)
        return (result,)


class ListRemove:
    """
    Removes the first occurrence of a specified value from a LIST.

    This node takes a LIST and a value as inputs, then returns a new LIST with
    the first occurrence of the value removed and a success indicator. If the value
    is not present, the original LIST is returned with success set to False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
                "value": ("*", {}),
            }
        }

    RETURN_TYPES = ("LIST", "BOOLEAN")
    RETURN_NAMES = ("list", "success")
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "remove"

    def remove(self, list: list[Any], value: Any) -> tuple[list[Any], bool]:
        result = list.copy()
        try:
            result.remove(value)
            return result, True
        except ValueError:
            return result, False


class ListPop:
    """
    Removes and returns an item at a specified position in a LIST.

    This node takes a LIST and an index as inputs, then returns both the new LIST
    with the item removed and the removed item. If no index is specified,
    removes and returns the last item.
    When the LIST is empty, the item is None.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            },
            "optional": {
                "index": ("INT", {"default": -1}),
            }
        }

    RETURN_TYPES = ("LIST", "*")
    RETURN_NAMES = ("list", "item")
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop"

    def pop(self, list: list[Any], index: int = -1) -> tuple[list[Any], Any]:
        result = list.copy()
        try:
            item = result.pop(index)
            return result, item
        except IndexError:
            return result, None


class ListClear:
    """
    Removes all items from a LIST.

    This node takes a LIST as input and returns a new empty LIST.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "clear"

    def clear(self, list: list[Any]) -> tuple[list[Any]]:
        return ([],)


class ListIndex:
    """
    Returns the index of the first occurrence of a value in a LIST.

    This node takes a LIST and a value as inputs, then returns the index of the first
    occurrence of the value. Optional start and end parameters limit the search to a slice
    of the LIST. Returns -1 if the value is not present.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
                "value": ("*", {}),
            },
            "optional": {
                "start": ("INT", {"default": 0}),
                "end": ("INT", {"default": -1}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("index",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "index"

    def index(self, list: list[Any], value: Any, start: int = 0, end: int = -1) -> tuple[int]:
        if end == -1:
            end = len(list)

        try:
            return (list.index(value, start, end),)
        except ValueError:
            return (-1,)


class ListCount:
    """
    Counts the number of occurrences of a value in a LIST.

    This node takes a LIST and a value as inputs, then returns the number of times
    the value appears in the LIST.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
                "value": ("*", {}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("count",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "count"

    def count(self, list: list[Any], value: Any) -> tuple[int]:
        return (list.count(value),)


class ListSort:
    """
    Sorts the items in a LIST.

    This node takes a LIST as input and returns a new sorted LIST.
    Option includes sorting in reverse order.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            },
            "optional": {
                "reverse": (["False", "True"], {"default": "False"}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "sort"

    def sort(self, list: list[Any], reverse: str = "False") -> tuple[list[Any]]:
        # Convert string to boolean
        reverse_bool = (reverse == "True")

        # Use sorted to create a new sorted list
        try:
            result = sorted(list, reverse=reverse_bool)
            return (result,)
        except TypeError:
            # If list contains mixed types that can't be compared, return original list
            return (list.copy(),)


class ListReverse:
    """
    Reverses the order of items in a LIST.

    This node takes a LIST as input and returns a new LIST with the items in reversed order.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "reverse"

    def reverse(self, list: list[Any]) -> tuple[list[Any]]:
        result = list.copy()
        result.reverse()
        return (result,)


class ListLength:
    """
    Returns the number of items in a LIST.

    This node takes a LIST as input and returns its length as an integer.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("length",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "length"

    def length(self, list: list[Any]) -> tuple[int]:
        return (len(list),)


class ListSlice:
    """
    Creates a slice of a LIST.

    This node takes a LIST and start/stop/step parameters, and returns a new LIST
    containing the specified slice of the original LIST.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            },
            "optional": {
                "start": ("INT", {"default": 0}),
                "stop": ("INT", {"default": -1}),
                "step": ("INT", {"default": 1}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "slice"

    def slice(self, list: list[Any], start: int = 0, stop: int = -1, step: int = 1) -> tuple[list[Any]]:
        if stop == -1:
            stop = len(list)

        return (list[start:stop:step],)


class ListGetItem:
    """
    Retrieves an item at a specified position in a LIST.

    This node takes a LIST and an index as inputs, then returns the item at the specified index.
    Negative indices count from the end of the LIST.
    Out of range indices return None.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
                "index": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("item",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_item"

    def get_item(self, list: list[Any], index: int) -> tuple[Any]:
        try:
            return (list[index],)
        except IndexError:
            return (None,)


class ListSetItem:
    """
    Sets an item at a specified position in a LIST.

    This node takes a LIST, an index, and a value, then returns a new LIST with
    the item at the specified index replaced by the value.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
                "index": ("INT", {"default": 0}),
                "value": ("*", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "set_item"

    def set_item(self, list: list[Any], index: int, value: Any) -> tuple[list[Any]]:
        result = list.copy()
        try:
            result[index] = value
            return (result,)
        except IndexError:
            raise IndexError(f"Index {index} out of range for LIST of length {len(list)}")


class ListContains:
    """
    Checks if a LIST contains a specified value.

    This node takes a LIST and a value as inputs, then returns True if the value
    is present in the LIST, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
                "value": ("*", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("contains",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "contains"

    def contains(self, list: list[Any], value: Any) -> tuple[bool]:
        return (value in list,)


class ListToDataList:
    """
    Converts a LIST object into a ComfyUI data list.

    This node takes a LIST object (Python list as a single variable) and
    converts it to a ComfyUI data list, allowing its items to be processed
    individually by nodes that accept data lists.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            }
        }

    RETURN_TYPES = ("*",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"
    OUTPUT_IS_LIST = (True,)

    def convert(self, list) -> tuple[list[Any]]:
        return (list,)


class ListToSet:
    """
    Converts a LIST into a SET.

    This node takes a LIST input and creates a new SET containing all unique elements
    from the LIST, removing any duplicates.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            }
        }

    RETURN_TYPES = ("SET",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"

    def convert(self, list: list[Any]) -> tuple[set[Any]]:
        return (set(list),)


class AnyToList:
    """
    Converts any input datatype into a LIST.

    This node takes any input value and wraps it in a LIST object,
    allowing it to be processed by nodes that expect LIST inputs.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("*", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"

    def convert(self, input: Any) -> tuple[list[Any]]:
        # Create a new list containing the input value
        return ([input],)


NODE_CLASS_MAPPINGS = {
    "ListAppend": ListAppend,
    "ListExtend": ListExtend,
    "ListInsert": ListInsert,
    "ListRemove": ListRemove,
    "ListPop": ListPop,
    "ListClear": ListClear,
    "ListIndex": ListIndex,
    "ListCount": ListCount,
    "ListSort": ListSort,
    "ListReverse": ListReverse,
    "ListLength": ListLength,
    "ListSlice": ListSlice,
    "ListGetItem": ListGetItem,
    "ListSetItem": ListSetItem,
    "ListContains": ListContains,
    "ListToDataList": ListToDataList,
    "ListToSet": ListToSet,
    "AnyToList": AnyToList,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ListAppend": "append",
    "ListExtend": "extend",
    "ListInsert": "insert",
    "ListRemove": "remove",
    "ListPop": "pop",
    "ListClear": "clear",
    "ListIndex": "index",
    "ListCount": "count",
    "ListSort": "sort",
    "ListReverse": "reverse",
    "ListLength": "length",
    "ListSlice": "slice",
    "ListGetItem": "get item",
    "ListSetItem": "set item",
    "ListContains": "contains",
    "ListToDataList": "convert to data list",
    "ListToSet": "convert to SET",
    "AnyToList": "any to LIST",
}
