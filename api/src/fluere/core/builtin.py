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


BUILTIN_NODES = [
    Node(_int, name="int"),
    Node(_float, name="float"),
    Node(_str, name="str"),
    Node(_bool, name="bool"),
]
