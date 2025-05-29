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

INT_MAX = 2**15-1 # the computer can do more but be nice to the eyes


class ListCreate(ComfyNodeABC):
    """
    Creates a new LIST from items.

    This node creates and returns a LIST. The list of items is dynamically
    extended based on the number of inputs provided.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.ANY, {"_dynamic": "number"}),
            })
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_list"

    def create_list(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        return (list(kwargs.values()),)


class ListCreateFromBoolean(ComfyNodeABC):
    """
    Creates a new LIST from BOOLEAN items.

    This node creates and returns a LIST. The list of items is dynamically
    extended based on the number of inputs provided.
    """
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.BOOLEAN, {"_dynamic": "number"}),
            })
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_list"

    def create_list(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        return ([bool(value) for value in kwargs.values()],)


class ListCreateFromFloat(ComfyNodeABC):
    """
    Creates a new LIST from FLOAT items.

    This node creates and returns a LIST. The list of items is dynamically
    extended based on the number of inputs provided.
    """
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.FLOAT, {"_dynamic": "number"}),
            })
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_list"

    def create_list(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        return ([float(value) for value in kwargs.values()],)


class ListCreateFromInt(ComfyNodeABC):
    """
    Creates a new LIST from INT items.

    This node creates and returns a LIST. The list of items is dynamically
    extended based on the number of inputs provided.
    """
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.INT, {"_dynamic": "number"}),
            })
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_list"

    def create_list(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        return ([int(value) for value in kwargs.values()],)


class ListCreateFromString(ComfyNodeABC):
    """
    Creates a new LIST from STRING items.

    This node creates and returns a LIST. The list of items is dynamically
    extended based on the number of inputs provided.
    """
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.STRING, {"_dynamic": "number"}),
            })
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_list"

    def create_list(self, **kwargs: list[Any]) -> tuple[list[Any]]:
        return ([str(value) for value in kwargs.values()],)


class ListAppend(ComfyNodeABC):
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
                "item": (IO.ANY, {}),
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


class ListContains(ComfyNodeABC):
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
                "value": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("contains",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "contains"

    def contains(self, list: list[Any], value: Any) -> tuple[bool]:
        return (value in list,)


class ListCount(ComfyNodeABC):
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
                "value": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("count",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "count"

    def count(self, list: list[Any], value: Any) -> tuple[int]:
        return (list.count(value),)


class ListExtend(ComfyNodeABC):
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


class ListFirst(ComfyNodeABC):
    """
    Returns the first element in a LIST.

    This node takes a LIST as input and returns the first element of the list.
    If the LIST is empty, it returns None.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("first_element",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_first_element"

    def get_first_element(self, list: list[Any]) -> tuple[Any]:
        return (list[0] if list else None,)


class ListGetItem(ComfyNodeABC):
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

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("item",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_item"

    def get_item(self, list: list[Any], index: int) -> tuple[Any]:
        try:
            return (list[index],)
        except IndexError:
            return (None,)


class ListIndex(ComfyNodeABC):
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
                "value": (IO.ANY, {}),
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


class ListInsert(ComfyNodeABC):
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
                "item": (IO.ANY, {}),
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


class ListLast(ComfyNodeABC):
    """
    Returns the last element in a LIST.

    This node takes a LIST as input and returns the last element of the list.
    If the LIST is empty, it returns None.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("last_element",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_last_element"

    def get_last_element(self, list: list[Any]) -> tuple[Any]:
        return (list[-1] if list else None,)


class ListLength(ComfyNodeABC):
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


class ListMax(ComfyNodeABC):
    """
    Returns the maximum value in a LIST.

    This node takes a LIST of comparable items and returns the maximum value.
    Returns None if the LIST is empty or if items are not comparable.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("max_value",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "find_max"

    def find_max(self, list: list[Any]) -> tuple[Any]:
        if not list:
            return (None,)

        try:
            return (max(list),)
        except (TypeError, ValueError):
            # Handle case where list contains non-comparable elements
            return (None,)


class ListMin(ComfyNodeABC):
    """
    Returns the minimum value in a LIST.

    This node takes a LIST of comparable items and returns the minimum value.
    Returns None if the LIST is empty or if items are not comparable.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("min_value",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "find_min"

    def find_min(self, list: list[Any]) -> tuple[Any]:
        if not list:
            return (None,)

        try:
            return (min(list),)
        except (TypeError, ValueError):
            # Handle case where list contains non-comparable elements
            return (None,)


class ListPop(ComfyNodeABC):
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

    RETURN_TYPES = ("LIST", IO.ANY)
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


class ListPopRandom(ComfyNodeABC):
    """
    Removes and returns a random element from a LIST.

    This node takes a LIST as input and returns the LIST with the random element removed
    and the removed element itself. If the LIST is empty, it returns None for the element.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "list": ("LIST", {}),
            }
        }

    RETURN_TYPES = ("LIST", IO.ANY)
    RETURN_NAMES = ("list", "item")
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop_random_element"

    def pop_random_element(self, list: list[Any]) -> tuple[list[Any], Any]:
        import random
        result = list.copy()
        if result:
            random_index = random.randrange(len(result))
            random_element = result.pop(random_index)
            return result, random_element
        return result, None


class ListRemove(ComfyNodeABC):
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
                "value": (IO.ANY, {}),
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


class ListReverse(ComfyNodeABC):
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


class ListSetItem(ComfyNodeABC):
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
                "value": (IO.ANY, {}),
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


class ListSlice(ComfyNodeABC):
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
                "stop": ("INT", {"default": INT_MAX}),
                "step": ("INT", {"default": 1}),
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "slice"

    def slice(self, list: list[Any], start: int = 0, stop: int = INT_MAX,
              step: int = 1) -> tuple[list[Any]]:
        return (list[start:stop:step],)


class ListSort(ComfyNodeABC):
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


class ListToDataList(ComfyNodeABC):
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

    RETURN_TYPES = (IO.ANY,)
    CATEGORY = "Basic/LIST"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"
    OUTPUT_IS_LIST = (True,)

    def convert(self, list) -> tuple[list[Any]]:
        return (list,)


class ListToSet(ComfyNodeABC):
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


NODE_CLASS_MAPPINGS = {
    "Basic data handling: ListCreate": ListCreate,
    "Basic data handling: ListCreateFromBoolean": ListCreateFromBoolean,
    "Basic data handling: ListCreateFromFloat": ListCreateFromFloat,
    "Basic data handling: ListCreateFromInt": ListCreateFromInt,
    "Basic data handling: ListCreateFromString": ListCreateFromString,
    "Basic data handling: ListAppend": ListAppend,
    "Basic data handling: ListContains": ListContains,
    "Basic data handling: ListCount": ListCount,
    "Basic data handling: ListExtend": ListExtend,
    "Basic data handling: ListFirst": ListFirst,
    "Basic data handling: ListGetItem": ListGetItem,
    "Basic data handling: ListIndex": ListIndex,
    "Basic data handling: ListInsert": ListInsert,
    "Basic data handling: ListLast": ListLast,
    "Basic data handling: ListLength": ListLength,
    "Basic data handling: ListMax": ListMax,
    "Basic data handling: ListMin": ListMin,
    "Basic data handling: ListPop": ListPop,
    "Basic data handling: ListPopRandom": ListPopRandom,
    "Basic data handling: ListRemove": ListRemove,
    "Basic data handling: ListReverse": ListReverse,
    "Basic data handling: ListSetItem": ListSetItem,
    "Basic data handling: ListSlice": ListSlice,
    "Basic data handling: ListSort": ListSort,
    "Basic data handling: ListToDataList": ListToDataList,
    "Basic data handling: ListToSet": ListToSet,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: ListCreate": "create LIST",
    "Basic data handling: ListCreateFromBoolean": "create LIST from BOOLEANs",
    "Basic data handling: ListCreateFromFloat": "create LIST from FLOATs",
    "Basic data handling: ListCreateFromInt": "create LIST from INTs",
    "Basic data handling: ListCreateFromString": "create LIST from STRINGs",
    "Basic data handling: ListAppend": "append",
    "Basic data handling: ListContains": "contains",
    "Basic data handling: ListCount": "count",
    "Basic data handling: ListExtend": "extend",
    "Basic data handling: ListFirst": "first element",
    "Basic data handling: ListGetItem": "get item",
    "Basic data handling: ListIndex": "index",
    "Basic data handling: ListInsert": "insert",
    "Basic data handling: ListLast": "last element",
    "Basic data handling: ListLength": "length",
    "Basic data handling: ListMax": "max",
    "Basic data handling: ListMin": "min",
    "Basic data handling: ListPop": "pop",
    "Basic data handling: ListPopRandom": "pop random",
    "Basic data handling: ListRemove": "remove",
    "Basic data handling: ListReverse": "reverse",
    "Basic data handling: ListSetItem": "set item",
    "Basic data handling: ListSlice": "slice",
    "Basic data handling: ListSort": "sort",
    "Basic data handling: ListToDataList": "convert to Data List",
    "Basic data handling: ListToSet": "convert to SET",
}
