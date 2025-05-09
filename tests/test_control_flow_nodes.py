#import pytest
from src.basic_data_handling.control_flow_nodes import IfElse, SwitchCase


def test_if_else():
    node = IfElse()

    # Test where condition is True
    assert node.execute(True, "Value if True", "Value if False") == ("Value if True",)

    # Test where condition is False
    assert node.execute(False, "Value if True", "Value if False") == ("Value if False",)

    # Test edge cases
    assert node.execute(True, 1, 2) == (1,)  # Integers
    assert node.execute(False, [1, 2, 3], None) == (None,)  # Complex types
    assert node.execute(True, None, "fallback") == (None,)  # Fallback to True branch


def test_switch_case():
    node = SwitchCase()

    # Selector within range, valid cases
    assert node.execute(0, "Case 0", "Case 1", "Case 2", "Case 3") == ("Case 0",)
    assert node.execute(1, "Case 0", "Case 1", "Case 2", "Case 3") == ("Case 1",)
    assert node.execute(3, "Case 0", "Case 1", "Case 2", "Case 3") == ("Case 3",)

    # Selector out of range, fallback to default case
    assert node.execute(4, "Case 0", "Case 1", "Case 2", "Case 3", default="Default") == ("Default",)
    assert node.execute(99, "Case 0", "Case 1", "Case 2", "Case 3", default="Default") == ("Default",)

    # Selector out of range, no default provided
    assert node.execute(4, "Case 0", "Case 1", "Case 2", "Case 3") == (None,)

    # Edge cases
    assert node.execute(0, None, "Case 1", "Case 2") == (None,)  # Case with None
    assert node.execute(2, "Case 0", "Case 1", "Case 2") == ("Case 2",)
    assert node.execute(0, 123, False, "Case 2") == (123,)  # Different data types
    assert node.execute(10, "Case 0", "Case 1", "Case 2", default="Fallback") == ("Fallback",)
