from inspect import cleandoc

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

class MathFormula(ComfyNodeABC):
    """
    A node that evaluates a mathematical formula provided as a string without using eval.

    This node takes up to 4 numerical inputs (`a`, `b`, `c`, and `d`) and safely evaluates the formula
    with supported operations: +, -, *, /, //, %, **, parentheses, and mathematical functions like abs(),
    floor(), ceil(), and round(). It treats one-letter variables as inputs and multi-letter words as functions.

    Example: If the formula is "a + abs(b * 4 + c)" and inputs are:
        a = 2, b = -3, c = 5,
    The calculation would be:
        result = 2 + abs(-3 * 4 + 5) = 2 + abs(-7) = 2 + 7 = 9
    """
    EXPERIMENTAL = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "formula": (IO.STRING, {"default": "a + b"}),
                "a": (IO.NUMBER, {"default": 0.0, "_dynamic": "letter"}),
            },
        }

    RETURN_TYPES = (IO.FLOAT,)
    CATEGORY = "Basic/maths"
    DESCRIPTION = cleandoc(__doc__ or "")
    FUNCTION = "evaluate"

    OPERATORS = {"**", "//", "/", "*", "-", "+", "%"}
    SUPPORTED_FUNCTIONS = {"abs", "floor", "ceil", "round"}
    VALID_CHARS = set("0123456789.+-*/%(), ")

    def evaluate(self, formula: str, a: float, b: float = 0.0, c: float = 0.0, d: float = 0.0) -> tuple[float]:
        # Tokenize the formula without replacement
        print(f'formula: "{formula}"')
        tokens = self.tokenize_formula(formula)
        print(f'ev tokens: "{tokens}"')

        # Replace variables in the tokenized formula
        replaced_tokens = []
        for token in tokens:
            if token == "a":
                replaced_tokens.append(str(a))
            elif token == "b":
                replaced_tokens.append(str(b))
            elif token == "c":
                replaced_tokens.append(str(c))
            elif token == "d":
                replaced_tokens.append(str(d))
            else:
                replaced_tokens.append(token)

        # Join the replaced tokens back into a formula
        updated_formula = " ".join(replaced_tokens)
        print(f'updated_formula: "{updated_formula}"')

        # Ensure formula is valid
        self.validate_formula(updated_formula)

        # Parse formula into postfix form and evaluate
        postfix = self.infix_to_postfix(replaced_tokens)
        print(f'postfix: "{postfix}"')
        result = self.evaluate_postfix(postfix)
        print(f'result: "{result}"')

        return (result,)

    def validate_formula(self, formula: str):
        """Validates the formula for allowed operators, functions, and characters."""
        import re

        # Validate supported characters
        for char in formula:
            if char not in self.VALID_CHARS and not char.isalpha():
                raise ValueError(f"Invalid character in formula: '{char}'")

        # Validate that all functions are supported
        functions = re.findall(r"[a-zA-Z_]\w*(?=\()", formula)  # Matches functions immediately before "("
        print('formula:')
        print(formula)
        print('functions:')
        print(functions)
        for func in functions:
            if func not in self.SUPPORTED_FUNCTIONS:
                raise ValueError(f"Unsupported function in formula: '{func}'")

    def tokenize_formula(self, formula: str) -> list:
        """
        Tokenizes a formula into numbers, variables, functions, operators, and parentheses.

        Rules:
        - A single-letter token (e.g., 'a') is treated as a variable.
        - A multi-letter token (e.g., 'abs') is treated as a function.
        - Numbers can be integers, floating point, or hexadecimal.
        """
        import re

        # Regex pattern for tokenizing
        pattern = (
            r"(?P<number>-?\d+(\.\d+)?([eE][+-]?\d+)?|-?0x[0-9a-fA-F]+)"  # Matches float, int, hex, scientific notation
            r"|(?P<function>[a-zA-Z]{2,})"                                # Matches multi-letter functions like 'abs'
            r"|(?P<variable>[a-zA-Z])"                                    # Matches single-letter variables (e.g., 'a', 'b')
            r"|(?P<operator>\*\*|//|[+\-*/%()])"                          # Matches operators and parentheses
        )
        # Apply regex to extract matches
        tokens = re.finditer(pattern, formula)

        # Collect and clean the matched tokens
        result = [match.group(0) for match in tokens]
        print(f'Tokens: {result}')  # Debug print
        return result

    def infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens in infix notation to postfix notation (RPN).
        Correctly handles unary negation (e.g., -b) and operator precedence.
        """
        precedence = {"**": 4, "*": 3, "/": 3, "//": 3, "%": 3, "+": 2, "-": 2, "(": 1}
        stack = []  # Operator stack
        postfix = []  # Output list
        previous_token = None  # Tracks the previous token to distinguish unary vs binary operators

        # Track function-to-parenthesis relationships
        function_stack = []  # Stack to track pending functions

        for token in tokens:
            if self.is_number(token):  # Numbers
                postfix.append(float(token))
            elif token in self.SUPPORTED_FUNCTIONS:  # Functions (e.g., abs)
                # Push function onto stack - will be processed when matching parenthesis is found
                function_stack.append(len(stack))  # Record stack depth for this function
                stack.append(token)
            elif token == "(":  # Left parentheses
                stack.append(token)
            elif token == ")":  # Right parentheses
                # Pop operators until left parenthesis
                while stack and stack[-1] != "(":
                    postfix.append(stack.pop())

                if not stack:
                    raise ValueError("Mismatched parentheses in expression.")

                stack.pop()  # Discard the left parenthesis

                # Check if this closing parenthesis matches a function call
                if function_stack and len(stack) == function_stack[-1]:
                    # We've found our function, add it to postfix
                    if stack and stack[-1] in self.SUPPORTED_FUNCTIONS:
                        postfix.append(stack.pop())
                    function_stack.pop()  # Remove the function marker
            elif token in self.OPERATORS:  # Operators (+, -, *, etc.)
                # Check for unary negation
                if token == "-" and (previous_token is None or previous_token in self.OPERATORS or previous_token == "("):
                    # Handle negative numbers directly - place negative value in postfix
                    if tokens.index(token) + 1 < len(tokens) and self.is_number(tokens[tokens.index(token) + 1]):
                        next_token = tokens[tokens.index(token) + 1]
                        # Skip this token and the next number, add negative number to postfix
                        postfix.append(-float(next_token))
                        previous_token = next_token  # Skip to after the number
                        continue
                    else:
                        # Traditional unary minus using 0 - operand
                        postfix.append(0.0)
                        stack.append(token)
                else:
                    # Handle regular operators
                    while stack and stack[-1] not in ["("] and precedence.get(stack[-1], 0) >= precedence[token]:
                        postfix.append(stack.pop())
                    stack.append(token)
            else:
                raise ValueError(f"Unexpected token in infix expression: {token}")

            # Update previous token
            previous_token = token

        # Pop any remaining operators from the stack
        while stack:
            top = stack.pop()
            if top in ["(", ")"]:
                raise ValueError("Mismatched parentheses in expression.")
            postfix.append(top)

        return postfix

    def evaluate_postfix(self, postfix: list) -> float:
        """
        Evaluates a postfix (RPN) expression and returns the result.
        Handles numbers, operators, and functions, including unary negation.
        """
        stack = []

        for token in postfix:
            if isinstance(token, float):  # Numbers
                stack.append(token)
            elif token in self.SUPPORTED_FUNCTIONS:  # Functions (e.g., abs)
                if not stack:
                    raise ValueError(f"Invalid formula: function '{token}' requires an argument but the stack is empty.")
                arg = stack.pop()
                stack.append(self.apply_function(token, arg))
            elif token in self.OPERATORS:  # Operators (+, -, *, /, etc.)
                if len(stack) < 2:
                    raise ValueError(f"Invalid formula: operator '{token}' requires two arguments but the stack has {len(stack)}.")
                b = stack.pop()
                a = stack.pop()
                stack.append(self.apply_operator(a, b, token))
            else:
                raise ValueError(f"Unexpected token in postfix expression: {token}")

        if len(stack) != 1:
            raise ValueError(f"Invalid postfix expression: stack contains excess items: {stack}")
        return stack.pop()

    def apply_operator(self, a: float, b: float, operator: str) -> float:
        """Applies the given operator to two operands."""
        if operator == "+":
            return a + b
        elif operator == "-":
            return a - b
        elif operator == "*":
            return a * b
        elif operator == "/":
            if b == 0:
                raise ZeroDivisionError("Division by zero.")
            return a / b
        elif operator == "//":
            if b == 0:
                raise ZeroDivisionError("Division by zero.")
            return a // b
        elif operator == "%":
            if b == 0:
                raise ZeroDivisionError("Modulo by zero.")
            return a % b
        elif operator == "**":
            return a ** b
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def apply_function(self, func: str, arg: float) -> float:
        """Applies a mathematical function."""
        import math
        if func == "abs":
            return abs(arg)
        elif func == "floor":
            return math.floor(arg)
        elif func == "ceil":
            return math.ceil(arg)
        elif func == "round":
            return round(arg)
        else:
            raise ValueError(f"Unsupported function: {func}")

    def is_number(self, value: str) -> bool:
        """Checks if a token is a valid number."""
        try:
            float.fromhex(value) if value.startswith("0x") else float(value)
            return True
        except ValueError:
            return False

NODE_CLASS_MAPPINGS = {
    "Basic data handling: MathFormula": MathFormula,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Basic data handling: MathFormula": "formula",
}
