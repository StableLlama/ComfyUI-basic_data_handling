from typing import Any
from inspect import cleandoc

class SetAdd:
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
                "item": ("*", {}),
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


class SetRemove:
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
                "item": ("*", {}),
            }
        }

    RETURN_TYPES = ("SET", "BOOLEAN")
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


class SetDiscard:
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
                "item": ("*", {}),
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


class SetPop:
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

    RETURN_TYPES = ("SET", "*")
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


class SetClear:
    """
    Removes all items from a SET.

    This node takes a SET as input and returns a new empty SET.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set": ("SET", {}),
            }
        }

    RETURN_TYPES = ("SET",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "clear"

    def clear(self, set: set[Any]) -> tuple[set[Any]]:
        return (set.__class__(),)


class SetUnion:
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


class SetIntersection:
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


class SetDifference:
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


class SetSymmetricDifference:
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


class SetIsSubset:
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

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_subset",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "is_subset"

    def is_subset(self, set1: set[Any], set2: set[Any]) -> tuple[bool]:
        return (set1.issubset(set2),)


class SetIsSuperset:
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

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_superset",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "is_superset"

    def is_superset(self, set1: set[Any], set2: set[Any]) -> tuple[bool]:
        return (set1.issuperset(set2),)


class SetIsDisjoint:
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

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_disjoint",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "is_disjoint"

    def is_disjoint(self, set1: set[Any], set2: set[Any]) -> tuple[bool]:
        return (set1.isdisjoint(set2),)


class SetContains:
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
                "value": ("*", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("contains",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "contains"

    def contains(self, set: set[Any], value: Any) -> tuple[bool]:
        return (value in set,)


class SetLength:
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

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("length",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "length"

    def length(self, set: set[Any]) -> tuple[int]:
        return (len(set),)


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
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"

    def convert(self, list: list[Any]) -> tuple[set[Any]]:
        return (set(list),)


class SetToDataList:
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

    RETURN_TYPES = ("*",)
    CATEGORY = "Basic/SET"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"
    OUTPUT_IS_LIST = (True,)

    def convert(self, set) -> tuple[list[Any]]:
        return (list(set),)


class SetToList:
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
    "SetAdd": SetAdd,
    "SetRemove": SetRemove,
    "SetDiscard": SetDiscard,
    "SetPop": SetPop,
    "SetClear": SetClear,
    "SetUnion": SetUnion,
    "SetIntersection": SetIntersection,
    "SetDifference": SetDifference,
    "SetSymmetricDifference": SetSymmetricDifference,
    "SetIsSubset": SetIsSubset,
    "SetIsSuperset": SetIsSuperset,
    "SetIsDisjoint": SetIsDisjoint,
    "SetContains": SetContains,
    "SetLength": SetLength,
    "SetToDataList": SetToDataList,
    "SetToList": SetToList,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SetAdd": "add",
    "SetRemove": "remove",
    "SetDiscard": "discard",
    "SetPop": "pop",
    "SetClear": "clear",
    "SetUnion": "union",
    "SetIntersection": "intersection",
    "SetDifference": "difference",
    "SetSymmetricDifference": "symmetric_difference",
    "SetIsSubset": "is_subset",
    "SetIsSuperset": "is_superset",
    "SetIsDisjoint": "is_disjoint",
    "SetContains": "contains",
    "SetLength": "length",
    "SetToDataList": "convert to data list",
    "SetToList": "convert to LIST",
}
