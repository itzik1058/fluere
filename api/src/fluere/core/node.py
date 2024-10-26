import inspect
from collections.abc import Callable
from enum import StrEnum
from typing import Any, Self

from pydantic import BaseModel

NodeParameterKind = StrEnum(
    "NodeParameterKind",
    [
        "POSITIONAL_ONLY",
        "POSITIONAL_OR_KEYWORD",
        "VAR_POSITIONAL",
        "KEYWORD_ONLY",
        "VAR_KEYWORD",
    ],
)  # same as inspect._ParameterKind but StrEnum


class NodeParameter(BaseModel):
    name: str
    kind: NodeParameterKind
    default: str | None
    annotation: str | None


class NodeSignature(BaseModel):
    name: str
    parameters: dict[str, NodeParameter]
    return_annotation: str | None

    @staticmethod
    def _annotation_repr(annotation: Any) -> str:
        return f"{annotation.__module__}.{annotation.__name__}"

    @classmethod
    def from_callable(cls, func: Callable[..., Any]) -> Self:
        signature = inspect.signature(func)
        parameter_kind: list[NodeParameterKind] = list(NodeParameterKind)
        parameters = {}
        for name, parameter in signature.parameters.items():
            default = None
            if parameter.default != parameter.empty:
                default = str(parameter.default)

            annotation = None
            if parameter.annotation != parameter.empty:
                annotation = cls._annotation_repr(parameter.annotation)

            parameters[name] = NodeParameter(
                name=parameter.name,
                kind=parameter_kind[parameter.kind],
                default=default,
                annotation=annotation,
            )
        return_annotation = None
        if signature.return_annotation != signature.empty:
            return_annotation = cls._annotation_repr(signature.return_annotation)
        return cls(
            name=func.__qualname__,
            parameters=parameters,
            return_annotation=return_annotation,
        )


class Node:
    def __init__(
        self,
        func: Callable[..., Any],
        name: str | None = None,
    ) -> None:
        self._signature = NodeSignature.from_callable(func)
        self._func = func

        if name is not None:
            self._signature.name = name

    @property
    def signature(self) -> NodeSignature:
        return self._signature

    @property
    def name(self) -> str:
        return self._signature.name
