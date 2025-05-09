from typing import Any
from inspect import cleandoc


class CastToString:
    """
    Converts any input to a STRING. Non-string values are converted using str().
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("*", {})
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_string"

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def convert_to_string(self, input: Any) -> tuple[str]:
        return (str(input),)


class CastToInt:
    """
    Converts any numeric input to an INT. Non-numeric or invalid inputs raise a ValueError.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("*", {})
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_int"

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def convert_to_int(self, input: Any) -> tuple[int]:
        try:
            return (int(input),)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert {input} to an INT.")


class CastToFloat:
    """
    Converts any numeric input to a FLOAT. Non-numeric or invalid inputs raise a ValueError.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("*", {})
            }
        }

    RETURN_TYPES = ("FLOAT",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_float"

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def convert_to_float(self, input: Any) -> tuple[float]:
        try:
            return (float(input),)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert {input} to a FLOAT.")


class CastToBoolean:
    """
    Converts any input to a BOOLEAN. Follows standard Python truthy/falsy rules.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("*", {})
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_boolean"

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def convert_to_boolean(self, input: Any) -> tuple[bool]:
        return (bool(input),)


class CastToList:
    """
    Converts any input to a LIST. Non-list inputs are wrapped in a list. If input is a ComfyUI data list,
    it converts the individual items into a Python LIST.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("*", {})
            }
        }

    RETURN_TYPES = ("LIST",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_list"

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def convert_to_list(self, input: Any) -> tuple[list]:
        if isinstance(input, list):
            return (input,)
        return ([input],)


class CastDataListToList:
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
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"
    INPUT_IS_LIST = True

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def convert(self, **kwargs: dict[str, list]) -> tuple[list[Any]]:
        return (kwargs.get('list', []).copy(),)


class CastToSet:
    """
    Converts any input to a SET. Non-set inputs are converted into a set. If input is a ComfyUI data list,
    it casts the individual items into a SET.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("*", {})
            }
        }

    RETURN_TYPES = ("SET",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_set"

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def convert_to_set(self, input: Any) -> tuple[set]:
        if isinstance(input, set):
            return (input,)
        return ({input,} if not isinstance(input, list) else set(input),)


class CastDataListToSet:
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

    RETURN_TYPES = ("SET",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert"
    INPUT_IS_LIST = True

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def convert(self, **kwargs: dict[str, list]) -> tuple[list[Any]]:
        return (set(kwargs.get('list', [])),)


class CastToDict:
    """
    Converts compatible inputs to a DICT. Input must be a mapping or a list of key-value pairs.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("*", {})
            }
        }

    RETURN_TYPES = ("DICT",)
    CATEGORY = "Basic/cast"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "convert_to_dict"

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def convert_to_dict(self, input: Any) -> tuple[dict]:
        try:
            return (dict(input),)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert {input} to a DICT. Ensure it is a mapping or list of key-value pairs.")


NODE_CLASS_MAPPINGS = {
    "CastToString": CastToString,
    "CastToInt": CastToInt,
    "CastToFloat": CastToFloat,
    "CastToBoolean": CastToBoolean,
    "CastToList": CastToList,
    "CastDataListToList": CastDataListToList,
    "CastToSet": CastToSet,
    "CastDataListToSet": CastDataListToSet,
    "CastToDict": CastToDict,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CastToString": "to STRING",
    "CastToInt": "to INT",
    "CastToFloat": "to FLOAT",
    "CastToBoolean": "to BOOLEAN",
    "CastToList": "to LIST",
    "CastDataListToList": "data list to LIST",
    "CastToSet": "to SET",
    "CastDataListToSet": "data list to SET",
    "CastToDict": "to DICT",
}
