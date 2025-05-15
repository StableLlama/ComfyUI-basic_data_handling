from typing import Any
from inspect import cleandoc
from comfy.comfy_types.node_typing import IO, ComfyNodeABC

class Equal(ComfyNodeABC):
    """
    Checks if two values are equal.

    This node takes two inputs of any type and returns True if they are equal,
    and False otherwise. For complex objects, structural equality is tested.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.ANY, {}),
                "value2": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, value1: Any, value2: Any) -> tuple[bool]:
        return (value1 == value2,)


class NotEqual(ComfyNodeABC):
    """
    Checks if two values are not equal.

    This node takes two inputs of any type and returns True if they are not equal,
    and False otherwise. For complex objects, structural inequality is tested.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.ANY, {}),
                "value2": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def compare(self, value1: Any, value2: Any) -> tuple[bool]:
        return (value1 != value2,)


class LessThan:
    """
    Checks if the first value is less than the second.

    This node takes two numerical inputs and returns True if the first value
    is less than the second value, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.NUMBER, {"widgetType": "FLOAT"}),
                "value2": (IO.NUMBER, {"widgetType": "FLOAT"}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, value1: float, value2: float) -> tuple[bool]:
        return (value1 < value2,)


class LessThanOrEqual:
    """
    Checks if the first value is less than or equal to the second.

    This node takes two numerical inputs and returns True if the first value
    is less than or equal to the second value, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.NUMBER, {"widgetType": "FLOAT"}),
                "value2": (IO.NUMBER, {"widgetType": "FLOAT"}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, value1: float, value2: float) -> tuple[bool]:
        return (value1 <= value2,)


class GreaterThan:
    """
    Checks if the first value is greater than the second.

    This node takes two numerical inputs and returns True if the first value
    is greater than the second value, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.NUMBER, {"widgetType": "FLOAT"}),
                "value2": (IO.NUMBER, {"widgetType": "FLOAT"}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, value1: float, value2: float) -> tuple[bool]:
        return (value1 > value2,)


class GreaterThanOrEqual:
    """
    Checks if the first value is greater than or equal to the second.

    This node takes two numerical inputs and returns True if the first value
    is greater than or equal to the second value, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.NUMBER, {"widgetType": "FLOAT"}),
                "value2": (IO.NUMBER, {"widgetType": "FLOAT"}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, value1: float, value2: float) -> tuple[bool]:
        return (value1 >= value2,)


class IsNull:
    """
    Checks if a value is None/null.

    This node takes any input value and returns True if the value is None,
    and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is_null",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_null"

    def check_null(self, value: Any) -> tuple[bool]:
        return (value is None,)


class NumberInRange:
    """
    Checks if a number is within a specified range.

    This node takes a number and range bounds, and returns True if the number
    is within the specified range, and False otherwise. The user can specify
    whether the bounds are inclusive or exclusive.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"widgetType": "FLOAT"}),
                "min_value": ("FLOAT", {"default": 0}),
                "max_value": ("FLOAT", {"default": 100}),
            },
            "optional": {
                "include_min": (IO.BOOLEAN, {"default": "True"}),
                "include_max": (IO.BOOLEAN, {"default": "True"}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("in_range",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_range"

    def check_range(self, value: float, min_value: float, max_value: float,
                    include_min: str = "True", include_max: str = "True") -> tuple[bool]:
        min_check = value >= min_value if include_min == "True" else value > min_value
        max_check = value <= max_value if include_max == "True" else value < max_value

        return (min_check and max_check,)


class CompareLength:
    """
    Compares the length of a container (string, list, etc) with a value.

    This node takes a container and a comparison value, and returns a boolean
    result based on the comparison of the container's length with the value.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "container": (IO.ANY, {}),
                "operator": (["==", "!=", ">", "<", ">=", "<="], {"default": "=="}),
                "length": (IO.INT, {"default": 0, "min": 0}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN, IO.INT)
    RETURN_NAMES = ("result", "actual_length")
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare_length"

    def compare_length(self, container: Any, operator: str, length: int) -> tuple[bool, int]:
        try:
            actual_length = len(container)
        except (TypeError, AttributeError):
            # If the object doesn't have a length, return False and -1
            return False, -1

        if operator == "==":
            return (actual_length == length, actual_length)
        elif operator == "!=":
            return (actual_length != length, actual_length)
        elif operator == ">":
            return (actual_length > length, actual_length)
        elif operator == "<":
            return (actual_length < length, actual_length)
        elif operator == ">=":
            return (actual_length >= length, actual_length)
        elif operator == "<=":
            return (actual_length <= length, actual_length)
        else:
            raise ValueError(f"Unknown operator: {operator}")


class StringComparison:
    """
    Compares two strings using a selected comparison operator.

    This node takes two string inputs and a comparison operator, and returns
    a boolean result based on the selected comparison.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string1": ("STRING", {"default": ""}),
                "string2": ("STRING", {"default": ""}),
                "operator": (["==", "!=", ">", "<", ">=", "<="], {"default": "=="}),
                "case_sensitive": (IO.BOOLEAN, {"default": True}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, string1: str, string2: str, operator: str, case_sensitive: str) -> tuple[bool]:
        if case_sensitive == "False":
            string1 = string1.lower()
            string2 = string2.lower()

        if operator == "==":
            return (string1 == string2,)
        elif operator == "!=":
            return (string1 != string2,)
        elif operator == ">":
            return (string1 > string2,)
        elif operator == "<":
            return (string1 < string2,)
        elif operator == ">=":
            return (string1 >= string2,)
        elif operator == "<=":
            return (string1 <= string2,)
        else:
            raise ValueError(f"Unknown operator: {operator}")


NODE_CLASS_MAPPINGS = {
    "Basic data handling: Equal": Equal,
    "Basic data handling: NotEqual": NotEqual,
    "Basic data handling: LessThan": LessThan,
    "Basic data handling: LessThanOrEqual": LessThanOrEqual,
    "Basic data handling: GreaterThan": GreaterThan,
    "Basic data handling: GreaterThanOrEqual": GreaterThanOrEqual,
    "Basic data handling: IsNull": IsNull,
    "Basic data handling: NumberInRange": NumberInRange,
    "Basic data handling: CompareLength": CompareLength,
    "Basic data handling: StringComparison": StringComparison,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: Equal": "==",
    "Basic data handling: NotEqual": "!=",
    "Basic data handling: LessThan": "<",
    "Basic data handling: LessThanOrEqual": "<=",
    "Basic data handling: GreaterThan": ">",
    "Basic data handling: GreaterThanOrEqual": ">=",
    "Basic data handling: IsNull": "is null",
    "Basic data handling: NumberInRange": "in range",
    "Basic data handling: CompareLength": "compare length",
    "Basic data handling: StringComparison": "string compare",
}
