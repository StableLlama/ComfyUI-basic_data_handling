import pytest
import math
from src.basic_data_handling.math_nodes import (
    MathSin, MathCos, MathTan, MathAsin, MathAcos, MathAtan, MathAtan2,
    MathSqrt, MathExp, MathLog, MathLog10, MathDegrees, MathRadians,
    MathFloor, MathCeil, MathAbs, MathPi, MathE, MathMin, MathMax,
)


def test_math_sin():
    node = MathSin()
    assert node.calculate(0, "radians") == (0.0,)
    assert node.calculate(math.pi / 2, "radians") == (1.0,)
    assert node.calculate(30, "degrees") == (math.sin(math.radians(30)),)
    # Test with string input
    assert node.calculate("45", "degrees")[0] == pytest.approx(math.sin(math.radians(45)))
    # Test negative angle
    assert node.calculate(-90, "degrees")[0] == pytest.approx(-1.0)


def test_math_cos():
    node = MathCos()
    assert node.calculate(0, "radians") == (1.0,)
    assert node.calculate(math.pi, "radians") == (-1.0,)
    assert node.calculate(60, "degrees") == (math.cos(math.radians(60)),)
    # Test with string input
    assert node.calculate("60", "degrees")[0] == pytest.approx(0.5)
    # Test negative angle
    assert node.calculate(-180, "degrees")[0] == pytest.approx(-1.0)


def test_math_tan():
    node = MathTan()
    assert node.calculate(0, "radians") == (0.0,)
    assert node.calculate(45, "degrees") == (math.tan(math.radians(45)),)
    # Test with string input
    assert node.calculate("30", "degrees")[0] == pytest.approx(math.tan(math.radians(30)))
    # Test negative angle
    assert node.calculate(-45, "degrees")[0] == pytest.approx(-1.0)
    # Test undefined tangent
    with pytest.raises(ValueError):  # Undefined tangent
        node.calculate(90, "degrees")
    with pytest.raises(ValueError):  # Undefined tangent
        node.calculate(math.pi/2, "radians")


def test_math_asin():
    node = MathAsin()
    assert node.calculate(0, "radians") == (0.0,)
    assert node.calculate(1, "radians") == (math.pi / 2,)
    assert node.calculate(0.5, "degrees") == (math.degrees(math.asin(0.5)),)
    # Test with string input
    assert node.calculate("0.5", "degrees")[0] == pytest.approx(30.0)
    # Test boundary values
    assert node.calculate(-1, "degrees")[0] == pytest.approx(-90.0)
    # Test out of range values
    with pytest.raises(ValueError):
        node.calculate(1.1, "degrees")


def test_math_acos():
    node = MathAcos()
    assert node.calculate(1, "radians") == (0.0,)
    assert node.calculate(0, "radians") == (math.pi / 2,)
    assert node.calculate(0.5, "degrees") == (math.degrees(math.acos(0.5)),)
    # Test with string input
    assert node.calculate("0.5", "degrees")[0] == pytest.approx(60.0)
    # Test boundary values
    assert node.calculate(-1, "degrees")[0] == pytest.approx(180.0)
    # Test out of range values
    with pytest.raises(ValueError):
        node.calculate(1.1, "degrees")


def test_math_atan():
    node = MathAtan()
    assert node.calculate(0, "radians") == (0.0,)
    assert node.calculate(1, "degrees") == (45.0,)
    assert node.calculate(-1, "radians") == (-math.pi / 4,)
    # Test with string input
    assert node.calculate("1.0", "degrees")[0] == pytest.approx(45.0)
    # Test large values
    assert node.calculate(1000, "degrees")[0] == pytest.approx(89.94, abs=0.01)


def test_math_atan2():
    node = MathAtan2()
    assert node.calculate(0, 1, "radians") == (0.0,)
    assert node.calculate(1, 1, "degrees") == (45.0,)
    assert node.calculate(-1, -1, "radians") == (-3 * math.pi / 4,)
    # Test with string input
    assert node.calculate("1", "1", "degrees")[0] == pytest.approx(45.0)
    # Test special cases
    assert node.calculate(1, 0, "degrees")[0] == pytest.approx(90.0)
    assert node.calculate(-1, 0, "degrees")[0] == pytest.approx(-90.0)
    assert node.calculate(0, -1, "degrees")[0] == pytest.approx(180.0)


def test_math_sqrt():
    node = MathSqrt()
    assert node.calculate(4) == (2.0,)
    assert node.calculate(0) == (0.0,)
    # Test with string input
    assert node.calculate("9")[0] == pytest.approx(3.0)
    # Test with float input
    assert node.calculate(2.25)[0] == pytest.approx(1.5)
    # Test negative numbers (should raise ValueError)
    with pytest.raises(ValueError):
        node.calculate(-1)


def test_math_exp():
    node = MathExp()
    assert node.calculate(0) == (1.0,)
    assert node.calculate(1) == (math.e,)
    assert node.calculate(-1) == (1 / math.e,)
    # Test with string input
    assert node.calculate("2")[0] == pytest.approx(math.exp(2))
    # Test with large input
    assert node.calculate(10)[0] == pytest.approx(math.exp(10))


def test_math_log():
    node = MathLog()
    assert node.calculate(1) == (0.0,)
    assert node.calculate(math.e) == (1.0,)
    assert node.calculate(8, base=2) == (3.0,)
    # Test with string input
    assert node.calculate("10", base="10")[0] == pytest.approx(1.0)
    # Test with default base (e)
    assert node.calculate(math.exp(5))[0] == pytest.approx(5.0)
    # Test with log of non-positive (should raise ValueError)
    with pytest.raises(ValueError):
        node.calculate(-1)
    with pytest.raises(ValueError):
        node.calculate(0)


def test_math_log10():
    node = MathLog10()
    assert node.calculate(1) == (0.0,)
    assert node.calculate(10) == (1.0,)
    # Test with string input
    assert node.calculate("100")[0] == pytest.approx(2.0)
    # Test with non-integer values
    assert node.calculate(2)[0] == pytest.approx(math.log10(2))
    # Test with log of non-positive (should raise ValueError)
    with pytest.raises(ValueError):
        node.calculate(0)
    with pytest.raises(ValueError):
        node.calculate(-10)


def test_math_degrees():
    node = MathDegrees()
    assert node.calculate(math.pi) == (180.0,)
    assert node.calculate(math.pi / 2) == (90.0,)
    assert node.calculate(0) == (0.0,)
    # Test with string input
    assert node.calculate("3.14159")[0] == pytest.approx(180.0, abs=0.01)
    # Test with negative values
    assert node.calculate(-math.pi)[0] == pytest.approx(-180.0)


def test_math_radians():
    node = MathRadians()
    assert node.calculate(180) == (math.pi,)
    assert node.calculate(90) == (math.pi / 2,)
    assert node.calculate(0) == (0.0,)
    # Test with string input
    assert node.calculate("180")[0] == pytest.approx(math.pi)
    # Test with negative values
    assert node.calculate(-180)[0] == pytest.approx(-math.pi)
    # Test with decimal values
    assert node.calculate(45.5)[0] == pytest.approx(math.radians(45.5))


def test_math_floor():
    node = MathFloor()
    assert node.calculate(1.7) == (1,)
    assert node.calculate(-1.7) == (-2,)
    assert node.calculate(0.0) == (0,)
    # Test with string input
    assert node.calculate("3.9")[0] == 3
    # Test with integer input
    assert node.calculate(5)[0] == 5
    # Test with very small decimals
    assert node.calculate(0.0001)[0] == 0


def test_math_ceil():
    node = MathCeil()
    assert node.calculate(1.2) == (2,)
    assert node.calculate(-1.2) == (-1,)
    assert node.calculate(0.0) == (0,)
    # Test with string input
    assert node.calculate("3.1")[0] == 4
    # Test with integer input
    assert node.calculate(5)[0] == 5
    # Test with very small decimals
    assert node.calculate(0.0001)[0] == 1


def test_math_abs():
    node = MathAbs()
    assert node.calculate(-5) == (5,)
    assert node.calculate(5) == (5,)
    assert node.calculate(0) == (0,)
    # Test with string input
    assert node.calculate("-3.14")[0] == pytest.approx(3.14)
    # Test with float input
    assert node.calculate(-2.5)[0] == 2.5
    # Test with zero
    assert node.calculate(0)[0] == 0


def test_math_pi():
    node = MathPi()
    assert node.calculate() == (math.pi,)
    # Verify precision to at least 10 decimal places
    assert abs(node.calculate()[0] - 3.1415926535) < 1e-10


def test_math_e():
    node = MathE()
    assert node.calculate() == (math.e,)
    # Verify precision to at least 10 decimal places
    assert abs(node.calculate()[0] - 2.7182818284) < 1e-10


def test_math_min():
    node = MathMin()
    assert node.calculate(5, 10) == (5,)
    assert node.calculate(-1, 0) == (-1,)
    assert node.calculate(3.5, 2.5) == (2.5,)
    # Test with string inputs
    assert node.calculate("7", "3")[0] == 3.0
    # Test with mixed types
    assert node.calculate(5, "2.5")[0] == 2.5
    # Test with equal values
    assert node.calculate(10, 10)[0] == 10


def test_math_max():
    node = MathMax()
    assert node.calculate(5, 10) == (10,)
    assert node.calculate(-1, 0) == (0,)
    assert node.calculate(3.5, 2.5) == (3.5,)
    # Test with string inputs
    assert node.calculate("7", "3")[0] == 7.0
    # Test with mixed types
    assert node.calculate(5, "7.5")[0] == 7.5
    # Test with equal values
    assert node.calculate(10, 10)[0] == 10
