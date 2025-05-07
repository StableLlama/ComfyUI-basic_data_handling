from inspect import cleandoc

class FloatAdd:
    """
    Adds two floating-point numbers.

    This node takes two floats as input and returns their sum.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float1": ("FLOAT", {"default": 0.0}),
                "float2": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "add"

    def add(self, float1: float, float2: float) -> tuple[float]:
        return (float1 + float2,)


class FloatSubtract:
    """
    Subtracts one floating-point number from another.

    This node takes two floats as input and returns the result of subtracting
    the second float from the first.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float1": ("FLOAT", {"default": 0.0}),
                "float2": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "subtract"

    def subtract(self, float1: float, float2: float) -> tuple[float]:
        return (float1 - float2,)


class FloatMultiply:
    """
    Multiplies two floating-point numbers.

    This node takes two floats as input and returns their product.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float1": ("FLOAT", {"default": 1.0}),
                "float2": ("FLOAT", {"default": 1.0}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "multiply"

    def multiply(self, float1: float, float2: float) -> tuple[float]:
        return (float1 * float2,)


class FloatDivide:
    """
    Divides one floating-point number by another.

    This node takes two floats as input and returns the result of division.
    It raises a ValueError if the divisor is 0.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float1": ("FLOAT", {"default": 1.0}),
                "float2": ("FLOAT", {"default": 1.0}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "divide"

    def divide(self, float1: float, float2: float) -> tuple[float]:
        if float2 == 0.0:
            raise ValueError("Cannot divide by zero.")
        return (float1 / float2,)


class FloatPower:
    """
    Raises one floating-point number to the power of another.

    This node takes two floats as input and returns the result of raising
    the first float to the power of the second.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base": ("FLOAT", {"default": 1.0}),
                "exponent": ("FLOAT", {"default": 1.0}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "power"

    def power(self, base: float, exponent: float) -> tuple[float]:
        return (base ** exponent,)


class FloatRound:
    """
    Rounds a floating-point number to the specified number of decimal places.

    This node takes a float and an integer for decimal places as inputs,
    and returns the rounded result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float_value": ("FLOAT", {"default": 0.0}),
                "decimal_places": ("INT", {"default": 2, "min": 0}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "round"

    def round(self, float_value: float, decimal_places: int) -> tuple[float]:
        return (round(float_value, decimal_places),)


class FloatIsInteger:
    """
    Checks if a floating-point number is an integer.

    This node takes a floating-point number as input and returns True if the number
    is an integer, otherwise False.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float_value": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "is_integer"

    def is_integer(self, float_value: float) -> tuple[bool]:
        return (float_value.is_integer(),)


class FloatAsIntegerRatio:
    """
    Returns the integer ratio of a floating-point number.

    This node takes a floating-point number and returns two integers,
    which represent the ratio as numerator and denominator.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float_value": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("numerator", "denominator")
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "as_integer_ratio"

    def as_integer_ratio(self, float_value: float) -> tuple[int, int]:
        # Decompose the float into numerator and denominator
        numerator, denominator = float_value.as_integer_ratio()
        return numerator, denominator


class FloatHex:
    """
    Converts a floating-point number to its hexadecimal representation.

    This node takes a float as input and returns its hexadecimal string representation.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float_value": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("STRING",)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "to_hex"

    def to_hex(self, float_value: float) -> tuple[str]:
        return (float_value.hex(),)


class FloatFromHex:
    """
    Converts a hexadecimal string to its corresponding floating-point number.

    This node takes a hexadecimal float string as input and returns the float.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "hex_value": ("STRING", {"default": "0x0.0p+0"}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    CATEGORY = "Basic/FLOAT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "from_hex"

    def from_hex(self, hex_value: str) -> tuple[float]:
        return (float.fromhex(hex_value),)


NODE_CLASS_MAPPINGS = {
    "FloatAdd": FloatAdd,
    "FloatSubtract": FloatSubtract,
    "FloatMultiply": FloatMultiply,
    "FloatDivide": FloatDivide,
    "FloatPower": FloatPower,
    "FloatRound": FloatRound,
    "FloatIsInteger": FloatIsInteger,
    "FloatAsIntegerRatio": FloatAsIntegerRatio,
    "FloatHex": FloatHex,
    "FloatFromHex": FloatFromHex,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FloatAdd": "add",
    "FloatSubtract": "subtract",
    "FloatMultiply": "multiply",
    "FloatDivide": "divide",
    "FloatPower": "power",
    "FloatRound": "round",
    "FloatIsInteger": "is_integer",
    "FloatAsIntegerRatio": "as_integer_ratio",
    "FloatHex": "to_hex",
    "FloatFromHex": "from_hex",
}
