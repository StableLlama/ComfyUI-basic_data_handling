import torch
from src.basic_data_handling.tensor_nodes import (
    TensorCreate, TensorBinaryOp, TensorUnaryOp, TensorSlice,
    TensorReshape, TensorPermute, TensorJoin, TensorInfo
)

def test_tensor_create():
    node = TensorCreate()
    # From list
    result = node.create([1, 2, 3])
    assert isinstance(result[0], torch.Tensor)
    assert torch.equal(result[0], torch.tensor([1, 2, 3]))

    # From scalar
    result = node.create(5.0)
    assert torch.equal(result[0], torch.tensor(5.0))

    # From existing tensor
    t = torch.tensor([1.0, 2.0])
    result = node.create(t)
    assert result[0] is t

def test_tensor_binary_op():
    node = TensorBinaryOp()
    a = torch.tensor([10.0, 20.0])
    b = torch.tensor([2.0, 4.0])

    assert torch.equal(node.operate(a, b, "add")[0], a + b)
    assert torch.equal(node.operate(a, b, "subtract")[0], a - b)
    assert torch.equal(node.operate(a, b, "multiply")[0], a * b)
    assert torch.equal(node.operate(a, b, "divide")[0], a / b)
    assert torch.equal(node.operate(a, 2.0, "power")[0], a ** 2.0)

def test_tensor_unary_op():
    node = TensorUnaryOp()
    t = torch.tensor([-1.0, 0.0, 1.0])

    assert torch.equal(node.operate(t, "abs")[0], torch.tensor([1.0, 0.0, 1.0]))
    assert torch.equal(node.operate(t, "neg")[0], torch.tensor([1.0, 0.0, -1.0]))
    assert torch.equal(node.operate(torch.tensor([0.0]), "sin")[0], torch.tensor([0.0]))

def test_tensor_slice():
    node = TensorSlice()
    t = torch.arange(10).reshape(2, 5) # [[0,1,2,3,4], [5,6,7,8,9]]

    # Simple slice
    result = node.slice_tensor(t, "0, 1:3")
    assert torch.equal(result[0], t[0, 1:3])

    # Ellipsis/Full slice
    result = node.slice_tensor(t, ":, 2")
    assert torch.equal(result[0], t[:, 2])

def test_tensor_reshape():
    node = TensorReshape()
    t = torch.arange(6)

    result = node.reshape(t, "2, 3")
    assert result[0].shape == (2, 3)

    result = node.reshape(t, "-1, 2")
    assert result[0].shape == (3, 2)

def test_tensor_permute():
    node = TensorPermute()
    t = torch.randn(2, 3, 4)

    result = node.permute(t, "2, 0, 1")
    assert result[0].shape == (4, 2, 3)

def test_tensor_join():
    node = TensorJoin()
    t1 = torch.tensor([1, 2])
    t2 = torch.tensor([3, 4])

    # Cat
    result = node.join(t1, t2, 0, "concatenate")
    assert torch.equal(result[0], torch.tensor([1, 2, 3, 4]))

    # Stack
    result = node.join(t1, t2, 0, "stack")
    assert result[0].shape == (2, 2)
    assert torch.equal(result[0], torch.tensor([[1, 2], [3, 4]]))

def test_tensor_info():
    node = TensorInfo()
    t = torch.zeros((2, 3), dtype=torch.float32)

    shape, dtype, device = node.get_info(t)
    assert shape == [2, 3]
    assert "float32" in dtype
    assert isinstance(device, str)
