from inspect import cleandoc

class BooleanAnd:
    """
    Returns the logical AND result of two boolean values.

    This node takes two boolean inputs and returns their logical AND result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": ("BOOLEAN", {"default": False, "forceInput": True}),
                "input2": ("BOOLEAN", {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "and_operation"

    def and_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (input1 and input2,)


class BooleanOr:
    """
    Returns the logical OR result of two boolean values.

    This node takes two boolean inputs and returns their logical OR result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": ("BOOLEAN", {"default": False, "forceInput": True}),
                "input2": ("BOOLEAN", {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "or_operation"

    def or_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (input1 or input2,)


class BooleanNot:
    """
    Returns the logical NOT result of a boolean value.

    This node takes one boolean input and returns its logical NOT result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("BOOLEAN", {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "not_operation"

    def not_operation(self, input: bool) -> tuple[bool]:
        return (not input,)


class BooleanXor:
    """
    Returns the logical XOR result of two boolean values.

    This node takes two boolean inputs and returns their logical XOR result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": ("BOOLEAN", {"default": False, "forceInput": True}),
                "input2": ("BOOLEAN", {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "xor_operation"

    def xor_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (input1 != input2,)


class BooleanNand:
    """
    Returns the logical NAND result of two boolean values.

    This node takes two boolean inputs and returns their logical NAND result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": ("BOOLEAN", {"default": False, "forceInput": True}),
                "input2": ("BOOLEAN", {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "nand_operation"

    def nand_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (not (input1 and input2),)


class BooleanNor:
    """
    Returns the logical NOR result of two boolean values.

    This node takes two boolean inputs and returns their logical NOR result.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": ("BOOLEAN", {"default": False, "forceInput": True}),
                "input2": ("BOOLEAN", {"default": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    CATEGORY = "Basic/BOOLEAN"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "nor_operation"

    def nor_operation(self, input1: bool, input2: bool) -> tuple[bool]:
        return (not (input1 or input2),)


NODE_CLASS_MAPPINGS = {
    "BooleanAnd": BooleanAnd,
    "BooleanOr": BooleanOr,
    "BooleanNot": BooleanNot,
    "BooleanXor": BooleanXor,
    "BooleanNand": BooleanNand,
    "BooleanNor": BooleanNor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BooleanAnd": "and",
    "BooleanOr": "or",
    "BooleanNot": "not",
    "BooleanXor": "xor",
    "BooleanNand": "nand",
    "BooleanNor": "nor",
}
