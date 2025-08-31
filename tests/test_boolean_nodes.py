#import pytest

from src.basic_data_handling.boolean_nodes import (
    BooleanAnd,
    BooleanOr,
    BooleanNot,
    BooleanXor,
    BooleanNand,
    BooleanNor,
)


def test_boolean_and():
    node = BooleanAnd()
    assert node.and_operation(True, True) == (True,)
    assert node.and_operation(True, False) == (False,)
    assert node.and_operation(False, True) == (False,)
    assert node.and_operation(False, False) == (False,)


def test_boolean_or():
    node = BooleanOr()
    assert node.or_operation(True, True) == (True,)
    assert node.or_operation(True, False) == (True,)
    assert node.or_operation(False, True) == (True,)
    assert node.or_operation(False, False) == (False,)


def test_boolean_not():
    node = BooleanNot()
    assert node.not_operation(True) == (False,)
    assert node.not_operation(False) == (True,)


def test_boolean_xor():
    node = BooleanXor()
    assert node.xor_operation(True, True) == (False,)
    assert node.xor_operation(True, False) == (True,)
    assert node.xor_operation(False, True) == (True,)
    assert node.xor_operation(False, False) == (False,)


def test_boolean_nand():
    node = BooleanNand()
    assert node.nand_operation(True, True) == (False,)
    assert node.nand_operation(True, False) == (True,)
    assert node.nand_operation(False, True) == (True,)
    assert node.nand_operation(False, False) == (True,)


def test_boolean_nor():
    node = BooleanNor()
    assert node.nor_operation(True, True) == (False,)
    assert node.nor_operation(True, False) == (False,)
    assert node.nor_operation(False, True) == (False,)
    assert node.nor_operation(False, False) == (True,)
