import pytest
import math
from math import sin, cos
from src.basic_data_handling.math_formula_node import MathFormula

def test_basic_formula_evaluation():
    """Test basic formula evaluation with simple operations."""
    node = MathFormula()

    # Simple arithmetic
    assert node.evaluate("a + b", a=3, b=4)[0] == pytest.approx(7.0)
    assert node.evaluate("a - b", a=10, b=6)[0] == pytest.approx(4.0)
    assert node.evaluate("a * b", a=5, b=3)[0] == pytest.approx(15.0)
    assert node.evaluate("a / b", a=10, b=2)[0] == pytest.approx(5.0)

    # Combined operations
    assert node.evaluate("a + b * c", a=2, b=3, c=4)[0] == pytest.approx(14.0)
    assert node.evaluate("(a + b) * c", a=2, b=3, c=4)[0] == pytest.approx(20.0)
    assert node.evaluate("a ** b", a=2, b=3)[0] == pytest.approx(8.0)
    assert node.evaluate("a // b", a=7, b=2)[0] == pytest.approx(3.0)
    assert node.evaluate("a % b", a=7, b=4)[0] == pytest.approx(3.0)

    # Unary minus
    assert node.evaluate("-a", a=5)[0] == pytest.approx(-5.0)
    assert node.evaluate("a * -b", a=3, b=4)[0] == pytest.approx(-12.0)

def test_function_calls():
    """Test formula evaluation with math functions."""
    node = MathFormula()

    # Single-argument functions
    assert node.evaluate("sin(a)", a=math.pi/6)[0] == pytest.approx(0.5)
    assert node.evaluate("cos(a)", a=0)[0] == pytest.approx(1.0)

    # Unary minus with function calls
    assert node.evaluate("sin(-a)", a=math.pi/6)[0] == pytest.approx(-0.5)
    assert node.evaluate("-sin(a)", a=math.pi/6)[0] == pytest.approx(-0.5)
    assert node.evaluate("-sin(-a)", a=math.pi/6)[0] == pytest.approx(0.5)

    # Unary minus with nested function calls
    assert node.evaluate("sin(cos(-a))", a=math.pi)[0] == pytest.approx(sin(cos(-math.pi)))
    assert node.evaluate("-sin(cos(-a))", a=math.pi)[0] == pytest.approx(-sin(cos(-math.pi)))
    assert node.evaluate("tan(a)", a=math.pi/4)[0] == pytest.approx(1.0)
    assert node.evaluate("sqrt(a)", a=16)[0] == pytest.approx(4.0)
    assert node.evaluate("log(a)", a=math.e)[0] == pytest.approx(1.0)
    assert node.evaluate("exp(a)", a=2)[0] == pytest.approx(math.exp(2))

    # Two-argument functions
    assert node.evaluate("min(a, b)", a=5, b=10)[0] == pytest.approx(5.0)
    assert node.evaluate("max(a, b)", a=5, b=10)[0] == pytest.approx(10.0)
    assert node.evaluate("pow(a, b)", a=2, b=3)[0] == pytest.approx(8.0)

def test_constants():
    """Test formula evaluation with constants."""
    node = MathFormula()

    # Constants called with empty parentheses
    assert node.evaluate("pi()")[0] == pytest.approx(math.pi)
    assert node.evaluate("e()")[0] == pytest.approx(math.e)

    # Using constants in expressions
    assert node.evaluate("2 * pi()")[0] == pytest.approx(2 * math.pi)
    assert node.evaluate("e() ** 2")[0] == pytest.approx(math.e ** 2)
    assert node.evaluate("sin(pi() / 2)")[0] == pytest.approx(1.0)
    assert node.evaluate("log(e())")[0] == pytest.approx(1.0)

    # More complex expressions with constants
    assert node.evaluate("a * pi() + b", a=2, b=1)[0] == pytest.approx(2 * math.pi + 1)
    assert node.evaluate("e() ** a", a=3)[0] == pytest.approx(math.e ** 3)
    assert node.evaluate("sin(a * pi())", a=0.5)[0] == pytest.approx(1.0, abs=1e-10)

def test_variable_constant_distinction():
    """Test that variables and constants can coexist without conflict."""
    node = MathFormula()

    # Using 'e' as a variable while also using 'e()' as a constant
    assert node.evaluate("e + e()", e=5)[0] == pytest.approx(5 + math.e)

    # Using 'pi' as a variable while also using 'pi()' as a constant
    with pytest.raises(ValueError, match=r"Function 'pi' must be called with parentheses, e.g., pi()"):
        node.evaluate("pi * pi()", pi=3)

    # More complex expressions
    assert node.evaluate("e * log(e())", e=2)[0] == pytest.approx(2.0)
    assert node.evaluate("a * e() + b * e", a=2, b=3, e=4)[0] == pytest.approx(2 * math.e + 3 * 4)

def test_unary_minus():
    """Test that unary minus (negation) is handled correctly in all contexts."""
    node = MathFormula()

    # Simple variable negation
    assert node.evaluate("-a", a=5)[0] == pytest.approx(-5.0)
    assert node.evaluate("-a", a=-3)[0] == pytest.approx(3.0)

    # Constant negation
    assert node.evaluate("-pi()")[0] == pytest.approx(-math.pi)
    assert node.evaluate("-e()")[0] == pytest.approx(-math.e)

    # Function result negation
    assert node.evaluate("-sin(a)", a=math.pi/2)[0] == pytest.approx(-1.0)
    assert node.evaluate("-sqrt(a)", a=4)[0] == pytest.approx(-2.0)

    # Nested unary minus
    assert node.evaluate("--a", a=5)[0] == pytest.approx(5.0)
    assert node.evaluate("---a", a=5)[0] == pytest.approx(-5.0)

    # Unary minus with binary operators
    assert node.evaluate("a + -b", a=5, b=3)[0] == pytest.approx(2.0)
    assert node.evaluate("a * -b", a=4, b=3)[0] == pytest.approx(-12.0)
    assert node.evaluate("a / -b", a=6, b=2)[0] == pytest.approx(-3.0)
    assert node.evaluate("a - -b", a=5, b=3)[0] == pytest.approx(8.0)

    # Unary minus with higher precedence operators
    assert node.evaluate("-a * b", a=2, b=3)[0] == pytest.approx(-6.0)
    assert node.evaluate("-(a * b)", a=2, b=3)[0] == pytest.approx(-6.0)
    assert node.evaluate("-a ** 2", a=3)[0] == pytest.approx(9.0)  # see documentation about this special case
    assert node.evaluate("(-a) ** 2", a=3)[0] == pytest.approx(9.0)  # (-a)^2

    # Unary minus with parentheses
    assert node.evaluate("-(a + b)", a=2, b=3)[0] == pytest.approx(-5.0)
    assert node.evaluate("-(a + b) * c", a=2, b=3, c=4)[0] == pytest.approx(-20.0)
    assert node.evaluate("a * -(b + c)", a=2, b=3, c=4)[0] == pytest.approx(-14.0)

    # Unary minus at start of parenthesized expressions
    assert node.evaluate("(-a + b)", a=5, b=3)[0] == pytest.approx(-2.0)
    assert node.evaluate("(-a - b)", a=5, b=3)[0] == pytest.approx(-8.0)

    # Unary minus with constants and functions in complex expressions
    assert node.evaluate("-pi() * sin(-a)", a=math.pi/2)[0] == pytest.approx(math.pi)
    assert node.evaluate("-e() ** -2")[0] == pytest.approx(1/(math.e**2)) # see documentation about this special case

def test_error_conditions():
    """Test error conditions in formula evaluation."""
    node = MathFormula()

    # Constants without parentheses should raise ValueError
    with pytest.raises(ValueError, match=r"Function 'pi' must be called with parentheses, e.g., pi()"):
        node.evaluate("pi")

    with pytest.raises(ValueError, match=r"Variable 'e' was not provided."):
        node.evaluate("2 * e")

    # Test unary minus with errors
    with pytest.raises(ValueError):
        node.evaluate("-unknown_var")

    with pytest.raises(ValueError):
        node.evaluate("-unknown_func(x)", x=5)

    # Unary minus with domain errors
    with pytest.raises(ValueError):
        node.evaluate("sqrt(-a)", a=4)  # Negative under square root

    with pytest.raises(ValueError):
        node.evaluate("log(-a)", a=2)  # Negative in logarithm

    # Missing variables
    with pytest.raises(ValueError, match=r"Variable 'x' was not provided"):
        node.evaluate("x + y", y=5)

    # Invalid function calls
    with pytest.raises(ValueError):
        node.evaluate("unknown_func(x)", x=5)

    # Division by zero
    with pytest.raises(ZeroDivisionError):
        node.evaluate("a / b", a=5, b=0)

    # Function domain errors
    with pytest.raises(ValueError):
        node.evaluate("sqrt(x)", x=-1)  # Negative square root

    with pytest.raises(ValueError):
        node.evaluate("log(x)", x=0)  # Log of zero

    with pytest.raises(ValueError):
        node.evaluate("asin(x)", x=2)  # Out of domain [-1, 1]

def test_complex_expressions():
    """Test evaluation of complex mathematical expressions."""
    node = MathFormula()

    # Complex expression with variables, functions, and constants
    formula = "a * sin(b * pi()) + c * sqrt(d) + e() ** 2"
    result = node.evaluate(formula, a=2, b=0.5, c=3, d=9)[0]
    expected = 2 * math.sin(0.5 * math.pi) + 3 * math.sqrt(9) + math.e ** 2
    assert result == pytest.approx(expected)

    # Expression with nested functions
    formula = "sqrt(pow(a, 2) + pow(b, 2))"
    assert node.evaluate(formula, a=3, b=4)[0] == pytest.approx(5.0)

    # Expression with multiple operations and precedence
    formula = "a + b * c - d / e + f ** g"
    result = node.evaluate(formula, a=1, b=2, c=3, d=8, e=4, f=2, g=3)[0]
    expected = 1 + 2 * 3 - 8 / 4 + 2 ** 3
    assert result == pytest.approx(expected)

    # Complex expressions with unary minus
    formula = "a + -b * c - -(d / e) + -f ** g"
    result = node.evaluate(formula, a=1, b=2, c=3, d=8, e=4, f=2, g=3)[0]
    expected = 1 + (-2) * 3 - (-(8 / 4)) + (-(2 ** 3))
    assert result == pytest.approx(expected)

    # Expression with multiple unary minuses and parentheses
    formula = "-a * (b + -c) / (-d)"
    result = node.evaluate(formula, a=2, b=5, c=3, d=4)[0]
    expected = -2 * (5 + (-3)) / (-4)
    assert result == pytest.approx(expected)

def test_formula_with_e_variable():
    """Test formulas with 'e' as a variable to ensure it doesn't clash with the constant."""
    node = MathFormula()

    # Using 'e' as a variable
    assert node.evaluate("e * 2", e=5)[0] == pytest.approx(10.0)

    # Using both 'e' as a variable and 'e()' as a constant in the same expression
    assert node.evaluate("e + e()", e=3)[0] == pytest.approx(3 + math.e)

    # More complex formula with both uses
    formula = "a * e + b * e()"
    result = node.evaluate(formula, a=2, e=3, b=4)[0]
    expected = 2 * 3 + 4 * math.e
    assert result == pytest.approx(expected)

    # Formula using 'e' in different contexts
    formula = "e * sin(e() * pi())"
    result = node.evaluate(formula, e=2)[0]
    expected = 2 * math.sin(math.e * math.pi)
    assert result == pytest.approx(expected)

def test_whitespace_handling():
    """Test that the parser correctly handles different whitespace patterns."""
    node = MathFormula()

    # No spaces
    assert node.evaluate("a+b*c", a=1, b=2, c=3)[0] == pytest.approx(7.0)

    # Lots of spaces
    assert node.evaluate("a  +  b  *  c", a=1, b=2, c=3)[0] == pytest.approx(7.0)

    # Whitespace around unary minus
    assert node.evaluate("- a", a=5)[0] == pytest.approx(-5.0)
    assert node.evaluate("-    a", a=5)[0] == pytest.approx(-5.0)
    assert node.evaluate("a * - b", a=3, b=4)[0] == pytest.approx(-12.0)
    assert node.evaluate("a * -    b", a=3, b=4)[0] == pytest.approx(-12.0)
    assert node.evaluate("- (a + b)", a=2, b=3)[0] == pytest.approx(-5.0)
    assert node.evaluate("-    (a + b)", a=2, b=3)[0] == pytest.approx(-5.0)

    # Mixed spacing around functions
    assert node.evaluate("sin( a )+cos(b)", a=math.pi/2, b=0)[0] == pytest.approx(2.0)

    # Spacing around constants
    assert node.evaluate("2*pi( )", a=1)[0] == pytest.approx(2 * math.pi)
    assert node.evaluate("e( )**2")[0] == pytest.approx(math.e ** 2)

def test_tokenizing():
    """Test the tokenization functionality."""
    node = MathFormula()

    # Test basic tokenizing
    tokens = node.tokenize_formula("a + b * c")
    assert "a" in tokens
    assert "+" in tokens
    assert "b" in tokens
    assert "*" in tokens
    assert "c" in tokens

    # Test tokenizing functions
    tokens = node.tokenize_formula("sin(a) + cos(b)")
    assert "sin" in tokens
    assert "(" in tokens
    assert "a" in tokens
    assert ")" in tokens
    assert "+" in tokens
    assert "cos" in tokens
    assert "b" in tokens

    # Test tokenizing constants with parentheses
    tokens = node.tokenize_formula("pi() + e()")
    assert "pi" in tokens
    assert "(" in tokens
    assert ")" in tokens
    assert "+" in tokens
    assert "e" in tokens

    # Test complex expression
    tokens = node.tokenize_formula("a + b * (c - d) / e() ** 2")
    assert all(token in tokens for token in ["a", "+", "b", "*", "(", "c", "-", "d", ")", "/", "e", "(", ")", "**", "2"])

def test_infix_to_postfix():
    """Test the infix to postfix conversion."""
    node = MathFormula()

    # Basic conversion
    formula = "a + b"
    tokens = node.tokenize_formula(formula)
    postfix = node.infix_to_postfix(tokens)

    # Test operator precedence
    formula = "a + b * c"
    tokens = node.tokenize_formula(formula)
    postfix = node.infix_to_postfix(tokens)
    # We can't test exact postfix because it contains internal representations,
    # but we can test the evaluation result
    assert node.evaluate(formula, a=1, b=2, c=3)[0] == pytest.approx(7.0)

    # Test parentheses
    formula = "(a + b) * c"
    tokens = node.tokenize_formula(formula)
    postfix = node.infix_to_postfix(tokens)
    assert node.evaluate(formula, a=1, b=2, c=3)[0] == pytest.approx(9.0)

    # Test function calls
    formula = "sin(a) + cos(b)"
    tokens = node.tokenize_formula(formula)
    postfix = node.infix_to_postfix(tokens)
    assert node.evaluate(formula, a=math.pi/2, b=0)[0] == pytest.approx(2.0)

    # Test constant function calls
    formula = "pi() + e()"
    tokens = node.tokenize_formula(formula)
    postfix = node.infix_to_postfix(tokens)
    assert node.evaluate(formula)[0] == pytest.approx(math.pi + math.e)
