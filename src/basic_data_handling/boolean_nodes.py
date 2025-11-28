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
    Returns the logical AND result of two boolean values.

    This node takes two boolean inputs and returns their logical AND result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": (IO.BOOLEAN, {"default": False, "forceInput": True}),
                "input2": (IO.BOOLEAN, {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "and_operation"

    def and_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (input1 and input2,)


class BooleanNand(ComfyNodeABC):
    """
    Returns the logical NAND result of two boolean values.

    This node takes two boolean inputs and returns their logical NAND result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": (IO.BOOLEAN, {"default": False, "forceInput": True}),
                "input2": (IO.BOOLEAN, {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "nand_operation"

    def nand_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (not (input1 and input2),)


class BooleanNor(ComfyNodeABC):
    """
    Returns the logical NOR result of two boolean values.

    This node takes two boolean inputs and returns their logical NOR result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": (IO.BOOLEAN, {"default": False, "forceInput": True}),
                "input2": (IO.BOOLEAN, {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "nor_operation"

    def nor_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (not (input1 or input2),)


class BooleanNot(ComfyNodeABC):
    """
    Returns the logical NOT result of a boolean value.

    This node takes one boolean input and returns its logical NOT result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.BOOLEAN, {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "not_operation"

    def not_operation(self, input: bool) -> tuple[bool]:
        return (not input,)


class BooleanOr(ComfyNodeABC):
    """
    Returns the logical OR result of two boolean values.

    This node takes two boolean inputs and returns their logical OR result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": (IO.BOOLEAN, {"default": False, "forceInput": True}),
                "input2": (IO.BOOLEAN, {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "or_operation"

    def or_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (input1 or input2,)


class BooleanXor(ComfyNodeABC):
    """
    Returns the logical XOR result of two boolean values.

    This node takes two boolean inputs and returns their logical XOR result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": (IO.BOOLEAN, {"default": False, "forceInput": True}),
                "input2": (IO.BOOLEAN, {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "xor_operation"

    def xor_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (input1 != input2,)


class GenericOr(ComfyNodeABC):
    """
    Returns the logical N/OR result of one or more values.

    This node takes a dynamic number of inputs and returns their logical N/OR result.
    Note that values are evaluated according Python's rules. I.e. an empty string is
    `false`, an integer 0 is also `false`, etc.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "invert": (IO.BOOLEAN, {"default": False}),
            },
            "optional": ContainsDynamicDict({
                "item_0": (IO.ANY, {"_dynamic": "number", "widgetType": "STRING"}),
            })
        }

    RETURN_TYPES = (IO.BOOLEAN,)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "or_operation"

    def or_operation(self, invert: bool, **kwargs: list[Any]) -> tuple[bool]:
        return (any(kwargs.values()) ^ invert,)


class GenericAnd(ComfyNodeABC):
    """
    Returns the logical N/AND result of one or more values.

    This node takes a dynamic number of inputs and returns their logical N/AND result.
    Note that values are evaluated according Python's rules. I.e. an empty string is
    `false`, an integer 0 is also `false`, etc.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "invert": (IO.BOOLEAN, {"default": False}),
            },
            "optional": ContainsDynamicDict({
                "item_0": (IO.ANY, {"_dynamic": "number", "widgetType": "STRING", "default": "True"}),
            })
        }

    RETURN_TYPES = (IO.BOOLEAN,)
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
