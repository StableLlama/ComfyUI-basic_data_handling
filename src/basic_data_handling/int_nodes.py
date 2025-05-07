from inspect import cleandoc
from typing import Literal


class IntAdd:
    """
    Adds two integers.

    This node takes two integers as input and returns their sum.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": ("INT", {"default": 0}),
                "int2": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "add"

    def add(self, int1: int, int2: int) -> tuple[int]:
        return (int1 + int2,)


class IntSubtract:
    """
    Subtracts one integer from another.

    This node takes two integers as input and returns the result of subtracting
    the second integer from the first.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": ("INT", {"default": 0}),
                "int2": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "subtract"

    def subtract(self, int1: int, int2: int) -> tuple[int]:
        return (int1 - int2,)


class IntMultiply:
    """
    Multiplies two integers.

    This node takes two integers as input and returns their product.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": ("INT", {"default": 1}),
                "int2": ("INT", {"default": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "multiply"

    def multiply(self, int1: int, int2: int) -> tuple[int]:
        return (int1 * int2,)


class IntDivide:
    """
    Divides one integer by another.

    This node takes two integers as input and returns the result of integer
    division. It raises a ValueError if the divisor is 0.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": ("INT", {"default": 1}),
                "int2": ("INT", {"default": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "divide"

    def divide(self, int1: int, int2: int) -> tuple[int]:
        if int2 == 0:
            raise ValueError("Cannot divide by zero.")
        return (int1 // int2,)


class IntModulus:
    """
    Returns the modulus of two integers.

    This node takes two integers as input and returns the remainder when the
    first integer is divided by the second.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": ("INT", {"default": 0}),
                "int2": ("INT", {"default": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "modulus"

    def modulus(self, int1: int, int2: int) -> tuple[int]:
        if int2 == 0:
            raise ValueError("Cannot perform modulus operation by zero.")
        return (int1 % int2,)


class IntPower:
    """
    Raises one integer to the power of another.

    This node takes two integers as input and returns the result of raising
    the first integer to the power of the second.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base": ("INT", {"default": 1}),
                "exponent": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "power"

    def power(self, base: int, exponent: int) -> tuple[int]:
        return (base**exponent,)


class IntBitLength:
    """
    Returns the number of bits required to represent an integer in binary.

    This node takes an integer as input and returns the number of bits needed
    to represent it, excluding the sign and leading zeros.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int_value": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Additional Methods/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "bit_length"

    def bit_length(self, int_value: int) -> tuple[int]:
        return (int_value.bit_length(),)


class IntToBytes:
    """
    Converts an integer to its byte representation.

    This node takes an integer, byte length, and byte order as inputs and
    returns the bytes object representation of the integer.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int_value": ("INT", {"default": 0}),
                "length": ("INT", {"default": 4, "min": 1}),
                "byteorder": (["big", "little"], {"default": "big"}),
                "signed": (["True", "False"], {"default": "False"}),
            }
        }

    RETURN_TYPES = ("BYTES",)
    CATEGORY = "Additional Methods/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "to_bytes"

    def to_bytes(self, int_value: int, length: int, byteorder: Literal["big"|"little"], signed: Literal["True"|"False"]) -> tuple[int]:
        signed_bool = (signed == "True")
        return (int_value.to_bytes(length, byteorder=byteorder, signed=signed_bool),)


class IntFromBytes:
    """
    Converts a bytes object to an integer.

    This class method takes bytes, byte order, and signed flag as inputs and
    returns an integer.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bytes_value": ("BYTES", {}),
                "byteorder": (["big", "little"], {"default": "big"}),
                "signed": (["True", "False"], {"default": "False"}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Additional Methods/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "from_bytes"

    def from_bytes(self, bytes_value, byteorder: Literal["big"|"little"], signed: Literal["True"|"False"]) -> tuple[int]:
        signed_bool = (signed == "True")
        return (int.from_bytes(bytes_value, byteorder=byteorder, signed=signed_bool),)


class IntBitCount:
    """
    Returns the number of 1 bits in the binary representation of an integer.

    This node takes an integer as input and returns the count of set bits.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int_value": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("INT",)
    CATEGORY = "Additional Methods/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "bit_count"

    def bit_count(self, int_value: int) -> tuple[int]:
        # Introduced in Python 3.10
        return (int_value.bit_count(),)


NODE_CLASS_MAPPINGS = {
    "IntAdd": IntAdd,
    "IntSubtract": IntSubtract,
    "IntMultiply": IntMultiply,
    "IntDivide": IntDivide,
    "IntModulus": IntModulus,
    "IntPower": IntPower,
    "IntBitLength": IntBitLength,
    "IntToBytes": IntToBytes,
    "IntFromBytes": IntFromBytes,
    "IntBitCount": IntBitCount,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IntAdd": "add",
    "IntSubtract": "subtract",
    "IntMultiply": "multiply",
    "IntDivide": "divide",
    "IntModulus": "modulus",
    "IntPower": "power",
    "IntBitLength": "bit_length",
    "IntToBytes": "to_bytes",
    "IntFromBytes": "from_bytes",
    "IntBitCount": "bit_count",
}

