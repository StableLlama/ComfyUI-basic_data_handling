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

class CastToBoolean(ComfyNodeABC):
    """
    Converts any value to a BOOLEAN using Python truthiness.

    Truthy values (non-zero numbers, non-empty strings/lists/dicts/sets) become True;
    falsy values (``0``, ``""``, empty containers, ``None``) become False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {"tooltip": "The value to convert to a BOOLEAN."})
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("boolean",)
    OUTPUT_TOOLTIPS = ("The input value converted to a BOOLEAN.",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_boolean"

    def convert_to_boolean(self, input: Any) -> tuple[bool]:
        return (bool(input),)


class CastToDict(ComfyNodeABC):
    """
    Converts a value into a DICT.

    The input must already be a mapping, or an iterable of key-value pairs (for
    example a LIST of two-element sequences such as ``[["a", 1], ["b", 2]]``).
    Raises a ValueError for any other kind of input.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {"tooltip": "The value to convert to a DICT."})
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dict",)
    OUTPUT_TOOLTIPS = ("The input value converted to a DICT.",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_dict"

    def convert_to_dict(self, input: Any) -> tuple[dict]:
        try:
            return (dict(input),)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert {input} to a DICT. Ensure it is a mapping or list of key-value pairs.")


class CastToFloat(ComfyNodeABC):
    """
    Converts a numeric value to a FLOAT.

    Accepts INT, FLOAT and numeric strings such as ``"3.14"``. Values that cannot be
    parsed as a number raise a ValueError.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {"tooltip": "The value to convert to a FLOAT."})
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float",)
    OUTPUT_TOOLTIPS = ("The input value converted to a FLOAT.",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_float"

    def convert_to_float(self, input: Any) -> tuple[float]:
        try:
            return (float(input),)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert {input} to a FLOAT.")


class CastToInt(ComfyNodeABC):
    """
    Converts a numeric value to an INT, truncating toward zero.

    Accepts INT, FLOAT (fractional part is dropped, like ``int()``) and numeric strings
    such as ``"42"``. Values that cannot be converted raise a ValueError.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {"tooltip": "The value to convert to an INT."})
            }
        }

    RETURN_TYPES = (IO.INT,)
    RETURN_NAMES = ("int",)
    OUTPUT_TOOLTIPS = ("The input value converted to an INT.",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_int"

    def convert_to_int(self, input: Any) -> tuple[int]:
        try:
            return (int(input),)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert {input} to an INT.")


class CastToList(ComfyNodeABC):
    """
    Converts a value into a Python LIST.

    Values that are already a list (including ComfyUI data lists) are returned as-is;
    any other single value is wrapped into a one-element list.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {"tooltip": "The value to convert to a LIST."})
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("list",)
    OUTPUT_TOOLTIPS = ("The input value converted to a LIST.",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_list"

    def convert_to_list(self, input: Any) -> tuple[list]:
        if isinstance(input, list):
            return (input,)
        return ([input],)


class CastToSet(ComfyNodeABC):
    """
    Converts a value into a SET (an unordered collection of unique items).

    Sets are returned unchanged; a list or ComfyUI data list becomes the set of its
    items (duplicates removed); any other single value is wrapped into a one-element set.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {"tooltip": "The value to convert to a SET."})
            }
        }

    RETURN_TYPES = ("SET",)
    RETURN_NAMES = ("set",)
    OUTPUT_TOOLTIPS = ("The input value converted to a SET.",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_set"

    def convert_to_set(self, input: Any) -> tuple[set]:
        if isinstance(input, set):
            return (input,)
        return ({input,} if not isinstance(input, list) else set(input),)


class CastToString(ComfyNodeABC):
    """
    Converts any value to a STRING using its textual representation.

    Numbers, booleans, lists, dicts, sets and other values are rendered with ``str()``,
    matching Python's default formatting.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {"tooltip": "The value to convert to a STRING."})
            }
        }

    RETURN_TYPES = (IO.STRING,)
    RETURN_NAMES = ("string",)
    OUTPUT_TOOLTIPS = ("The input value converted to a STRING.",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_string"

    def convert_to_string(self, input: Any) -> tuple[str]:
        return (str(input),)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: CastToBoolean": CastToBoolean,
    "Basic data handling: CastToDict": CastToDict,
    "Basic data handling: CastToFloat": CastToFloat,
    "Basic data handling: CastToInt": CastToInt,
    "Basic data handling: CastToList": CastToList,
    "Basic data handling: CastToSet": CastToSet,
    "Basic data handling: CastToString": CastToString,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: CastToBoolean": "to BOOLEAN",
    "Basic data handling: CastToDict": "to DICT",
    "Basic data handling: CastToFloat": "to FLOAT",
    "Basic data handling: CastToInt": "to INT",
    "Basic data handling: CastToList": "to LIST",
    "Basic data handling: CastToSet": "to SET",
    "Basic data handling: CastToString": "to STRING",
}
