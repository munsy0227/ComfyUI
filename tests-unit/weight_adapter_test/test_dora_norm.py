import pytest
import torch

import comfy.cli_args
comfy.cli_args.args.cpu = True
from comfy.weight_adapter.base import weight_decompose


@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize("strength", [0., 0.5, 1.])
@pytest.mark.parametrize("shape", [(3, 2), (3, 2, 3, 3)])
def test_dora_normalizes_updated_direction(axis, strength, shape):
    torch.manual_seed(9)
    weight = torch.randn(shape)
    delta = torch.randn(shape) * 0.3
    direction = weight + delta * 0.7
    if axis == 1:
        norm = lambda w: w.flatten(1).norm(dim=1).reshape(shape[0], *([1] * (len(shape) - 1)))
    else:
        norm = lambda w: w.transpose(0, 1).flatten(1).norm(dim=1).reshape(shape[1], 1, *([1] * (len(shape) - 2))).transpose(0, 1)
    magnitude = norm(weight)
    expected = weight + strength * (direction * magnitude / norm(direction) - weight)
    actual = weight_decompose(magnitude, weight.clone(), delta.clone(), 0.7, strength, torch.float32, lambda x: x)
    torch.testing.assert_close(actual, expected)
