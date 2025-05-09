from typing import Any
from inspect import cleandoc

class IfElse:
    """
    Implements a conditional branch (if/else) in the workflow.

    This node takes a condition input and two value inputs. If the condition
    evaluates to True, the first value is returned; otherwise, the second value
    is returned. This allows conditional data flow in ComfyUI workflows.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "condition": ("BOOLEAN", {}),
                "if_true": ("*", {"lazy": True}),
                "if_false": ("*", {"lazy": True}),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/Flow Control"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "execute"

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool|str:
        if input_types["condition"] not in ("BOOLEAN"):
            return "condition must be a BOOLEAN type"
        return True

    def check_lazy_status(self, condition: bool, if_true: Any, if_false: Any) -> list[str]:
        needed = []
        if if_true is None and condition is True:
            needed.append("if_true")
        if if_false is None and condition is False:
            needed.append("if_false")
        return needed

    def execute(self, condition: bool, if_true: Any, if_false: Any) -> tuple[Any]:
        return (if_true if condition else if_false,)


class SwitchCase:
    """
    Implements a switch/case selection in the workflow.

    This node takes a selector input (an integer) and multiple case value inputs.
    It returns the value corresponding to the provided index. If the index is out
    of range, the default value is returned. This allows for selection from multiple
    options based on a computed index.

    NOTE: This version of the node will most likely be deprecated in the future.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "selector": ("INT", {"default": 0, "min": 0}),
                "case_0": ("*", {"lazy": True}),
                "case_1": ("*", {"lazy": True}),
            },
            "optional": {
                "case_2": ("*", {"lazy": True}),
                "case_3": ("*", {"lazy": True}),
                "case_4": ("*", {"lazy": True}),
                "default": ("*", {"lazy": True}),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/Flow Control"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "execute"

    @classmethod
    def VALIDATE_INPUTS(cls, input_types: dict[str, str]) -> bool|str:
        if input_types["selector"] not in ("INT"):
            return "selector must be a INT type"
        return True

    def check_lazy_status(self, condition: int, case_0: Any, case_1: Any,
                          case_2: Any, case_3: Any, case_4: Any, default: Any) -> list[str]:
        needed = []
        if case_0 is None and condition == 0:
            needed.append("case_0")
        if case_1 is None and condition == 1:
            needed.append("case_1")
        if case_2 is None and condition == 2:
            needed.append("case_2")
        if case_3 is None and condition == 3:
            needed.append("case_3")
        if case_4 is None and condition == 4:
            needed.append("case_4")
        if default is None and not 0 <= condition <= 4:
            needed.append("default")
        return needed

    def execute(self, selector: int, case_0: Any, case_1: Any,
                case_2: Any = None, case_3: Any = None,
                case_4: Any = None, default: Any = None) -> tuple[Any]:
        cases = [case_0, case_1, case_2, case_3, case_4]

        if 0 <= selector < len(cases) and cases[selector] is not None:
            return (cases[selector],)

        # If selector is out of range or the selected case is None, return default
        return (default,)


NODE_CLASS_MAPPINGS = {
    "IfElse": IfElse,
    "SwitchCase": SwitchCase,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IfElse": "if/else",
    "SwitchCase": "switch/case",
}
