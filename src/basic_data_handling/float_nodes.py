from inspect import cleandoc
from comfy.comfy_types.node_typing import IO, ComfyNodeABC


class FloatCreate(ComfyNodeABC):
    """
    Create a FLOAT from a STRING widget.

    The input string must be a valid floating-point number and will be
    directly converted to a FLOAT without any further processing.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.ANY, {"default": "0.0", "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, value: str) -> tuple[float]:
        return (float(value),)


class FloatAdd(ComfyNodeABC):
    """
    Adds two floating-point numbers.

    This node takes two floats as input and returns their sum.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float1": (IO.FLOAT, {"default": 0.0}),
                "float2": (IO.FLOAT, {"default": 0.0}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "add"

    def add(self, float1: float, float2: float) -> tuple[float]:
        return (float1 + float2,)


class FloatSubtract(ComfyNodeABC):
    """
    Subtracts one floating-point number from another.

    This node takes two floats as input and returns the result of subtracting
    the second float from the first.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float1": (IO.FLOAT, {"default": 0.0}),
                "float2": (IO.FLOAT, {"default": 0.0}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "subtract"

    def subtract(self, float1: float, float2: float) -> tuple[float]:
        return (float1 - float2,)


class FloatMultiply(ComfyNodeABC):
    """
    Multiplies two floating-point numbers.

    This node takes two floats as input and returns their product.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float1": (IO.FLOAT, {"default": 1.0}),
                "float2": (IO.FLOAT, {"default": 1.0}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "multiply"

    def multiply(self, float1: float, float2: float) -> tuple[float]:
        return (float1 * float2,)


class FloatDivide(ComfyNodeABC):
    """
    Divides one floating-point number by another.

    This node takes two floats as input and returns the result of division.
    It raises a ValueError if the divisor is 0.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float1": (IO.FLOAT, {"default": 1.0}),
                "float2": (IO.FLOAT, {"default": 1.0}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "divide"

    def divide(self, float1: float, float2: float) -> tuple[float]:
        if float2 == 0.0:
            raise ValueError("Cannot divide by zero.")
        return (float1 / float2,)


class FloatDivideSafe(ComfyNodeABC):
    """
    Divides one floating-point number by another.

    This node takes two floats as input and returns the result of the division.
    It returns positive or negative infinity if the divisor is 0 (assumed to be +0.0).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float1": (IO.FLOAT, {"default": 1.0}),
                "float2": (IO.FLOAT, {"default": 1.0}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "divide"

    def divide(self, float1: float, float2: float) -> tuple[float]:
        if float2 == 0.0:
            return (float('inf') if float1 > 0 else float('-inf'),)
        return (float1 / float2,)


class FloatAsIntegerRatio(ComfyNodeABC):
    """
    Returns the integer ratio of a floating-point number.

    This node takes a floating-point number and returns two integers,
    which represent the ratio as numerator and denominator.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float_value": (IO.FLOAT, {"default": 0.0}),
            }
        }

    RETURN_TYPES = (IO.INT, IO.INT)
    RETURN_NAMES = ("numerator", "denominator")
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "as_integer_ratio"

    def as_integer_ratio(self, float_value: float) -> tuple[int, int]:
        # Decompose the float into numerator and denominator
        numerator, denominator = float_value.as_integer_ratio()
        return numerator, denominator


class FloatFromHex(ComfyNodeABC):
    """
    Converts a hexadecimal string to its corresponding floating-point number.

    This node takes a hexadecimal float string as input and returns the float.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "hex_value": (IO.STRING, {"default": "0x0.0p+0"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "from_hex"

    def from_hex(self, hex_value: str) -> tuple[float]:
        return (float.fromhex(hex_value),)


class FloatHex(ComfyNodeABC):
    """
    Converts a floating-point number to its hexadecimal representation.

    This node takes a float as input and returns its hexadecimal string representation.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float_value": (IO.FLOAT, {"default": 0.0}),
            }
        }

    RETURN_TYPES = (IO.STRING,)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "to_hex"

    def to_hex(self, float_value: float) -> tuple[str]:
        return (float_value.hex(),)


class FloatIsInteger(ComfyNodeABC):
    """
    Checks if a floating-point number is an integer.

    This node takes a floating-point number as input and returns True if the number
    is an integer, otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float_value": (IO.FLOAT, {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "is_integer"

    def is_integer(self, float_value: float) -> tuple[bool]:
        return (float_value.is_integer(),)


class FloatPower(ComfyNodeABC):
    """
    Raises one floating-point number to the power of another.

    This node takes two floats as input and returns the result of raising
    the first float to the power of the second.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base": (IO.FLOAT, {"default": 1.0}),
                "exponent": (IO.FLOAT, {"default": 1.0}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "power"

    def power(self, base: float, exponent: float) -> tuple[float]:
        return (base ** exponent,)


class FloatRound(ComfyNodeABC):
    """
    Rounds a floating-point number to the specified number of decimal places.

    This node takes a float and an integer for decimal places as inputs,
    and returns the rounded result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float_value": (IO.FLOAT, {"default": 0.0}),
                "decimal_places": (IO.INT, {"default": 2, "min": 0}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "round"

    def round(self, float_value: float, decimal_places: int) -> tuple[float]:
        return (round(float_value, decimal_places),)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: FloatCreate": FloatCreate,
    "Basic data handling: FloatAdd": FloatAdd,
    "Basic data handling: FloatSubtract": FloatSubtract,
    "Basic data handling: FloatMultiply": FloatMultiply,
    "Basic data handling: FloatDivide": FloatDivide,
    "Basic data handling: FloatDivideSafe": FloatDivideSafe,
    "Basic data handling: FloatAsIntegerRatio": FloatAsIntegerRatio,
    "Basic data handling: FloatFromHex": FloatFromHex,
    "Basic data handling: FloatHex": FloatHex,
    "Basic data handling: FloatIsInteger": FloatIsInteger,
    "Basic data handling: FloatPower": FloatPower,
    "Basic data handling: FloatRound": FloatRound,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: FloatCreate": "create FLOAT",
    "Basic data handling: FloatAdd": "add",
    "Basic data handling: FloatSubtract": "subtract",
    "Basic data handling: FloatMultiply": "multiply",
    "Basic data handling: FloatDivide": "divide",
    "Basic data handling: FloatDivideSafe": "divide (zero safe)",
    "Basic data handling: FloatAsIntegerRatio": "integer ratio",
    "Basic data handling: FloatFromHex": "from hex",
    "Basic data handling: FloatHex": "to hex",
    "Basic data handling: FloatIsInteger": "is integer",
    "Basic data handling: FloatPower": "power",
    "Basic data handling: FloatRound": "round",
}
