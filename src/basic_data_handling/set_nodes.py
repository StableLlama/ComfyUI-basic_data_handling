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


class SetCreate(ComfyNodeABC):
    """
    Creates a new SET from items.

    This node creates and returns a SET. The list of items is dynamically
    extended based on the number of inputs provided.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.ANY, {"_dynamic": "number", "widgetType": "STRING", "tooltip": "One of the items to add to the SET. Connect more values to add more items."}),
            })
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("The new SET containing the provided items (duplicates removed).",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_set"

    def create_set(self, **kwargs: list[Any]) -> tuple[set[Any]]:
        values = list(kwargs.values())[:-1]
        return (set(values),)


class SetCreateFromBoolean(ComfyNodeABC):
    """
    Creates a new SET from items.

    This node creates and returns a SET. The list of items is dynamically
    extended based on the number of inputs provided.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.BOOLEAN, {"_dynamic": "number", "widgetType": "STRING", "tooltip": "One of the boolean items to add to the SET. Connect more values to add more items."}),
            })
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("The new SET containing the provided boolean items (duplicates removed).",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_set"

    def create_set(self, **kwargs: list[Any]) -> tuple[set[Any]]:
        values = [bool(value) for value in list(kwargs.values())[:-1]]
        return (set(values),)


class SetCreateFromFloat(ComfyNodeABC):
    """
    Creates a new SET from items.

    This node creates and returns a SET. The list of items is dynamically
    extended based on the number of inputs provided.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.FLOAT, {"_dynamic": "number", "widgetType": "STRING", "tooltip": "One of the float items to add to the SET. Connect more values to add more items."}),
            })
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("The new SET containing the provided float items (duplicates removed).",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_set"

    def create_set(self, **kwargs: list[Any]) -> tuple[set[Any]]:
        values = [float(value) for value in list(kwargs.values())[:-1]]
        return (set(values),)


class SetCreateFromInt(ComfyNodeABC):
    """
    Creates a new SET from items.

    This node creates and returns a SET. The list of items is dynamically
    extended based on the number of inputs provided.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.INT, {"_dynamic": "number", "widgetType": "STRING", "tooltip": "One of the integer items to add to the SET. Connect more values to add more items."}),
            })
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("The new SET containing the provided integer items (duplicates removed).",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_set"

    def create_set(self, **kwargs: list[Any]) -> tuple[set[Any]]:
        values = [int(value) for value in list(kwargs.values())[:-1]]
        return (set(values),)


class SetCreateFromString(ComfyNodeABC):
    """
    Creates a new SET from items.

    This node creates and returns a SET. The list of items is dynamically
    extended based on the number of inputs provided.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.STRING, {"_dynamic": "number", "widgetType": "STRING", "tooltip": "One of the string items to add to the SET. Connect more values to add more items."}),
            })
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("The new SET containing the provided string items (duplicates removed).",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create_set"

    def create_set(self, **kwargs: list[Any]) -> tuple[set[Any]]:
        values = [str(value) for value in list(kwargs.values())[:-1]]
        return (set(values),)


class SetAdd(ComfyNodeABC):
    """
    Adds an item to a SET.

    This node takes a SET and any item as inputs, then returns a new SET
    with the item added. If the item is already present, the SET remains unchanged.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to add to."}),
                "item": (IO.ANY, {"tooltip": "The item to add."}),
            }
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("The SET with the item added (unchanged when the item was already present).",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "add"

    def add(self, set: set[Any], item: Any) -> tuple[set[Any]]:
        result = set.copy()
        result.add(item)
        return (result,)


class SetAll(ComfyNodeABC):
    """
    Checks if all elements in the SET are true.

    This node takes a SET as input and returns True if all elements in the SET
    evaluate to True (or if the SET is empty), and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to evaluate."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("all_true",)
    OUTPUT_TOOLTIPS = ("True when every element is truthy (or the SET is empty).",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_all"

    def check_all(self, set: set[Any]) -> tuple[bool]:
        return (all(set),)


class SetAny(ComfyNodeABC):
    """
    Checks if any element in the SET is true.

    This node takes a SET as input and returns True if at least one element
    in the SET evaluates to True, and False otherwise (including if the SET is empty).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to evaluate."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("any_true",)
    OUTPUT_TOOLTIPS = ("True when at least one element is truthy (False for an empty SET).",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_any"

    def check_any(self, set: set[Any]) -> tuple[bool]:
        return (any(set),)


class SetContains(ComfyNodeABC):
    """
    Checks if a SET contains a specified value.

    This node takes a SET and a value as inputs, then returns True if the value
    is present in the SET, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to search."}),
                "value": (IO.ANY, {"tooltip": "The value to look for."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("contains",)
    OUTPUT_TOOLTIPS = ("True when the value is present in the SET.",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "contains"

    def contains(self, set: set[Any], value: Any) -> tuple[bool]:
        return (value in set,)


class SetDifference(ComfyNodeABC):
    """
    Returns the difference between two SETs.

    This node takes two SETs as input and returns a new SET containing
    elements in the first SET but not in the second SET.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set1": ("SET", {"tooltip": "The SET to subtract from."}),
                "set2": ("SET", {"tooltip": "The SET of elements to remove."}),
            }
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("Elements in set1 that are not in set2.",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "difference"

    def difference(self, set1: set[Any], set2: set[Any]) -> tuple[set[Any]]:
        result = set1.copy()
        result.difference_update(set2)
        return (result,)


class SetDiscard(ComfyNodeABC):
    """
    Removes an item from a SET if it is present.

    This node takes a SET and any item as inputs, then returns a new SET
    with the item removed. Unlike remove, no error is raised if the item is not present.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to remove from."}),
                "item": (IO.ANY, {"tooltip": "The item to remove if present."}),
            }
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("The SET with the item removed (unchanged when it was absent).",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "discard"

    def discard(self, set: set[Any], item: Any) -> tuple[set[Any]]:
        result = set.copy()
        result.discard(item)
        return (result,)


class SetEnumerate(ComfyNodeABC):
    """
    Enumerates elements in a SET.

    This node takes a SET as input and returns a LIST of tuples where each tuple
    contains an index and a value from the SET. The start parameter specifies the
    initial index value (default is 0).

    Note: Since SETs are unordered, the enumeration order is arbitrary but consistent
    within a single operation.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to enumerate."}),
            },
            "optional": {
                "start": ("INT", {"default": 0, "tooltip": "Index value assigned to the first element."}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("enumerated",)
    OUTPUT_TOOLTIPS = ("List of (index, value) pairs. Order is arbitrary but stable within one operation.",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "enumerate_set"

    def enumerate_set(self, set: set[Any], start: int = 0) -> tuple[list]:
        return (list(enumerate(set, start=start)),)


class SetIntersection(ComfyNodeABC):
    """
    Returns the intersection of two or more SETs.

    This node takes multiple SETs as input and returns a new SET containing
    only elements present in all input SETs.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set1": ("SET", {"tooltip": "First SET."}),
                "set2": ("SET", {"tooltip": "Second SET."}),
            },
            "optional": {
                "set3": ("SET", {"tooltip": "Optional additional SET."}),
                "set4": ("SET", {"tooltip": "Optional additional SET."}),
            }
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("Elements present in all of the input SETs.",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "intersection"

    def intersection(self, set1: set[Any], set2: set[Any], set3=None, set4=None) -> tuple[set[Any]]:
        result = set1.copy()
        result.intersection_update(set2)

        if set3 is not None:
            result.intersection_update(set3)

        if set4 is not None:
            result.intersection_update(set4)

        return (result,)


class SetIsDisjoint(ComfyNodeABC):
    """
    Checks if two SETs have no elements in common.

    This node takes two SETs as input and returns True if they have no elements in common.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set1": ("SET", {"tooltip": "First SET."}),
                "set2": ("SET", {"tooltip": "Second SET."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is_disjoint",)
    OUTPUT_TOOLTIPS = ("True when the two SETs share no elements.",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "is_disjoint"

    def is_disjoint(self, set1: set[Any], set2: set[Any]) -> tuple[bool]:
        return (set1.isdisjoint(set2),)


class SetIsSubset(ComfyNodeABC):
    """
    Checks if set1 is a subset of set2.

    This node takes two SETs as input and returns True if set1 is a subset of set2
    (all elements in set1 are also in set2).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set1": ("SET", {"tooltip": "Candidate subset."}),
                "set2": ("SET", {"tooltip": "SET that may contain all of set1's elements."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is_subset",)
    OUTPUT_TOOLTIPS = ("True when every element of set1 is also in set2.",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "is_subset"

    def is_subset(self, set1: set[Any], set2: set[Any]) -> tuple[bool]:
        return (set1.issubset(set2),)


class SetIsSuperset(ComfyNodeABC):
    """
    Checks if set1 is a superset of set2.

    This node takes two SETs as input and returns True if set1 is a superset of set2
    (set1 contains all elements in set2).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set1": ("SET", {"tooltip": "Candidate superset."}),
                "set2": ("SET", {"tooltip": "SET whose elements must all be in set1."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is_superset",)
    OUTPUT_TOOLTIPS = ("True when set1 contains every element of set2.",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "is_superset"

    def is_superset(self, set1: set[Any], set2: set[Any]) -> tuple[bool]:
        return (set1.issuperset(set2),)


class SetLength(ComfyNodeABC):
    """
    Returns the number of items in a SET.

    This node takes a SET as input and returns its length (number of elements) as an integer.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to measure."}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    RETURN_NAMES = ("length",)
    OUTPUT_TOOLTIPS = ("The number of elements in the SET.",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "length"

    def length(self, set: set[Any]) -> tuple[int]:
        return (len(set),)


class SetPop(ComfyNodeABC):
    """
    Removes and returns an arbitrary item from a SET.

    This node takes a SET as input and returns both the new SET
    with an arbitrary item removed and the removed item.
    When the SET is empty, the item is None.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to pop an item from."}),
            }
        }

    RETURN_TYPES = ("SET", IO.ANY)
    RETURN_NAMES = ("set", "item")
    OUTPUT_TOOLTIPS = ("The SET with an arbitrary item removed.", "The removed item (None when the SET was empty).")
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop"

    def pop(self, set: set[Any]) -> tuple[set[Any], Any]:
        result = set.copy()
        try:
            item = result.pop()
            return result, item
        except KeyError:
            return result, None


class SetPopRandom(ComfyNodeABC):
    """
    Removes and returns a random element from a SET.

    This node takes a SET as input and returns the SET with a random element removed
    and the removed element itself. If the SET is empty, it returns None for the element.
    An optional seed can be provided for reproducible selection.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to pop a random element from."}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": True, "tooltip": "Seed for reproducible selection. Leave empty to pick randomly each run."}),
            },
        }

    RETURN_TYPES = ("SET", IO.ANY)
    RETURN_NAMES = ("set", "item")
    OUTPUT_TOOLTIPS = ("The SET with a random element removed.", "The removed element (None when the SET was empty).")
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop_random_element"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        seed = kwargs.get("seed")
        if seed is None:
            return float("NaN")  # Not equal to anything -> trigger recalculation
        return seed

    def pop_random_element(self, set: set[Any], seed=None) -> tuple[set[Any], Any]:
        import random
        rng = random.Random(seed) if seed is not None else random
        result = set.copy()
        if result:
            random_element = rng.choice(list(result))
            result.remove(random_element)
            return result, random_element
        return result, None


class SetRemove(ComfyNodeABC):
    """
    Removes an item from a SET.

    This node takes a SET and any item as inputs, then returns a new SET
    with the item removed and a success indicator. If the item is not present,
    the original SET is returned with success set to False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to remove from."}),
                "item": (IO.ANY, {"tooltip": "The item to remove."}),
            }
        }

    RETURN_TYPES = ("SET", IO.BOOLEAN)
    RETURN_NAMES = ("set", "success")
    OUTPUT_TOOLTIPS = ("The SET with the item removed.", "True when the item was present and removed.")
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "remove"

    def remove(self, set: set[Any], item: Any) -> tuple[set[Any], bool]:
        result = set.copy()
        try:
            result.remove(item)
            return result, True
        except KeyError:
            return result, False


class SetSum(ComfyNodeABC):
    """
    Calculates the sum of all elements in a SET.

    This node takes a SET as input and returns the sum of all its elements.
    The optional start parameter specifies the initial value (default is 0).

    Note: This operation requires all elements to be numeric or otherwise
    compatible with addition. If the SET contains mixed or incompatible types,
    it may raise an error.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET of numbers to sum."}),
            },
            "optional": {
                "start": ("INT", {"default": 0, "tooltip": "Initial value added to the sum."}),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT",)
    RETURN_NAMES = ("sum_int", "sum_float",)
    OUTPUT_TOOLTIPS = ("The total as an integer.", "The total as a float.")
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "sum_set"

    def sum_set(self, set: set[Any], start: int = 0) -> tuple[int, float]:
        result = sum(set, start)
        return result, float(result)


class SetSymmetricDifference(ComfyNodeABC):
    """
    Returns the symmetric difference between two SETs.

    This node takes two SETs as input and returns a new SET containing
    elements in either SET but not in both.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set1": ("SET", {"tooltip": "First SET."}),
                "set2": ("SET", {"tooltip": "Second SET."}),
            }
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("Elements present in exactly one of the two SETs.",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "symmetric_difference"

    def symmetric_difference(self, set1: set[Any], set2: set[Any]) -> tuple[set[Any]]:
        result = set1.copy()
        result.symmetric_difference_update(set2)
        return (result,)


class SetUnion(ComfyNodeABC):
    """
    Returns the union of two or more SETs.

    This node takes multiple SETs as input and returns a new SET containing
    all elements from all the input SETs.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set1": ("SET", {"tooltip": "First SET."}),
                "set2": ("SET", {"tooltip": "Second SET."}),
            },
            "optional": {
                "set3": ("SET", {"tooltip": "Optional additional SET."}),
                "set4": ("SET", {"tooltip": "Optional additional SET."}),
            }
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("All elements from every input SET (duplicates removed).",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "union"

    def union(self, set1: set[Any], set2: set[Any], set3=None, set4=None) -> tuple[set[Any]]:
        result = set1.copy()
        result.update(set2)

        if set3 is not None:
            result.update(set3)

        if set4 is not None:
            result.update(set4)

        return (result,)


class SetToDataList(ComfyNodeABC):
    """
    Converts a SET object into a ComfyUI data list.

    This node takes a SET object (Python set as a single variable) and
    converts it to a ComfyUI data list, allowing its items to be processed
    individually by nodes that accept data lists.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to convert."}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("items",)
    OUTPUT_TOOLTIPS = ("The SET's elements as a ComfyUI data list.",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"
    OUTPUT_IS_LIST = (True,)

    def convert(self, set) -> tuple[list[Any]]:
        return (list(set),)


class SetToList(ComfyNodeABC):
    """
    Converts a SET into a LIST.

    This node takes a SET input and creates a new LIST containing all elements
    from the SET. Note that the order of elements in the resulting LIST is arbitrary
    since SETs are unordered collections.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {"tooltip": "The SET to convert."}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("list",)
    OUTPUT_TOOLTIPS = ("The SET's elements as a Python LIST (order is arbitrary).",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"

    def convert(self, set: set[Any]) -> tuple[list[Any]]:
        return (list(set),)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: SetCreate": SetCreate,
    "Basic data handling: SetCreateFromBoolean": SetCreateFromBoolean,
    "Basic data handling: SetCreateFromFloat": SetCreateFromFloat,
    "Basic data handling: SetCreateFromInt": SetCreateFromInt,
    "Basic data handling: SetCreateFromString": SetCreateFromString,
    "Basic data handling: SetAdd": SetAdd,
    "Basic data handling: SetAll": SetAll,
    "Basic data handling: SetAny": SetAny,
    "Basic data handling: SetContains": SetContains,
    "Basic data handling: SetDifference": SetDifference,
    "Basic data handling: SetDiscard": SetDiscard,
    "Basic data handling: SetEnumerate": SetEnumerate,
    "Basic data handling: SetIntersection": SetIntersection,
    "Basic data handling: SetIsDisjoint": SetIsDisjoint,
    "Basic data handling: SetIsSubset": SetIsSubset,
    "Basic data handling: SetIsSuperset": SetIsSuperset,
    "Basic data handling: SetLength": SetLength,
    "Basic data handling: SetPop": SetPop,
    "Basic data handling: SetPopRandom": SetPopRandom,
    "Basic data handling: SetRemove": SetRemove,
    "Basic data handling: SetSum": SetSum,
    "Basic data handling: SetSymmetricDifference": SetSymmetricDifference,
    "Basic data handling: SetUnion": SetUnion,
    "Basic data handling: SetToDataList": SetToDataList,
    "Basic data handling: SetToList": SetToList,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: SetCreate": "create SET",
    "Basic data handling: SetCreateFromBoolean": "create SET from BOOLEANs",
    "Basic data handling: SetCreateFromFloat": "create SET from FLOATs",
    "Basic data handling: SetCreateFromInt": "create SET from INTs",
    "Basic data handling: SetCreateFromString": "create SET from STRINGs",
    "Basic data handling: SetAdd": "add",
    "Basic data handling: SetAll": "all",
    "Basic data handling: SetAny": "any",
    "Basic data handling: SetContains": "contains",
    "Basic data handling: SetDifference": "difference",
    "Basic data handling: SetDiscard": "discard",
    "Basic data handling: SetEnumerate": "enumerate",
    "Basic data handling: SetIntersection": "intersection",
    "Basic data handling: SetIsDisjoint": "is disjoint",
    "Basic data handling: SetIsSubset": "is subset",
    "Basic data handling: SetIsSuperset": "is superset",
    "Basic data handling: SetLength": "length",
    "Basic data handling: SetPop": "pop",
    "Basic data handling: SetPopRandom": "pop random",
    "Basic data handling: SetRemove": "remove",
    "Basic data handling: SetSum": "sum",
    "Basic data handling: SetSymmetricDifference": "symmetric difference",
    "Basic data handling: SetUnion": "union",
    "Basic data handling: SetToDataList": "convert to Data List",
    "Basic data handling: SetToList": "convert to LIST",
}
