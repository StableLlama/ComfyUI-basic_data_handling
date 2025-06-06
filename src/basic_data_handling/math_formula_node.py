import re
import math
from inspect import cleandoc

try:
    from comfy.comfy_types.node_typing import IO, ComfyNodeABC
except ImportError:
    # Mock classes for standalone testing
    class IO:
        BOOLEAN = "BOOLEAN"
        INT = "INT"
        FLOAT = "FLOAT"
        STRING = "STRING"
        NUMBER = "FLOAT,INT"
        ANY = "*"
    ComfyNodeABC = object

from ._dynamic_input import ContainsDynamicDict

class MathFormula(ComfyNodeABC):
    """
    A node that evaluates a mathematical formula provided as a string without using eval.

    This node takes an arbitrary number of numerical inputs (single letters like `a`, `b`, `c`, etc.) and safely
    evaluates the formula with supported operations: +, -, *, /, //, %, **, parentheses, and mathematical
    functions. It treats one-letter variables as inputs and multi-letter words as functions.

    The identifiers `e` and `pi` are special. When used as a function call (`e()`, `pi()`), they return their
    respective mathematical constants. When used as a variable (`e`), they are treated like any other
    variable and expect a corresponding input.

    Supported functions:
    - Basic: abs, floor, ceil, round, min(a,b), max(a,b)
    - Trigonometric: sin, cos, tan, asin, acos, atan, atan2(y,x), degrees, radians
    - Hyperbolic: sinh, cosh, tanh, asinh, acosh, atanh
    - Exponential & Logarithmic: exp, log, log10, log2, sqrt, pow(base,exp)
    - Constants (must be called with empty parentheses): pi(), e()
    """
    EXPERIMENTAL = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": ContainsDynamicDict({
                "formula": (IO.STRING, {"default": "a + b"}),
                "a": (IO.NUMBER, {"default": 1.0, "_dynamic": "letter"}),
                "b": (IO.NUMBER, {"default": 2.0, "_dynamic": "letter"}),
            }),
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "math"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "evaluate"

    FUNC_ARITIES = {
        "pi": 0, "e": 0, "abs": 1, "floor": 1, "ceil": 1, "round": 1, "sin": 1, "cos": 1,
        "tan": 1, "asin": 1, "acos": 1, "atan": 1, "degrees": 1, "radians": 1, "sinh": 1,
        "cosh": 1, "tanh": 1, "asinh": 1, "acosh": 1, "atanh": 1, "exp": 1, "log": 1,
        "log10": 1, "log2": 1, "sqrt": 1, "pow": 2, "atan2": 2, "min": 2, "max": 2,
    }
    SUPPORTED_FUNCTIONS = set(FUNC_ARITIES.keys())

    OPERATOR_PROPS = {
        "+": (2, "LEFT", 2), "-": (2, "LEFT", 2), "*": (3, "LEFT", 2), "/": (3, "LEFT", 2),
        "//": (3, "LEFT", 2), "%": (3, "LEFT", 2), "**": (4, "RIGHT", 2),
        "_NEG": (5, "RIGHT", 1),
    }
    OPERATORS = set(OPERATOR_PROPS.keys())

    TOKEN_REGEX = re.compile(
        r"([a-zA-Z_][a-zA-Z0-9_]*)"
        r"|(\d+(?:\.\d*)?|\.\d+)"
        r"|(\*\*|//|[+\-*/%(),])"
    )

    def evaluate(self, formula: str, **kwargs) -> tuple[float]:
        tokens = self.tokenize_formula(formula)
        postfix_tokens = self.infix_to_postfix(tokens)
        result = self.evaluate_postfix(postfix_tokens, kwargs)
        return (result,)

    def tokenize_formula(self, formula: str) -> list[str]:
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.,+-*/%() \t\n\r"
        for char in formula:
            if char not in allowed_chars:
                raise ValueError(f"Invalid character in formula: '{char}'")
        return [token for group in self.TOKEN_REGEX.findall(formula) for token in group if token]

    def infix_to_postfix(self, tokens: list[str]) -> list:
        output_queue = []
        op_stack = []
        prev_token = None
        binary_operators = {op for op, props in self.OPERATOR_PROPS.items() if props[2] == 2}

        for i, token in enumerate(tokens):
            if self.is_number(token):
                output_queue.append(float(token))
            elif token.isalnum() and not token.isdigit():
                is_function_call = (i + 1 < len(tokens) and tokens[i+1] == '(')

                if is_function_call:
                    if token not in self.SUPPORTED_FUNCTIONS:
                        raise ValueError(f"Unknown function: '{token}'")
                    op_stack.append(token) # Push function name as string
                else: # It's a variable
                    if len(token) == 1 and token.isalpha():
                        output_queue.append(('VAR', token)) # Push variable as a tagged tuple
                    else:
                        if token in self.SUPPORTED_FUNCTIONS:
                            raise ValueError(f"Function '{token}' must be called with parentheses, e.g., {token}()")
                        else:
                            raise ValueError(f"Unknown identifier: '{token}'. Only single-letter variables are allowed.")

            elif token == "(":
                op_stack.append(token)
            elif token == ",":
                while op_stack and op_stack[-1] != "(":
                    output_queue.append(op_stack.pop())
                if not op_stack or op_stack[-1] != "(":
                    raise ValueError("Misplaced comma or mismatched parentheses.")
            elif token == ")":
                while op_stack and op_stack[-1] != "(":
                    output_queue.append(op_stack.pop())
                if not op_stack:
                    raise ValueError("Mismatched parentheses.")
                op_stack.pop()
                if op_stack and op_stack[-1] in self.SUPPORTED_FUNCTIONS:
                    output_queue.append(op_stack.pop())
            elif token in self.OPERATORS:
                is_unary = token == '-' and (prev_token is None or prev_token in binary_operators or prev_token in ['(', ','])
                op_to_push = "_NEG" if is_unary else token

                props = self.OPERATOR_PROPS[op_to_push]
                prec, assoc = props[0], props[1]

                while (op_stack and op_stack[-1] != '(' and op_stack[-1] in self.OPERATORS and
                       (self.OPERATOR_PROPS.get(op_stack[-1], (0,))[0] > prec or
                        (self.OPERATOR_PROPS.get(op_stack[-1], (0,))[0] == prec and assoc == "LEFT"))):
                    output_queue.append(op_stack.pop())
                op_stack.append(op_to_push)
            else:
                raise ValueError(f"Unknown identifier or invalid expression: '{token}'")
            prev_token = token

        while op_stack:
            op = op_stack.pop()
            if op == "(":
                raise ValueError("Mismatched parentheses.")
            output_queue.append(op)

        return output_queue

    def evaluate_postfix(self, postfix: list, variables: dict) -> float:
        stack = []
        for token in postfix:
            if isinstance(token, float):
                stack.append(token)
            elif isinstance(token, tuple) and token[0] == 'VAR':
                var_name = token[1]
                if var_name not in variables:
                    raise ValueError(f"Variable '{var_name}' was not provided.")
                stack.append(float(variables[var_name]))
            elif token in self.OPERATORS:
                arity = self.OPERATOR_PROPS[token][2]
                if len(stack) < arity:
                    raise ValueError(f"Operator '{token}' needs {arity} operand(s).")

                operands = [stack.pop() for _ in range(arity)]
                operands.reverse()

                if arity == 1:
                    stack.append(-operands[0])
                else:
                    stack.append(self.apply_operator(operands[0], operands[1], token))
            elif token in self.SUPPORTED_FUNCTIONS:
                arity = self.FUNC_ARITIES[token]
                if len(stack) < arity:
                    raise ValueError(f"Function '{token}' needs {arity} argument(s).")

                args = [stack.pop() for _ in range(arity)]
                args.reverse()
                stack.append(self.apply_function(token, args))
            else:
                raise ValueError(f"Internal error: Unknown token in postfix queue: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression. The formula may be incomplete or have extra values.")
        return stack[0]

    def apply_operator(self, a: float, b: float, operator: str) -> float:
        if operator == "+": return a + b
        if operator == "-": return a - b
        if operator == "*": return a * b
        if operator == "**": return a ** b
        if b == 0 and operator in ['/', '//', '%']:
            raise ZeroDivisionError(f"Division by zero in operator '{operator}'.")
        if operator == "/": return a / b
        if operator == "//": return a // b
        if operator == "%": return a % b
        raise ValueError(f"Unsupported operator: {operator}")

    def apply_function(self, func: str, args: list) -> float:
        if func == "pi": return math.pi
        if func == "e": return math.e
        if len(args) == 1:
            arg = args[0]
            if func == "abs": return abs(arg)
            if func == "floor": return math.floor(arg)
            if func == "ceil": return math.ceil(arg)
            if func == "round": return round(arg)
            if func == "sin": return math.sin(arg)
            if func == "cos": return math.cos(arg)
            if func == "tan": return math.tan(arg)
            if func == "asin": return math.asin(arg)
            if func == "acos": return math.acos(arg)
            if func == "atan": return math.atan(arg)
            if func == "degrees": return math.degrees(arg)
            if func == "radians": return math.radians(arg)
            if func == "sinh": return math.sinh(arg)
            if func == "cosh": return math.cosh(arg)
            if func == "tanh": return math.tanh(arg)
            if func == "asinh": return math.asinh(arg)
            if func == "acosh": return math.acosh(arg)
            if func == "atanh": return math.atanh(arg)
            if func == "exp": return math.exp(arg)
            if func == "log": return math.log(arg)
            if func == "log10": return math.log10(arg)
            if func == "log2": return math.log2(arg)
            if func == "sqrt": return math.sqrt(arg)
        if len(args) == 2:
            a, b = args[0], args[1]
            if func == "pow": return math.pow(a, b)
            if func == "atan2": return math.atan2(a, b)
            if func == "min": return min(a, b)
            if func == "max": return max(a, b)
        raise ValueError(f"Internal error: apply_function called with wrong number of args for '{func}'")

    def is_number(self, value: str) -> bool:
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

NODE_CLASS_MAPPINGS = {
    "Basic data handling: MathFormula": MathFormula,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: MathFormula": "formula",
}
