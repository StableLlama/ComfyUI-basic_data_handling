#import pytest
from src.basic_data_handling.control_flow_nodes import (
    IfElse, SwitchCase, IfElifElse, ContinueFlow, FlowSelect, ForceCalculation, ExecutionOrder
)


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


def test_if_else_lazy_status():
    node = IfElse()

    # condition is True, if_true is needed
    assert node.check_lazy_status(True, None, "Value if False") == ["if_true"]
    # condition is True, if_true is not needed
    assert node.check_lazy_status(True, "Value if True", "Value if False") == []
    # condition is False, if_false is needed
    assert node.check_lazy_status(False, "Value if True", None) == ["if_false"]
    # condition is False, if_false is not needed
    assert node.check_lazy_status(False, "Value if True", "Value if False") == []


def test_switch_case():
    node = SwitchCase()

    # Selector within range, valid cases
    assert node.execute(0, case_0="Case 0", case_1="Case 1", case_2="Case 2", case_3="Case 3") == ("Case 0",)
    assert node.execute(1, case_0="Case 0", case_1="Case 1", case_2="Case 2", case_3="Case 3") == ("Case 1",)
    assert node.execute(3, case_0="Case 0", case_1="Case 1", case_2="Case 2", case_3="Case 3") == ("Case 3",)

    # Selector out of range, fallback to default case
    assert node.execute(4, case_0="Case 0", case_1="Case 1", case_2="Case 2", case_3="Case 3", default="Default") == ("Default",)
    assert node.execute(99, case_0="Case 0", case_1="Case 1", case_2="Case 2", case_3="Case 3", default="Default") == ("Default",)

    # Selector out of range, no default provided
    assert node.execute(4, case_0="Case 0", case_1="Case 1", case_2="Case 2", case_3="Case 3") == (None,)

    # Edge cases
    assert node.execute(0, case_0=None, case_1="Case 1", case_2="Case 2") == (None,)  # Case with None
    assert node.execute(2, case_0="Case 0", case_1="Case 1", case_2="Case 2") == ("Case 2",)
    assert node.execute(0, case_0=123, case_1=False, case_2="Case 2") == (123,)  # Different data types
    assert node.execute(10, case_0="Case 0", case_1="Case 1", case_2="Case 2", default="Fallback") == ("Fallback",)


def test_switch_case_lazy_status():
    node = SwitchCase()

    # select is valid, case is needed
    assert node.check_lazy_status(select=1, case_0="val", case_1=None, case_2="val2") == ["case_1"]
    # select is valid, case is not needed
    assert node.check_lazy_status(select=1, case_0="val", case_1="val1", case_2="val2") == []
    # select out of range, default is needed
    assert node.check_lazy_status(select=5, case_0="val", case_1="val1", default=None) == ["default"]
    # select out of range, default is not needed
    assert node.check_lazy_status(select=5, case_0="val", case_1="val1", default="default_val") == []
    # select out of range, no default
    assert node.check_lazy_status(select=5, case_0="val", case_1="val1") == []
    # non-numeric case key should be ignored
    assert node.check_lazy_status(select=0, case_a="val") == []


def test_if_elif_else():
    node = IfElifElse()
    # if is True
    assert node.execute(**{"if": True, "then": "if_val", "elif_0": False, "then_0": "elif0_val", "else": "else_val"}) == ("if_val",)
    # if is False, elif_0 is True
    assert node.execute(**{"if": False, "then": "if_val", "elif_0": True, "then_0": "elif0_val", "else": "else_val"}) == ("elif0_val",)
    # if is False, elif_0 is False, else
    assert node.execute(**{"if": False, "then": "if_val", "elif_0": False, "then_0": "elif0_val", "else": "else_val"}) == ("else_val",)
    # if is True, and one elif that is False, else
    assert node.execute(**{"if": True, "then": "if_val", "elif_0": False, "then_0": "elif0_val", "else": "else_val"}) == ("if_val",)
    # if is True, and one elif that is True, else
    assert node.execute(**{"if": True, "then": "if_val", "elif_0": True, "then_0": "elif0_val", "else": "else_val"}) == ("if_val",)
    # if is False, and one elif that is True, else
    assert node.execute(**{"if": False, "then": "if_val", "elif_0": True, "then_0": "elif0_val", "else": "else_val"}) == ("elif0_val",)
    # if is False, and one elif that is False, else
    assert node.execute(**{"if": False, "then": "if_val", "elif_0": False, "then_0": "elif0_val", "else": "else_val"}) == ("else_val",)
    # if is False, multiple elifs, one is true
    assert node.execute(**{"if": False, "then": "if_val", "elif_0": False, "then_0": "elif0_val", "elif_1": True, "then_1": "elif1_val", "else": "else_val"}) == ("elif1_val",)
    # all false, else
    assert node.execute(**{"if": False, "then": "if_val", "elif_0": False, "then_0": "elif0_val", "elif_1": False, "then_1": "elif1_val", "else": "else_val"}) == ("else_val",)
    # all false, no else
    assert node.execute(**{"if": False, "then": "if_val", "elif_0": False, "then_0": "elif0_val"}) == (None,)
    # Missing then for a true condition
    assert node.execute(**{"if": True, "elif_0": False, "then_0": "elif0_val"}) == (None,)


def test_if_elif_else_lazy_status():
    node = IfElifElse()
    # if is True, then is needed
    assert node.check_lazy_status(**{"if": True, "then": None, "else": "else_val"}) == ["then"]
    # if is True, then is not needed
    assert node.check_lazy_status(**{"if": True, "then": "if_val", "else": "else_val"}) == []
    # if is False, else is needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "else": None}) == ["else"]
    # if is False, else is not needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "else": "else_val"}) == []
    # if is False, elif_0 needs evaluation
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": None}) == ["elif_0"]
    # if is False, elif_0 needs evaluation
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": None, "else": None}) == ["elif_0"]
    # if is False, elif_0 needs evaluation
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": None, "else": "else_val"}) == ["elif_0"]
    # if is False, elif_0 False, else needs evaluation
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "else": None}) == ["else"]
    # if is False, elif_0 False, else needs evaluation but is already fulfilled
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "else": "else_val"}) == []
    # if is False, elif_0 is True, then_0 is needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": True, "then_0": None, "else": None}) == ["then_0"]
    # if is False, elif_0 is True, then_0 is needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": True, "then_0": None, "else": "else_val"}) == ["then_0"]
    # if is False, elif_0 is True, then_0 is not needed, but else is needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": True, "then_0": "elif0_val", "else": None}) == ["else"]
    # if is False, elif_0 is True, then_0 is not needed, but else is needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": True, "then_0": "elif0_val", "else": "else_val"}) == []
    # if is False, elif_0 False, elif_1 needs evaluation
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "elif_1": None}) == ["elif_1"]
    # if is False, elif_0 False, elif_1 needs evaluation
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "elif_1": None, "else": None}) == ["elif_1"]
    # if is False, elif_0 False, elif_1 needs evaluation
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "elif_1": None, "else": "else_val"}) == ["elif_1"]
    # if is False, elif_0 False, elif_1 False, else needs evaluation
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "elif_1": False, "else": None}) == ["else"]
    # if is False, elif_0 False, elif_1 False, else needs evaluation but is already fulfilled
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "elif_1": False, "else": "else_val"}) == []
    # if is False, elif_0 False, elif_1 is True, then_1 is needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "elif_1": True, "then_1": None, "else": None}) == ["then_1"]
    # if is False, elif_0 False, elif_1 is True, then_1 is needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "elif_1": True, "then_1": None, "else": "else_val"}) == ["then_1"]
    # if is False, elif_0 False, elif_1 is True, then_1 is not needed, but else is needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "elif_1": True, "then_1": "elif1_val", "else": None}) == ["else"]
    # if is False, elif_0 False, elif_1 is True, then_1 is not needed, but else is needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "elif_1": True, "then_1": "elif1_val", "else": "else_val"}) == []
    # all false, else is needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "then_0": "elif1_val", "else": None}) == ["else"]
    # all false, else is not needed
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "then_0": "elif1_val", "else": "else_val"}) == []
    # all false, no else
    assert node.check_lazy_status(**{"if": False, "then": "if_val", "elif_0": False, "then_0": "elif0_val"}) == []


def test_continue_flow():
    node = ContinueFlow()
    # select is True
    assert node.execute("some value", select=True) == ("some value",)
    # select is False
    assert node.execute("some value", select=False) == (None,)  # ExecutionBlocker(None) becomes None
    # select is default (True)
    assert node.execute("some value") == ("some value",)
    # Test with different value types
    assert node.execute(123, select=True) == (123,)
    assert node.execute([1, 2], select=False) == (None,)


def test_flow_select():
    node = FlowSelect()
    # select is True
    assert node.select("some value", select=True) == ("some value", None)
    # select is False
    assert node.select("some value", select=False) == (None, "some value")
    # select is default (True)
    assert node.select("some value") == ("some value", None)
    # Test with different value types
    assert node.select(42, select=True) == (42, None)
    assert node.select({'a': 1}, select=False) == (None, {'a': 1})


def test_force_calculation():
    node = ForceCalculation()
    # execute
    assert node.execute("some value") == ("some value",)
    assert node.execute(None) == (None,)


def test_execution_order():
    node = ExecutionOrder()
    # with "any node output"
    assert node.execute(**{'any node output': "passthrough_val"}) == (None, "passthrough_val")
    # without "any node output"
    assert node.execute() == (None, [])
    # with other kwargs
    assert node.execute(other_kwarg="some_val") == (None, [])
    # with multiple kwargs
    assert node.execute(**{'any node output': "passthrough_val", "E/O": "ignored"}) == (None, "passthrough_val")
