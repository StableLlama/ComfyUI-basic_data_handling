#import pytest

from src.basic_data_handling.boolean_nodes import (
    BooleanAnd,
    BooleanOr,
    BooleanNot,
    BooleanXor,
    BooleanNand,
    BooleanNor,
    GenericAnd,
    GenericOr,
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


def test_generic_or():
    node = GenericOr()
    # 2xOR
    assert node.or_operation(False, item_0=True, item_1=True) == (True,)
    assert node.or_operation(False, item_0=True, item_1=False) == (True,)
    assert node.or_operation(False, item_0=False, item_1=True) == (True,)
    assert node.or_operation(False, item_0=False, item_1=False) == (False,)
    # 2xNOR
    assert node.or_operation(True, item_0=True, item_1=True) == (False,)
    assert node.or_operation(True, item_0=True, item_1=False) == (False,)
    assert node.or_operation(True, item_0=False, item_1=True) == (False,)
    assert node.or_operation(True, item_0=False, item_1=False) == (True,)
    # A couple of 3xOR cases
    assert node.or_operation(False, item_0=False, item_1=False, item_2=True) == (True,)
    assert node.or_operation(False, item_0=False, item_1=False, item_2=False) == (False,)


def test_generic_and():
    node = GenericAnd()
    # 2xAND
    assert node.and_operation(False, item_0=True, item_1=True) == (True,)
    assert node.and_operation(False, item_0=True, item_1=False) == (False,)
    assert node.and_operation(False, item_0=False, item_1=True) == (False,)
    assert node.and_operation(False, item_0=False, item_1=False) == (False,)
    # 2xNAND
    assert node.and_operation(True, item_0=True, item_1=True) == (False,)
    assert node.and_operation(True, item_0=True, item_1=False) == (True,)
    assert node.and_operation(True, item_0=False, item_1=True) == (True,)
    assert node.and_operation(True, item_0=False, item_1=False) == (True,)
    # A couple of 3xAND cases
    assert node.and_operation(False, item_0=True, item_1=True, item_2=True) == (True,)
    assert node.and_operation(False, item_0=True, item_1=False, item_2=True) == (False,)
