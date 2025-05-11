from inspect import cleandoc
from typing import Literal
from comfy.comfy_types.node_typing import IO, ComfyNodeABC

class IntAdd(ComfyNodeABC):
    """
    Adds two integers.

    This node takes two integers as input and returns their sum.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": (IO.INT, {"default": 0}),
                "int2": (IO.INT, {"default": 0}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "add"

    def add(self, int1: int, int2: int) -> tuple[int]:
        return (int1 + int2,)


class IntSubtract(ComfyNodeABC):
    """
    Subtracts one integer from another.

    This node takes two integers as input and returns the result of subtracting
    the second integer from the first.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": (IO.INT, {"default": 0}),
                "int2": (IO.INT, {"default": 0}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "subtract"

    def subtract(self, int1: int, int2: int) -> tuple[int]:
        return (int1 - int2,)


class IntMultiply(ComfyNodeABC):
    """
    Multiplies two integers.

    This node takes two integers as input and returns their product.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": (IO.INT, {"default": 1}),
                "int2": (IO.INT, {"default": 1}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "multiply"

    def multiply(self, int1: int, int2: int) -> tuple[int]:
        return (int1 * int2,)


class IntDivide(ComfyNodeABC):
    """
    Divides one integer by another.

    This node takes two integers as input and returns the result of integer
    division. It raises a ValueError if the divisor is 0.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": (IO.INT, {"default": 1}),
                "int2": (IO.INT, {"default": 1}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "divide"

    def divide(self, int1: int, int2: int) -> tuple[int]:
        if int2 == 0:
            raise ValueError("Cannot divide by zero.")
        return (int1 // int2,)


class IntDivideSafe(ComfyNodeABC):
    """
    Divides one integer by another.

    This node takes two integers as input and returns the result of the integer
    division. It returns the positive or negative infinity value if the divisor is 0.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": (IO.INT, {"default": 1}),
                "int2": (IO.INT, {"default": 1}),
                "infinity": (IO.INT, {"default": 9223372036854775807}), # 2**63 - 1
            }
        }

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "divide"

    def divide(self, int1: int, int2: int, infinity: int) -> tuple[int]:
        if int2 == 0:
            return (infinity if int1 > 0 else -infinity,)
        return (int1 // int2,)


class IntModulus(ComfyNodeABC):
    """
    Returns the modulus of two integers.

    This node takes two integers as input and returns the remainder when the
    first integer is divided by the second.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": (IO.INT, {"default": 0}),
                "int2": (IO.INT, {"default": 1}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "modulus"

    def modulus(self, int1: int, int2: int) -> tuple[int]:
        if int2 == 0:
            raise ValueError("Cannot perform modulus operation by zero.")
        return (int1 % int2,)


class IntPower(ComfyNodeABC):
    """
    Raises one integer to the power of another.

    This node takes two integers as input and returns the result of raising
    the first integer to the power of the second.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base": (IO.INT, {"default": 1}),
                "exponent": (IO.INT, {"default": 0}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "power"

    def power(self, base: int, exponent: int) -> tuple[int]:
        return (base**exponent,)


class IntBitLength(ComfyNodeABC):
    """
    Returns the number of bits required to represent an integer in binary.

    This node takes an integer as input and returns the number of bits needed
    to represent it, excluding the sign and leading zeros.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int_value": (IO.INT, {"default": 0}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "bit_length"

    def bit_length(self, int_value: int) -> tuple[int]:
        return (int_value.bit_length(),)


class IntToBytes(ComfyNodeABC):
    """
    Converts an integer to its byte representation.

    This node takes an integer, byte length, and byte order as inputs and
    returns the bytes object representation of the integer.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int_value": (IO.INT, {"default": 0}),
                "length": (IO.INT, {"default": 4, "min": 1}),
                "byteorder": (["big", "little"], {"default": "big"}),
                "signed": (["True", "False"], {"default": "False"}),
            }
        }

    RETURN_TYPES = ("BYTES",)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "to_bytes"

    def to_bytes(self, int_value: int, length: int, byteorder: Literal["big", "little"], signed: Literal["True", "False"]) -> tuple[bytes]:
        signed_bool = (signed == "True")
        return (int_value.to_bytes(length, byteorder=byteorder, signed=signed_bool),)


class IntFromBytes(ComfyNodeABC):
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

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "from_bytes"

    def from_bytes(self, bytes_value, byteorder: Literal["big", "little"], signed: Literal["True", "False"]) -> tuple[int]:
        signed_bool = (signed == "True")
        return (int.from_bytes(bytes_value, byteorder=byteorder, signed=signed_bool),)


class IntBitCount(ComfyNodeABC):
    """
    Returns the number of 1 bits in the binary representation of an integer.

    This node takes an integer as input and returns the count of set bits.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int_value": (IO.INT, {"default": 0}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/INT"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "bit_count"

    def bit_count(self, int_value: int) -> tuple[int]:
        # Introduced in Python 3.10
        return (int_value.bit_count(),)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: IntAdd": IntAdd,
    "Basic data handling: IntSubtract": IntSubtract,
    "Basic data handling: IntMultiply": IntMultiply,
    "Basic data handling: IntDivide": IntDivide,
    "Basic data handling: IntDivideSafe": IntDivideSafe,
    "Basic data handling: IntModulus": IntModulus,
    "Basic data handling: IntPower": IntPower,
    "Basic data handling: IntBitLength": IntBitLength,
    "Basic data handling: IntToBytes": IntToBytes,
    "Basic data handling: IntFromBytes": IntFromBytes,
    "Basic data handling: IntBitCount": IntBitCount,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: IntAdd": "add",
    "Basic data handling: IntSubtract": "subtract",
    "Basic data handling: IntMultiply": "multiply",
    "Basic data handling: IntDivide": "divide",
    "Basic data handling: IntDivideSafe": "divide (division by zero safe)",
    "Basic data handling: IntModulus": "modulus",
    "Basic data handling: IntPower": "power",
    "Basic data handling: IntBitLength": "bit_length",
    "Basic data handling: IntToBytes": "to_bytes",
    "Basic data handling: IntFromBytes": "from_bytes",
    "Basic data handling: IntBitCount": "bit_count",
}

