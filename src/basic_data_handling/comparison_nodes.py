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

class Equal(ComfyNodeABC):
    """
    Checks if two values are equal.

    This node takes two inputs of any type and returns True if they are equal,
    and False otherwise. For complex objects (lists, dicts, sets), structural
    equality is tested.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.ANY, {"tooltip": "First value to compare."}),
                "value2": (IO.ANY, {"tooltip": "Second value to compare."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when the two values are equal, otherwise False.",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, value1: Any, value2: Any) -> tuple[bool]:
        return (value1 == value2,)


class NotEqual(ComfyNodeABC):
    """
    Checks if two values are not equal.

    This node takes two inputs of any type and returns True if they are not equal,
    and False otherwise. For complex objects (lists, dicts, sets), structural
    inequality is tested.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.ANY, {"tooltip": "First value to compare."}),
                "value2": (IO.ANY, {"tooltip": "Second value to compare."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when the two values are not equal, otherwise False.",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool:
        return True

    def compare(self, value1: Any, value2: Any) -> tuple[bool]:
        return (value1 != value2,)


class LessThan(ComfyNodeABC):
    """
    Checks if the first value is less than the second.

    This node takes two numerical inputs and returns True if the first value
    is strictly less than the second value, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.NUMBER, {"widgetType": "FLOAT", "tooltip": "Left-hand operand of the comparison."}),
                "value2": (IO.NUMBER, {"widgetType": "FLOAT", "tooltip": "Right-hand operand of the comparison."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when value1 is strictly less than value2, otherwise False.",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, value1: float, value2: float) -> tuple[bool]:
        return (value1 < value2,)


class LessThanOrEqual(ComfyNodeABC):
    """
    Checks if the first value is less than or equal to the second.

    This node takes two numerical inputs and returns True if the first value
    is less than or equal to the second value, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.NUMBER, {"widgetType": "FLOAT", "tooltip": "Left-hand operand of the comparison."}),
                "value2": (IO.NUMBER, {"widgetType": "FLOAT", "tooltip": "Right-hand operand of the comparison."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when value1 is less than or equal to value2, otherwise False.",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, value1: float, value2: float) -> tuple[bool]:
        return (value1 <= value2,)


class GreaterThan(ComfyNodeABC):
    """
    Checks if the first value is greater than the second.

    This node takes two numerical inputs and returns True if the first value
    is strictly greater than the second value, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.NUMBER, {"widgetType": "FLOAT", "tooltip": "Left-hand operand of the comparison."}),
                "value2": (IO.NUMBER, {"widgetType": "FLOAT", "tooltip": "Right-hand operand of the comparison."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when value1 is strictly greater than value2, otherwise False.",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, value1: float, value2: float) -> tuple[bool]:
        return (value1 > value2,)


class GreaterThanOrEqual(ComfyNodeABC):
    """
    Checks if the first value is greater than or equal to the second.

    This node takes two numerical inputs and returns True if the first value
    is greater than or equal to the second value, and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.NUMBER, {"widgetType": "FLOAT", "tooltip": "Left-hand operand of the comparison."}),
                "value2": (IO.NUMBER, {"widgetType": "FLOAT", "tooltip": "Right-hand operand of the comparison."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when value1 is greater than or equal to value2, otherwise False.",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "compare"

    def compare(self, value1: float, value2: float) -> tuple[bool]:
        return (value1 >= value2,)


class IsNull(ComfyNodeABC):
    """
    Checks if a value is None/null.

    This node takes any input value and returns True if the value is None
    (Python null), and False otherwise.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.ANY, {"tooltip": "The value to test for null."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("is_null",)
    OUTPUT_TOOLTIPS = ("True when the input value is None, otherwise False.",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_null"

    def check_null(self, value: Any) -> tuple[bool]:
        return (value is None,)


class NumberInRange(ComfyNodeABC):
    """
    Checks if a number is within a specified range.

    This node takes a number, a minimum and a maximum bound, and returns True if the
    number lies within the range. The ``include_min`` and ``include_max`` options control
    whether the boundaries themselves count as being inside the range.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"widgetType": "FLOAT", "tooltip": "The number to test."}),
                "min_value": ("FLOAT", {"default": 0, "tooltip": "Lower bound of the range."}),
                "max_value": ("FLOAT", {"default": 100, "tooltip": "Upper bound of the range."}),
            },
            "optional": {
                "include_min": (IO.BOOLEAN, {"default": "True", "tooltip": "Treat the lower bound as inside the range (>=)."}),
                "include_max": (IO.BOOLEAN, {"default": "True", "tooltip": "Treat the upper bound as inside the range (<=)."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("in_range",)
    OUTPUT_TOOLTIPS = ("True when the number lies within the configured range.",)
    CATEGORY = "Basic/comparison"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "check_range"

    def check_range(self, value: float, min_value: float, max_value: float,
                    include_min: str = "True", include_max: str = "True") -> tuple[bool]:
        min_check = value >= min_value if include_min == "True" else value > min_value
        max_check = value <= max_value if include_max == "True" else value < max_value

        return (min_check and max_check,)


class CompareLength(ComfyNodeABC):
    """
    Compares the length of a container (string, list, dict, set, ...) with a value.

    This node measures ``len(container)`` and compares it with *length* using the
    selected *operator*. Returns the boolean result and, as a convenience, the
    actual measured length.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "container": (IO.ANY, {"tooltip": "The object whose length is measured (string, list, dict, set, ...)."}),
                "operator": (["==", "!=", ">", "<", ">=", "<="], {"default": "==", "tooltip": "Comparison operator applied between the length and the given value."}),
                "length": (IO.INT, {"default": 0, "min": 0, "tooltip": "The value the measured length is compared against."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN, IO.INT)
    RETURN_NAMES = ("result", "actual_length")
    OUTPUT_TOOLTIPS = ("Result of evaluating length <operator> value.", "The measured length of the container (-1 when it has no length).")
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


class StringComparison(ComfyNodeABC):
    """
    Compares two strings using a selected comparison operator.

    This node takes two string inputs and an operator, and returns True when the
    comparison holds. Comparisons are lexicographic (dictionary order); enable
    *case_sensitive* to treat uppercase and lowercase letters as distinct.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string1": ("STRING", {"default": "", "tooltip": "First string to compare."}),
                "string2": ("STRING", {"default": "", "tooltip": "Second string to compare."}),
                "operator": (["==", "!=", ">", "<", ">=", "<="], {"default": "==", "tooltip": "Comparison operator applied between the two strings."}),
                "case_sensitive": (IO.BOOLEAN, {"default": True, "tooltip": "When enabled, letter case is respected (e.g. 'A' != 'a')."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when the selected comparison holds between the two strings.",)
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
