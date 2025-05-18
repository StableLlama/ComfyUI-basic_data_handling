from typing import Any
from inspect import cleandoc
from comfy.comfy_types.node_typing import IO, ComfyNodeABC
from comfy_execution.graph import ExecutionBlocker


class IfElse(ComfyNodeABC):
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
                "condition": (IO.BOOLEAN, {}),
                "if_true": (IO.ANY, {"lazy": True}),
                "if_false": (IO.ANY, {"lazy": True}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/flow control"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "execute"

    def check_lazy_status(self, condition: bool, if_true: Any, if_false: Any) -> list[str]:
        needed = []
        if if_true is None and condition is True:
            needed.append("if_true")
        if if_false is None and condition is False:
            needed.append("if_false")
        return needed

    def execute(self, condition: bool, if_true: Any, if_false: Any) -> tuple[Any]:
        return (if_true if condition else if_false,)


class IfElifElse(ComfyNodeABC):
    """
    Implements a conditional branch (if/elif/else) in the workflow.

    This node takes a condition input and two value inputs. If the condition
    evaluates to True, the first value is returned; otherwise, the elif (else if)
    is evaluated and returned when true. This continues for all additional elifs.
    When none is true, the value of the else is returned.
    This allows conditional data flow in ComfyUI workflows.
    """
    EXPERIMENTAL = True
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "if": (IO.BOOLEAN, {"forceInput": True}),
                "then": (IO.ANY, {"lazy": True}),
            },
            "optional": {
                "elif_0": (IO.BOOLEAN, {"forceInput": True, "lazy": True, "_dynamic": "number", "_dynamicGroup": 0}),
                "then_0": (IO.ANY, {"lazy": True, "_dynamic": "number", "_dynamicGroup": 0}),
                "else": (IO.ANY, {"lazy": True}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/flow control"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "execute"

    def check_lazy_status(self, **kwargs) -> list[str]:
        needed = []

        # Check if condition
        if kwargs.get("if", False) and kwargs.get("then") is None:
            needed.append("then")
            return needed  # If main condition is true, we only need "then"

        # Check each elif condition
        elif_index = 0
        while True:
            elif_key = f"elif_{elif_index}"
            then_key = f"then_{elif_index}"

            if elif_key not in kwargs:
                break

            # If this elif condition is true and its value is None, add it to needed
            if kwargs.get(elif_key, False) and kwargs.get(then_key) is None:
                needed.append(then_key)
                return needed  # If any elif is true, we need only its then value

            elif_index += 1

        # If no conditions were true, check if we need the else
        if "else" in kwargs and kwargs["else"] is None:
            needed.append("else")

        return needed

    def execute(self, **kwargs) -> tuple[Any]:
        # Check if the main condition is true
        if kwargs.get("if", False):
            return (kwargs.get("then"),)

        # Check each elif condition
        elif_index = 0
        while True:
            elif_key = f"elif_{elif_index}"
            then_key = f"then_{elif_index}"

            if elif_key not in kwargs:
                break

            if kwargs.get(elif_key, False):
                return (kwargs.get(then_key),)

            elif_index += 1

        # If no conditions were true, return the else value
        return (kwargs.get("else"),)


class SwitchCase(ComfyNodeABC):
    """
    Implements a switch/case selection in the workflow.

    This node takes a selector input (an integer) and multiple case value inputs.
    It returns the value corresponding to the provided index. If the index is out
    of range, the default value is returned. This allows for selection from multiple
    options based on a computed index.

    NOTE: This version of the node will most likely be deprecated in the future.
    """
    EXPERIMENTAL = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "selector": (IO.INT, {"default": 0, "min": 0}),
                "case_0": (IO.ANY, {"lazy": True, "_dynamic": "number"}),
            },
            "optional": {
                "default": (IO.ANY, {"lazy": True}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("result",)
    CATEGORY = "Basic/flow control"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "execute"

    def check_lazy_status(self, selector: int, **kwargs) -> list[str]:
        needed = []

        # Check for needed case inputs based on selector
        case_count = 0
        for key, value in kwargs.items():
            if key.startswith("case_"):
                try:
                    case_index = int(key.split("_")[1])
                    case_count = max(case_count, case_index + 1)
                    if value is None and selector == case_index:
                        needed.append(key)
                except ValueError:
                    pass  # Not a numeric case key

        # Check if default is needed when selector is out of range
        if "default" in kwargs and kwargs["default"] is None and not 0 <= selector < case_count:
            needed.append("default")

        return needed

    def execute(self, selector: int, **kwargs) -> tuple[Any]:
        # Build cases array from all case_X inputs
        cases = []
        for i in range(len(kwargs)):
            case_key = f"case_{i}"
            if case_key in kwargs:
                cases.append(kwargs[case_key])
            else:
                break

        # Return the selected case if valid
        if 0 <= selector < len(cases) and cases[selector] is not None:
            return (cases[selector],)

        # If selector is out of range or the selected case is None, return default
        return (kwargs.get("default"),)


class FlowSelect(ComfyNodeABC):
    """
    Select the direction of the flow.

    This node takes a value and directs it to either the "true" or "false" output.

    Note: for dynamic switching in a Data Flow you might want to use
    "filter select" instead.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (IO.ANY, {}),
                "select": (IO.BOOLEAN, {}),
            }
        }

    RETURN_TYPES = (IO.ANY, IO.ANY)
    RETURN_NAMES = ("true", "false")
    CATEGORY = "Basic/flow control"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "select"

    def select(self, value, select = True) -> tuple[Any, Any]:
        if select:
            return value, ExecutionBlocker(None)
        else:
            return ExecutionBlocker(None), value


class ExecutionOrder(ComfyNodeABC):
    """
    Force execution order in the workflow.

    This node is lightweight and does not affect the workflow. It is used to force
    the execution order of nodes in the workflow. You only need to chain this node
    with the other execution order nodes in the desired order and add any
    output of the nodes you want to force execution order on.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "E/O": ("E/O", {}),
                "any node output": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = ("E/O",)
    CATEGORY = "Basic/flow control"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "execute"

    def execute(self, **kwargs) -> tuple[Any]:
        return (None,)


NODE_CLASS_MAPPINGS = {
    "Basic data handling: IfElse": IfElse,
    "Basic data handling: IfElifElse": IfElifElse,
    "Basic data handling: SwitchCase": SwitchCase,
    "Basic data handling: FlowSelect": FlowSelect,
    "Basic data handling: ExecutionOrder": ExecutionOrder,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: IfElse": "if/else",
    "Basic data handling: IfElifElse": "if/elif/.../else",
    "Basic data handling: SwitchCase": "switch/case",
    "Basic data handling: FlowSelect": "flow select",
    "Basic data handling: ExecutionOrder": "force execution order",
}
