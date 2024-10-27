import pytest

from fluere.core import BUILTIN_NODES


def test_nodes() -> None:
    _int = BUILTIN_NODES["_int"]
    assert _int(5) == 5
    assert _int("3") == int("3")
    with pytest.raises(TypeError):
        _int(None)
