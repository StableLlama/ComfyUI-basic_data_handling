import math
from inspect import cleandoc
from typing import Literal, Union

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

class MathAbs(ComfyNodeABC):
    """
    Returns the absolute value of a number.

    This node takes a number and returns its absolute value (magnitude without sign).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value: Union[float, int, str]) -> tuple[Union[float, int]]:
        return (abs(float(value)),)


class MathAcos(ComfyNodeABC):
    """
    Calculates the arc cosine (inverse cosine) of a value.

    This node takes a value between -1 and 1, and returns the arc cosine in radians or degrees.
    The arc cosine is the inverse operation of cosine, returning the angle whose cosine is the input value.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
                "unit": (["radians", "degrees"], {"default": "degrees"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value: Union[float, int, str], unit: Literal["radians", "degrees"]) -> tuple[float]:
        result = math.acos(float(value))
        if unit == "degrees":
            result = math.degrees(result)
        return (result,)


class MathAsin(ComfyNodeABC):
    """
    Calculates the arc sine (inverse sine) of a value.

    This node takes a value between -1 and 1, and returns the arc sine in radians or degrees.
    The arc sine is the inverse operation of sine, returning the angle whose sine is the input value.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
                "unit": (["radians", "degrees"], {"default": "degrees"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value: Union[float, int, str], unit: Literal["radians", "degrees"]) -> tuple[float]:
        result = math.asin(float(value))
        if unit == "degrees":
            result = math.degrees(result)
        return (result,)


class MathAtan(ComfyNodeABC):
    """
    Calculates the arc tangent (inverse tangent) of a value.

    This node takes a value and returns the arc tangent in radians or degrees.
    The arc tangent is the inverse operation of tangent, returning the angle whose tangent is the input value.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
                "unit": (["radians", "degrees"], {"default": "degrees"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value: Union[float, int, str], unit: Literal["radians", "degrees"]) -> tuple[float]:
        result = math.atan(float(value))
        if unit == "degrees":
            result = math.degrees(result)
        return (result,)


class MathAtan2(ComfyNodeABC):
    """
    Calculates the arc tangent of y/x, considering the quadrant.

    This node takes y and x coordinates and returns the arc tangent in radians or degrees.
    Unlike atan(y/x), this function handles the case where x is zero and correctly determines
    the quadrant of the resulting angle.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "y": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
                "x": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
                "unit": (["radians", "degrees"], {"default": "degrees"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, y: Union[float, int, str], x: Union[float, int, str], unit: Literal["radians", "degrees"]) -> tuple[float]:
        result = math.atan2(float(y), float(x))
        if unit == "degrees":
            result = math.degrees(result)
        return (result,)


class MathCeil(ComfyNodeABC):
    """
    Returns the ceiling of a number.

    This node takes a number and returns the smallest integer greater than or equal to the input value.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value: Union[float, int, str]) -> tuple[int]:
        return (math.ceil(float(value)),)


class MathCos(ComfyNodeABC):
    """
    Calculates the cosine of an angle in radians or degrees.

    This node takes an angle value and unit type, and returns the cosine of that angle.
    The cosine of an angle is the ratio of the length of the adjacent side to the length
    of the hypotenuse in a right-angled triangle.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "angle": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
                "unit": (["radians", "degrees"], {"default": "degrees"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, angle: Union[float, int, str], unit: Literal["radians", "degrees"]) -> tuple[float]:
        if unit == "degrees":
            # Convert degrees to radians
            angle = math.radians(float(angle))
        return (math.cos(float(angle)),)


class MathDegrees(ComfyNodeABC):
    """
    Converts an angle from radians to degrees.

    This node takes an angle in radians and returns the equivalent angle in degrees.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "radians": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, radians: Union[float, int, str]) -> tuple[float]:
        return (math.degrees(float(radians)),)


class MathE(ComfyNodeABC):
    """
    Returns the mathematical constant e.

    This node returns the value of e (Euler's number), which is approximately 2.71828.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self) -> tuple[float]:
        return (math.e,)


class MathExp(ComfyNodeABC):
    """
    Calculates the exponential of a number (e^x).

    This node takes a number and returns e (Euler's number) raised to the power of that number.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value: Union[float, int, str]) -> tuple[float]:
        return (math.exp(float(value)),)


class MathFloor(ComfyNodeABC):
    """
    Returns the floor of a number.

    This node takes a number and returns the largest integer less than or equal to the input value.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = (IO.INT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value: Union[float, int, str]) -> tuple[int]:
        return (math.floor(float(value)),)


class MathLog(ComfyNodeABC):
    """
    Calculates the natural logarithm (base e) of a number.

    This node takes a positive number and returns its natural logarithm.
    If the specified base is not 'e', calculates the logarithm with the specified base.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"default": 1.0, "min": 0.0000001, "widgetType": "STRING"}),
            },
            "optional": {
                "base": (IO.NUMBER, {"default": math.e, "min": 0.0000001, "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value: Union[float, int, str], base: Union[float, int, str] = math.e) -> tuple[float]:
        return (math.log(float(value), float(base)),)


class MathLog10(ComfyNodeABC):
    """
    Calculates the base-10 logarithm of a number.

    This node takes a positive number and returns its base-10 logarithm.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"default": 1.0, "min": 0.0000001, "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value: Union[float, int, str]) -> tuple[float]:
        return (math.log10(float(value)),)


class MathMax(ComfyNodeABC):
    """
    Returns the maximum value among the inputs.

    This node takes two or more values and returns the maximum value among them.
    The function works with both FLOAT and INT types.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
                "value2": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = ("*",)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value1: Union[float, int, str], value2: Union[float, int, str]) -> tuple[Union[float, int]]:
        return (max(float(value1), float(value2)),)


class MathMin(ComfyNodeABC):
    """
    Returns the minimum value among the inputs.

    This node takes two or more values and returns the minimum value among them.
    The function works with both FLOAT and INT types.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value1": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
                "value2": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = ("*",)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value1: Union[float, int, str], value2: Union[float, int, str]) -> tuple[Union[float, int]]:
        return (min(float(value1), float(value2)),)


class MathPi(ComfyNodeABC):
    """
    Returns the mathematical constant π (pi).

    This node returns the value of π, which is approximately 3.14159.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self) -> tuple[float]:
        return (math.pi,)


class MathRadians(ComfyNodeABC):
    """
    Converts an angle from degrees to radians.

    This node takes an angle in degrees and returns the equivalent angle in radians.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "degrees": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, degrees: Union[float, int, str]) -> tuple[float]:
        return (math.radians(float(degrees)),)


class MathSin(ComfyNodeABC):
    """
    Calculates the sine of an angle in radians or degrees.

    This node takes an angle value and unit type, and returns the sine of that angle.
    The sine of an angle is the ratio of the length of the opposite side to the length
    of the hypotenuse in a right-angled triangle.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "angle": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
                "unit": (["radians", "degrees"], {"default": "degrees"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, angle: Union[float, int, str], unit: Literal["radians", "degrees"]) -> tuple[float]:
        if unit == "degrees":
            # Convert degrees to radians
            angle = math.radians(float(angle))
        return (math.sin(float(angle)),)


class MathSqrt(ComfyNodeABC):
    """
    Calculates the square root of a non-negative number.

    This node takes a non-negative number and returns its square root.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.NUMBER, {"default": 0.0, "min": 0.0, "widgetType": "STRING"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, value: Union[float, int, str]) -> tuple[float]:
        return (math.sqrt(float(value)),)


class MathTan(ComfyNodeABC):
    """
    Calculates the tangent of an angle in radians or degrees.

    This node takes an angle value and unit type, and returns the tangent of that angle.
    The tangent of an angle is the ratio of the length of the opposite side to the length
    of the adjacent side in a right-angled triangle.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "angle": (IO.NUMBER, {"default": 0.0, "widgetType": "STRING"}),
                "unit": (["radians", "degrees"], {"default": "degrees"}),
            }
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "calculate"

    def calculate(self, angle: Union[float, int, str], unit: Literal["radians", "degrees"]) -> tuple[float]:
        if unit == "degrees":
            # Convert degrees to radians
            angle = math.radians(float(angle))

        # Handle specific angles that would result in division by zero
        if abs(math.cos(float(angle))) < 1e-10:
            raise ValueError("Tangent is undefined at this angle (division by zero)")

        return (math.tan(float(angle)),)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: MathAbs": MathAbs,
    "Basic data handling: MathAcos": MathAcos,
    "Basic data handling: MathAsin": MathAsin,
    "Basic data handling: MathAtan": MathAtan,
    "Basic data handling: MathAtan2": MathAtan2,
    "Basic data handling: MathCeil": MathCeil,
    "Basic data handling: MathCos": MathCos,
    "Basic data handling: MathDegrees": MathDegrees,
    "Basic data handling: MathE": MathE,
    "Basic data handling: MathExp": MathExp,
    "Basic data handling: MathFloor": MathFloor,
    "Basic data handling: MathLog": MathLog,
    "Basic data handling: MathLog10": MathLog10,
    "Basic data handling: MathMax": MathMax,
    "Basic data handling: MathMin": MathMin,
    "Basic data handling: MathPi": MathPi,
    "Basic data handling: MathRadians": MathRadians,
    "Basic data handling: MathSin": MathSin,
    "Basic data handling: MathSqrt": MathSqrt,
    "Basic data handling: MathTan": MathTan,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: MathAbs": "abs",
    "Basic data handling: MathAcos": "acos",
    "Basic data handling: MathAsin": "asin",
    "Basic data handling: MathAtan": "atan",
    "Basic data handling: MathAtan2": "atan2",
    "Basic data handling: MathCeil": "ceil",
    "Basic data handling: MathCos": "cos",
    "Basic data handling: MathDegrees": "degrees",
    "Basic data handling: MathE": "e (2.71828)",
    "Basic data handling: MathExp": "exp",
    "Basic data handling: MathFloor": "floor",
    "Basic data handling: MathLog": "log",
    "Basic data handling: MathLog10": "log10",
    "Basic data handling: MathMax": "max",
    "Basic data handling: MathMin": "min",
    "Basic data handling: MathPi": "pi (3.14159)",
    "Basic data handling: MathRadians": "radians",
    "Basic data handling: MathSin": "sin",
    "Basic data handling: MathSqrt": "sqrt",
    "Basic data handling: MathTan": "tan",
}
