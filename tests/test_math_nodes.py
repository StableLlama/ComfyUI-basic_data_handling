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


def test_math_cos():
    node = MathCos()
    assert node.calculate(0, "radians") == (1.0,)
    assert node.calculate(math.pi, "radians") == (-1.0,)
    assert node.calculate(60, "degrees") == (math.cos(math.radians(60)),)


def test_math_tan():
    node = MathTan()
    assert node.calculate(0, "radians") == (0.0,)
    assert node.calculate(45, "degrees") == (math.tan(math.radians(45)),)
    with pytest.raises(ValueError):  # Undefined tangent
        node.calculate(90, "degrees")


def test_math_asin():
    node = MathAsin()
    assert node.calculate(0, "radians") == (0.0,)
    assert node.calculate(1, "radians") == (math.pi / 2,)
    assert node.calculate(0.5, "degrees") == (math.degrees(math.asin(0.5)),)


def test_math_acos():
    node = MathAcos()
    assert node.calculate(1, "radians") == (0.0,)
    assert node.calculate(0, "radians") == (math.pi / 2,)
    assert node.calculate(0.5, "degrees") == (math.degrees(math.acos(0.5)),)


def test_math_atan():
    node = MathAtan()
    assert node.calculate(0, "radians") == (0.0,)
    assert node.calculate(1, "degrees") == (45.0,)
    assert node.calculate(-1, "radians") == (-math.pi / 4,)


def test_math_atan2():
    node = MathAtan2()
    assert node.calculate(0, 1, "radians") == (0.0,)
    assert node.calculate(1, 1, "degrees") == (45.0,)
    assert node.calculate(-1, -1, "radians") == (-3 * math.pi / 4,)


def test_math_sqrt():
    node = MathSqrt()
    assert node.calculate(4) == (2.0,)
    assert node.calculate(0) == (0.0,)
    with pytest.raises(ValueError):  # Negative numbers
        node.calculate(-1)


def test_math_exp():
    node = MathExp()
    assert node.calculate(0) == (1.0,)
    assert node.calculate(1) == (math.e,)
    assert node.calculate(-1) == (1 / math.e,)


def test_math_log():
    node = MathLog()
    assert node.calculate(1) == (0.0,)
    assert node.calculate(math.e) == (1.0,)
    assert node.calculate(8, base=2) == (3.0,)
    with pytest.raises(ValueError):  # Log of non-positive
        node.calculate(-1)


def test_math_log10():
    node = MathLog10()
    assert node.calculate(1) == (0.0,)
    assert node.calculate(10) == (1.0,)
    with pytest.raises(ValueError):  # Log of non-positive
        node.calculate(0)


def test_math_degrees():
    node = MathDegrees()
    assert node.calculate(math.pi) == (180.0,)
    assert node.calculate(math.pi / 2) == (90.0,)
    assert node.calculate(0) == (0.0,)


def test_math_radians():
    node = MathRadians()
    assert node.calculate(180) == (math.pi,)
    assert node.calculate(90) == (math.pi / 2,)
    assert node.calculate(0) == (0.0,)


def test_math_floor():
    node = MathFloor()
    assert node.calculate(1.7) == (1,)
    assert node.calculate(-1.7) == (-2,)
    assert node.calculate(0.0) == (0,)


def test_math_ceil():
    node = MathCeil()
    assert node.calculate(1.2) == (2,)
    assert node.calculate(-1.2) == (-1,)
    assert node.calculate(0.0) == (0,)


def test_math_abs():
    node = MathAbs()
    assert node.calculate(-5) == (5,)
    assert node.calculate(5) == (5,)
    assert node.calculate(0) == (0,)


def test_math_pi():
    node = MathPi()
    assert node.calculate() == (math.pi,)


def test_math_e():
    node = MathE()
    assert node.calculate() == (math.e,)


def test_math_min():
    node = MathMin()
    assert node.calculate(5, 10) == (5,)
    assert node.calculate(-1, 0) == (-1,)
    assert node.calculate(3.5, 2.5) == (2.5,)


def test_math_max():
    node = MathMax()
    assert node.calculate(5, 10) == (10,)
    assert node.calculate(-1, 0) == (0,)
    assert node.calculate(3.5, 2.5) == (3.5,)
