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
                "item_0": (IO.ANY, {"_dynamic": "number", "widgetType": "STRING"}),
            })
        }

    RETURN_TYPES = ("SET",)
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
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.BOOLEAN, {"_dynamic": "number", "widgetType": "STRING"}),
            })
        }

    RETURN_TYPES = ("SET",)
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
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.FLOAT, {"_dynamic": "number", "widgetType": "STRING"}),
            })
        }

    RETURN_TYPES = ("SET",)
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
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.INT, {"_dynamic": "number", "widgetType": "STRING"}),
            })
        }

    RETURN_TYPES = ("SET",)
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
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": ContainsDynamicDict({
                "item_0": (IO.STRING, {"_dynamic": "number", "widgetType": "STRING"}),
            })
        }

    RETURN_TYPES = ("SET",)
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
                "set": ("SET", {}),
                "item": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("SET",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "add"

    def add(self, set: set[Any], item: Any) -> tuple[set[Any]]:
        result = set.copy()
        result.add(item)
        return (result,)


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
                "set": ("SET", {}),
                "value": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("contains",)
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
                "set1": ("SET", {}),
                "set2": ("SET", {}),
            }
        }

    RETURN_TYPES = ("SET",)
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
                "set": ("SET", {}),
                "item": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("SET",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "discard"

    def discard(self, set: set[Any], item: Any) -> tuple[set[Any]]:
        result = set.copy()
        result.discard(item)
        return (result,)


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
                "set1": ("SET", {}),
                "set2": ("SET", {}),
            },
            "optional": {
                "set3": ("SET", {}),
                "set4": ("SET", {}),
            }
        }

    RETURN_TYPES = ("SET",)
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
                "set1": ("SET", {}),
                "set2": ("SET", {}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is_disjoint",)
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
                "set1": ("SET", {}),
                "set2": ("SET", {}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is_subset",)
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
                "set1": ("SET", {}),
                "set2": ("SET", {}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is_superset",)
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
                "set": ("SET", {}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    RETURN_NAMES = ("length",)
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
                "set": ("SET", {}),
            }
        }

    RETURN_TYPES = ("SET", IO.ANY)
    RETURN_NAMES = ("set", "item")
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
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {}),
            }
        }

    RETURN_TYPES = ("SET", IO.ANY)
    RETURN_NAMES = ("set", "item")
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "pop_random_element"

    def pop_random_element(self, set: set[Any]) -> tuple[set[Any], Any]:
        import random
        result = set.copy()
        if result:
            random_element = random.choice(list(result))
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
                "set": ("SET", {}),
                "item": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("SET", IO.BOOLEAN)
    RETURN_NAMES = ("set", "success")
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
                "set1": ("SET", {}),
                "set2": ("SET", {}),
            }
        }

    RETURN_TYPES = ("SET",)
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
                "set1": ("SET", {}),
                "set2": ("SET", {}),
            },
            "optional": {
                "set3": ("SET", {}),
                "set4": ("SET", {}),
            }
        }

    RETURN_TYPES = ("SET",)
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
                "set": ("SET", {}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
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
                "set": ("SET", {}),
            }
        }

    RETURN_TYPES = ("LIST",)
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
    "Basic data handling: SetContains": SetContains,
    "Basic data handling: SetDifference": SetDifference,
    "Basic data handling: SetDiscard": SetDiscard,
    "Basic data handling: SetIntersection": SetIntersection,
    "Basic data handling: SetIsDisjoint": SetIsDisjoint,
    "Basic data handling: SetIsSubset": SetIsSubset,
    "Basic data handling: SetIsSuperset": SetIsSuperset,
    "Basic data handling: SetLength": SetLength,
    "Basic data handling: SetPop": SetPop,
    "Basic data handling: SetPopRandom": SetPopRandom,
    "Basic data handling: SetRemove": SetRemove,
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
    "Basic data handling: SetContains": "contains",
    "Basic data handling: SetDifference": "difference",
    "Basic data handling: SetDiscard": "discard",
    "Basic data handling: SetIntersection": "intersection",
    "Basic data handling: SetIsDisjoint": "is disjoint",
    "Basic data handling: SetIsSubset": "is subset",
    "Basic data handling: SetIsSuperset": "is superset",
    "Basic data handling: SetLength": "length",
    "Basic data handling: SetPop": "pop",
    "Basic data handling: SetPopRandom": "pop random",
    "Basic data handling: SetRemove": "remove",
    "Basic data handling: SetSymmetricDifference": "symmetric difference",
    "Basic data handling: SetUnion": "union",
    "Basic data handling: SetToDataList": "convert to Data List",
    "Basic data handling: SetToList": "convert to LIST",
}
