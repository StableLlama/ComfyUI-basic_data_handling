from typing import Any
from inspect import cleandoc
from comfy.comfy_types.node_typing import IO, ComfyNodeABC

class CastToBoolean(ComfyNodeABC):
    """
    Converts any input to a BOOLEAN. Follows standard Python truthy/falsy rules.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {})
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_boolean"

    def convert_to_boolean(self, input: Any) -> tuple[bool]:
        return (bool(input),)


class CastToDict(ComfyNodeABC):
    """
    Converts compatible inputs to a DICT. Input must be a mapping or a list of key-value pairs.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {})
            }
        }

    RETURN_TYPES = ("DICT",)
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
    Converts any numeric input to a FLOAT. Non-numeric or invalid inputs raise a ValueError.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {})
            }
        }

    RETURN_TYPES = ("FLOAT",)
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
    Converts any numeric input to an INT. Non-numeric or invalid inputs raise a ValueError.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {})
            }
        }

    RETURN_TYPES = (IO.INT,)
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
    Converts any input to a LIST. Non-list inputs are wrapped in a list. If input is a ComfyUI data list,
    it converts the individual items into a Python LIST.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {})
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_list"

    def convert_to_list(self, input: Any) -> tuple[list]:
        if isinstance(input, list):
            return (input,)
        return ([input],)


class CastToSet(ComfyNodeABC):
    """
    Converts any input to a SET. Non-set inputs are converted into a set. If input is a ComfyUI data list,
    it casts the individual items into a SET.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {})
            }
        }

    RETURN_TYPES = ("SET",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_set"

    def convert_to_set(self, input: Any) -> tuple[set]:
        if isinstance(input, set):
            return (input,)
        return ({input,} if not isinstance(input, list) else set(input),)


class CastToString(ComfyNodeABC):
    """
    Converts any input to a STRING. Non-string values are converted using str().
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {})
            }
        }

    RETURN_TYPES = (IO.STRING,)
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
