import pytest

from fluere.core.builtin import BUILTIN_NODES


def test_nodes():
    _int = BUILTIN_NODES["_int"]
    assert _int(5) == 5
    assert _int("3") == int("3")
    with pytest.raises(TypeError):
        _int(None)
