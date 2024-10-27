from typing import Any

from fluere.core.node import Node


def _int(value: Any) -> int:
    return int(value)


def _float(value: Any) -> float:
    return float(value)


def _str(value: Any) -> str:
    return str(value)


def _bool(value: Any) -> bool:
    return bool(value)


BUILTIN_NODES = {
    "_int": Node(_int, name="int"),
    "_float": Node(_float, name="float"),
    "_str": Node(_str, name="str"),
    "_bool": Node(_bool, name="bool"),
}
