from inspect import cleandoc
from typing import Any

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

from ._dynamic_input import ContainsDynamicDict


class BooleanAnd(ComfyNodeABC):
    """
    Returns the logical AND (conjunction) of two boolean values.

    Outputs True only when both inputs are True. This matches the behaviour of the
    Python ``and`` operator applied to the two operands.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": (IO.BOOLEAN, {"default": False, "forceInput": True, "tooltip": "First operand."}),
                "input2": (IO.BOOLEAN, {"default": False, "forceInput": True, "tooltip": "Second operand."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True only when both inputs are True, otherwise False.",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "and_operation"

    def and_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (input1 and input2,)


class BooleanNand(ComfyNodeABC):
    """
    Returns the logical NAND of two boolean values.

    Outputs False only when both inputs are True; it is the negation of AND.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": (IO.BOOLEAN, {"default": False, "forceInput": True, "tooltip": "First operand."}),
                "input2": (IO.BOOLEAN, {"default": False, "forceInput": True, "tooltip": "Second operand."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("False only when both inputs are True, otherwise True.",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "nand_operation"

    def nand_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (not (input1 and input2),)


class BooleanNor(ComfyNodeABC):
    """
    Returns the logical NOR of two boolean values.

    Outputs True only when both inputs are False; it is the negation of OR.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": (IO.BOOLEAN, {"default": False, "forceInput": True, "tooltip": "First operand."}),
                "input2": (IO.BOOLEAN, {"default": False, "forceInput": True, "tooltip": "Second operand."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True only when both inputs are False, otherwise False.",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "nor_operation"

    def nor_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (not (input1 or input2),)


class BooleanNot(ComfyNodeABC):
    """
    Returns the logical NOT (negation) of a boolean value.

    Outputs True when the input is False and False when the input is True.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.BOOLEAN, {"default": False, "forceInput": True, "tooltip": "The value to negate."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when the input is False, False when the input is True.",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "not_operation"

    def not_operation(self, input: bool) -> tuple[bool]:
        return (not input,)


class BooleanOr(ComfyNodeABC):
    """
    Returns the logical OR (disjunction) of two boolean values.

    Outputs True when at least one input is True. This matches the behaviour of the
    Python ``or`` operator applied to the two operands.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": (IO.BOOLEAN, {"default": False, "forceInput": True, "tooltip": "First operand."}),
                "input2": (IO.BOOLEAN, {"default": False, "forceInput": True, "tooltip": "Second operand."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when at least one input is True, otherwise False.",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "or_operation"

    def or_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (input1 or input2,)


class BooleanXor(ComfyNodeABC):
    """
    Returns the logical XOR (exclusive or) of two boolean values.

    Outputs True when the inputs differ from one another and False when they are equal.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": (IO.BOOLEAN, {"default": False, "forceInput": True, "tooltip": "First operand."}),
                "input2": (IO.BOOLEAN, {"default": False, "forceInput": True, "tooltip": "Second operand."}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when the two inputs differ, False when they are equal.",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "xor_operation"

    def xor_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (input1 != input2,)


class GenericOr(ComfyNodeABC):
    """
    Returns the OR of any number of values, evaluated with Python truthiness.

    Connect additional values to the dynamic item input to add more operands. Because
    Python truthiness is used, values such as ``0``, ``""``, ``[]``, ``{}`` and ``None``
    count as False. When *invert* is enabled the result is negated (NOR).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "invert": (IO.BOOLEAN, {"default": False, "tooltip": "When enabled, negates the result (turns OR into NOR)."}),
            },
            "optional": ContainsDynamicDict({
                "item_0": (IO.ANY, {"_dynamic": "number", "widgetType": "STRING", "tooltip": "One of the values to combine. Connect more values to add operands."}),
            })
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when at least one connected value is truthy (unless inverted).",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "or_operation"

    def or_operation(self, invert: bool, **kwargs: list[Any]) -> tuple[bool]:
        return (any(kwargs.values()) ^ invert,)


class GenericAnd(ComfyNodeABC):
    """
    Returns the AND of any number of values, evaluated with Python truthiness.

    Connect additional values to the dynamic item input to add more operands. Because
    Python truthiness is used, values such as ``0``, ``""``, ``[]``, ``{}`` and ``None``
    count as False. When *invert* is enabled the result is negated (NAND).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "invert": (IO.BOOLEAN, {"default": False, "tooltip": "When enabled, negates the result (turns AND into NAND)."}),
            },
            "optional": ContainsDynamicDict({
                "item_0": (IO.ANY, {"_dynamic": "number", "widgetType": "STRING", "default": "True", "tooltip": "One of the values to combine. Connect more values to add operands."}),
            })
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    RETURN_NAMES = ("result",)
    OUTPUT_TOOLTIPS = ("True when all connected values are truthy (unless inverted).",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "and_operation"

    def and_operation(self, invert: bool, **kwargs: list[Any]) -> tuple[bool]:
        return (all(kwargs.values()) ^ invert,)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: Boolean And": BooleanAnd,
    "Basic data handling: Generic And": GenericAnd,
    "Basic data handling: Boolean Nand": BooleanNand,
    "Basic data handling: Boolean Nor": BooleanNor,
    "Basic data handling: Boolean Not": BooleanNot,
    "Basic data handling: Boolean Or": BooleanOr,
    "Basic data handling: Generic Or": GenericOr,
    "Basic data handling: Boolean Xor": BooleanXor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: Boolean And": "and",
    "Basic data handling: Generic And": "and (generic)",
    "Basic data handling: Boolean Nand": "nand",
    "Basic data handling: Boolean Nor": "nor",
    "Basic data handling: Boolean Not": "not",
    "Basic data handling: Boolean Or": "or",
    "Basic data handling: Generic Or": "or (generic)",
    "Basic data handling: Boolean Xor": "xor",
}
