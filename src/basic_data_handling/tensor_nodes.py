try:
    import torch
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "basic_data_handling: Missing dependency 'torch'. It seems your ComfyUI installation is faulty."
        "Only for development purposes: Install it with `pip install .[dev] numpy torch pillow` or `pip install torch`."
    ) from e

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

class TensorCreate(ComfyNodeABC):
    """
    Creates a PyTorch tensor from various input types.
    Can accept numbers, lists, or existing tensors.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    CATEGORY = "Basic/tensor"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "create"

    def create(self, input: Any) -> tuple[torch.Tensor]:
        if isinstance(input, torch.Tensor):
            return (input,)
        try:
            return (torch.tensor(input),)
        except Exception as e:
            raise ValueError(f"Failed to create tensor from {type(input)}: {str(e)}")

class TensorBinaryOp(ComfyNodeABC):
    """
    Performs binary operations between two tensors or a tensor and a scalar.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": (IO.ANY, {}),
                "b": (IO.ANY, {}),
                "operation": (["add", "subtract", "multiply", "divide", "power", "remainder", "floor_divide"], {"default": "add"}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    CATEGORY = "Basic/tensor"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "operate"

    def operate(self, a: Any, b: Any, operation: str) -> tuple[torch.Tensor]:
        a_tensor = a if isinstance(a, torch.Tensor) else torch.tensor(a)
        b_tensor = b if isinstance(b, torch.Tensor) else torch.tensor(b)

        if operation == "add":
            return (a_tensor + b_tensor,)
        elif operation == "subtract":
            return (a_tensor - b_tensor,)
        elif operation == "multiply":
            return (a_tensor * b_tensor,)
        elif operation == "divide":
            return (a_tensor / b_tensor,)
        elif operation == "power":
            return (torch.pow(a_tensor, b_tensor),)
        elif operation == "remainder":
            return (a_tensor % b_tensor,)
        elif operation == "floor_divide":
            return (a_tensor // b_tensor,)
        else:
            raise ValueError(f"Unknown operation: {operation}")

class TensorUnaryOp(ComfyNodeABC):
    """
    Performs unary operations on a tensor.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (IO.ANY, {}),
                "operation": (["abs", "neg", "exp", "log", "sin", "cos", "sqrt", "sigmoid", "relu"], {"default": "abs"}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    CATEGORY = "Basic/tensor"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "operate"

    def operate(self, input: Any, operation: str) -> tuple[torch.Tensor]:
        t = input if isinstance(input, torch.Tensor) else torch.tensor(input)

        if operation == "abs":
            return (torch.abs(t),)
        elif operation == "neg":
            return (torch.neg(t),)
        elif operation == "exp":
            return (torch.exp(t),)
        elif operation == "log":
            return (torch.log(t),)
        elif operation == "sin":
            return (torch.sin(t),)
        elif operation == "cos":
            return (torch.cos(t),)
        elif operation == "sqrt":
            return (torch.sqrt(t),)
        elif operation == "sigmoid":
            return (torch.sigmoid(t),)
        elif operation == "relu":
            return (torch.relu(t),)
        else:
            raise ValueError(f"Unknown operation: {operation}")

class TensorSlice(ComfyNodeABC):
    """
    Slices a tensor using a slice string (e.g., ':, 0:10, 5').
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "tensor": (IO.ANY, {}),
                "slice_str": (IO.STRING, {"default": ":"}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    CATEGORY = "Basic/tensor"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "slice_tensor"

    def slice_tensor(self, tensor: Any, slice_str: str) -> tuple[torch.Tensor]:
        if not isinstance(tensor, torch.Tensor):
            tensor = torch.tensor(tensor)

        # Basic parsing of slice string
        # This is a bit advanced for a simple node, but very useful.
        # We'll use eval in a restricted way or manual parsing.
        # Manual parsing is safer.
        def parse_slice(s):
            parts = s.split(':')
            if len(parts) == 1:
                return int(parts[0])
            return slice(*(int(p) if p.strip() else None for p in parts))

        try:
            dims = [d.strip() for d in slice_str.split(',')]
            indices = tuple(parse_slice(d) if ':' in d or d.isdigit() or (d.startswith('-') and d[1:].isdigit()) else d for d in dims)
            # Re-index with parsed slices
            # Note: this is a simplification. torch supports more complex indexing.
            # But for basic usage, this covers most cases.
            return (tensor[indices],)
        except Exception as e:
            raise ValueError(f"Failed to slice tensor with '{slice_str}': {str(e)}")

class TensorReshape(ComfyNodeABC):
    """
    Reshapes a tensor.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "tensor": (IO.ANY, {}),
                "shape": (IO.STRING, {"default": "-1"}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    CATEGORY = "Basic/tensor"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "reshape"

    def reshape(self, tensor: Any, shape: str) -> tuple[torch.Tensor]:
        if not isinstance(tensor, torch.Tensor):
            tensor = torch.tensor(tensor)

        try:
            shape_tuple = tuple(int(s.strip()) for s in shape.split(','))
            return (tensor.reshape(shape_tuple),)
        except Exception as e:
            raise ValueError(f"Failed to reshape tensor to {shape}: {str(e)}")

class TensorPermute(ComfyNodeABC):
    """
    Permutes tensor dimensions.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "tensor": (IO.ANY, {}),
                "dims": (IO.STRING, {"default": "0, 1"}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    CATEGORY = "Basic/tensor"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "permute"

    def permute(self, tensor: Any, dims: str) -> tuple[torch.Tensor]:
        if not isinstance(tensor, torch.Tensor):
            tensor = torch.tensor(tensor)

        try:
            dims_tuple = tuple(int(d.strip()) for d in dims.split(','))
            return (tensor.permute(dims_tuple),)
        except Exception as e:
            raise ValueError(f"Failed to permute tensor with dims {dims}: {str(e)}")

class TensorJoin(ComfyNodeABC):
    """
    Joins multiple tensors (concatenate or stack).
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "tensor1": (IO.ANY, {}),
                "tensor2": (IO.ANY, {}),
                "dim": (IO.INT, {"default": 0}),
                "mode": (["concatenate", "stack"], {"default": "concatenate"}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    CATEGORY = "Basic/tensor"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "join"

    def join(self, tensor1: Any, tensor2: Any, dim: int, mode: str) -> tuple[torch.Tensor]:
        t1 = tensor1 if isinstance(tensor1, torch.Tensor) else torch.tensor(tensor1)
        t2 = tensor2 if isinstance(tensor2, torch.Tensor) else torch.tensor(tensor2)

        if mode == "concatenate":
            return (torch.cat([t1, t2], dim=dim),)
        else:
            return (torch.stack([t1, t2], dim=dim),)

class TensorInfo(ComfyNodeABC):
    """
    Returns information about a tensor.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "tensor": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = (IO.ANY, IO.STRING, IO.STRING)
    RETURN_NAMES = ("shape", "dtype", "device")
    CATEGORY = "Basic/tensor"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "get_info"

    def get_info(self, tensor: Any) -> tuple[list[int], str, str]:
        if not isinstance(tensor, torch.Tensor):
            tensor = torch.tensor(tensor)

        return (list(tensor.shape), str(tensor.dtype), str(tensor.device))

NODE_CLASS_MAPPINGS = {
    "TensorCreate": TensorCreate,
    "TensorBinaryOp": TensorBinaryOp,
    "TensorUnaryOp": TensorUnaryOp,
    "TensorSlice": TensorSlice,
    "TensorReshape": TensorReshape,
    "TensorPermute": TensorPermute,
    "TensorJoin": TensorJoin,
    "TensorInfo": TensorInfo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TensorCreate": "Tensor Create",
    "TensorBinaryOp": "Tensor Binary Op",
    "TensorUnaryOp": "Tensor Unary Op",
    "TensorSlice": "Tensor Slice",
    "TensorReshape": "Tensor Reshape",
    "TensorPermute": "Tensor Permute",
    "TensorJoin": "Tensor Join",
    "TensorInfo": "Tensor Info",
}
